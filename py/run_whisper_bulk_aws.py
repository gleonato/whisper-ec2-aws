import os
import json
import whisper
import boto3
from io import BytesIO
import tempfile
from push import send_sns_message
from transcription_to_txt import update_chat_with_transcription

# Unset the environment variable MallocStackLogging to avoid memory issues
os.environ['MallocStackLogging'] = '0'

# Initialize the S3 client
print("Initializing S3 client...")
# Specify the profile name
session = boto3.Session(profile_name='AWSAdministratorAccessPersonal')
s3 = session.client('s3')

print("Loading Whisper model...")
# model references here: https://github.com/openai/whisper
# model = whisper.load_model("turbo") # Load the turbo model
# Change from "turbo" to a smaller model
model = whisper.load_model("medium")  # or "tiny" or "small" and "medium" 

# S3 bucket and directories
bucket_name = "whisper-gus"
audio_dir = "audio-files/"
output_file = "output/transcription-all.txt"
sns_topic_arn = "arn:aws:sns:us-east-1:437930410990:sms_notification_topic"  # Replace with your actual SNS topic ARN

# Load the progress file if it exists
progress_file = "transcription_progress.json"
if os.path.exists(progress_file):
    with open(progress_file, "r") as f:
        progress = json.load(f)
    count = progress.get("count", 0)
    processed_files = set(progress.get("processed_files", []))
else:
    count = 0
    processed_files = set()

# List all audio files in the S3 bucket directory with pagination
print(f"Listing audio files in S3 bucket '{bucket_name}' with prefix '{audio_dir}'...")
audio_files = []
paginator = s3.get_paginator('list_objects_v2')
page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=audio_dir)

for page in page_iterator:
    if 'Contents' in page:
        audio_files.extend([item['Key'] for item in page['Contents'] if item['Key'].endswith(".opus")])

print(f"Found {len(audio_files)} audio files.")

# Iterate over all audio files in the S3 bucket directory
for audio_file in audio_files:
    if audio_file in processed_files:
        continue
    print(f"Processing file: {audio_file}")

    # Load audio from S3
    print(f"Loading audio file '{audio_file}' from S3...")
    audio_obj = s3.get_object(Bucket=bucket_name, Key=audio_file)
    audio_data = BytesIO(audio_obj['Body'].read())
    audio_bytes = audio_data.read()

    # Save audio bytes to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".opus") as temp_audio_file:
        temp_audio_file.write(audio_bytes)
        temp_audio_file_path = temp_audio_file.name

    # Load audio from the temporary file
    audio = whisper.load_audio(temp_audio_file_path)

    # Ensure the audio is in the correct format
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # Make log-Mel spectrogram and move to the same device as the model
    print("Generating log-Mel spectrogram...")
    mel = whisper.log_mel_spectrogram(audio, n_mels=model.dims.n_mels).to(model.device)

    # Detect the spoken language
    print("Detecting language...")
    _, probs = model.detect_language(mel)
    detected_language = max(probs, key=probs.get)
    print(f"Detected language for {audio_file}: {detected_language}")

    # Decode the audio
    print("Decoding audio...")
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)

    # Append the recognized text to the output file in S3
    print(f"Appending transcription to '{output_file}' in S3...")
    try:
        output_obj = s3.get_object(Bucket=bucket_name, Key=output_file)
        output_data = output_obj['Body'].read().decode('utf-8')
    except s3.exceptions.NoSuchKey:
        output_data = ""
    output_data += f"Transcription for {audio_file}:\n{result.text}\n\n"

    s3.put_object(Bucket=bucket_name, Key=output_file, Body=output_data.encode('utf-8'))
    count += 1
    print(f"{count}/{len(audio_files)} Transcription for {audio_file} written to {output_file}")

    # Update chat.txt with the transcription
    update_chat_with_transcription(audio_file, result.text, s3_client=s3)

    # Send SNS notification every 1000 files
    if count % 1000 == 0:
        print(f"Sending SNS notification for {count} files processed...")
        message = f"Transcription for {count}/{len(audio_files)} files completed. Last processed file: {audio_file}. Detected language: {detected_language}."
        send_sns_message(sns_topic_arn, message, subject="Transcription Batch Completed")

    # Clean up the temporary file
    os.remove(temp_audio_file_path)

    # Update the progress file
    processed_files.add(audio_file)
    with open(progress_file, "w") as f:
        json.dump({"count": count, "processed_files": list(processed_files)}, f)

# After the loop ends, add completion notification
print("Processing complete.")
final_message = f"Transcription processing completed. Total files processed: {count}. Final file: {audio_file if count > 0 else 'None'}."
print(f"Sending final completion notification...")
send_sns_message(sns_topic_arn, final_message, subject="Transcription Processing Complete")
