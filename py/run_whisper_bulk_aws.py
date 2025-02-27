import whisper
import os
import boto3
from io import BytesIO
import tempfile

# Initialize the S3 client
print("Initializing S3 client...")
# Specify the profile name
session = boto3.Session(profile_name='AWSAdministratorAccessPersonal')
s3 = session.client('s3')

print("Loading Whisper model...")
model = whisper.load_model("turbo")
count = 0

# S3 bucket and directories
bucket_name = "whisper-gus"
audio_dir = "audio-files/"
output_file = "output/transcription-all.txt"

# List all audio files in the S3 bucket directory
print(f"Listing audio files in S3 bucket '{bucket_name}' with prefix '{audio_dir}'...")
response = s3.list_objects_v2(Bucket=bucket_name, Prefix=audio_dir)
audio_files = [item['Key'] for item in response.get('Contents', []) if item['Key'].endswith(".opus")]

print(f"Found {len(audio_files)} audio files.")

# Iterate over all audio files in the S3 bucket directory
for audio_file in audio_files:
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
    print(f"{count} Transcription for {audio_file} written to {output_file}")

    # Clean up the temporary file
    os.remove(temp_audio_file_path)

print("Processing complete.")
