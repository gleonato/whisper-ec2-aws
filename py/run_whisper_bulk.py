import whisper
import os

model = whisper.load_model("turbo")
count = 0

# Directory containing audio files
audio_dir = "/Users/gusleonato/Personal/Whisper/audio-files"
output_file = "transcription-all-984222220.txt"

# Open the output file in write mode
with open(output_file, "w") as f:
    # Iterate over all audio files in the directory
    for audio_file in os.listdir(audio_dir):
        if audio_file.endswith(".opus"):
            # # Load audio and pad/trim it to fit 30 seconds
            audio_path = os.path.join(audio_dir, audio_file)
            audio = whisper.load_audio(audio_path)
            audio = whisper.pad_or_trim(audio)

            # Make log-Mel spectrogram and move to the same device as the model
            mel = whisper.log_mel_spectrogram(audio, n_mels=model.dims.n_mels).to(model.device)

            # Detect the spoken language
            _, probs = model.detect_language(mel)
            detected_language = max(probs, key=probs.get)
            print(f"Detected language for {audio_file}: {detected_language}")

            # Decode the audio
            options = whisper.DecodingOptions()
            result = whisper.decode(model, mel, options)

           # Open the output file in append mode and write the recognized text
        with open(output_file, "a") as f:
            count += 1
            f.write(f"Transcription for {audio_file}:\n{result.text}\n\n")
            print(f"{count} Transcription for {audio_file} written to {output_file}")
            