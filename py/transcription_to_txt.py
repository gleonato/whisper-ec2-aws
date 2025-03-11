def update_chat_with_transcription(audio_file, output_data):
    """
    Update the chat.txt file by inserting the transcription before the audio file reference.

    :param audio_file: The full path of the audio file.
    :param output_data: The transcription text to insert before the audio file reference.
    """
    import os

    # Trim the path prefix to leave only the file name
    audio_file_name = os.path.basename(audio_file)

    # Read the chat.txt file
    chat_file_path = '/Users/gusleonato/Personal/Whisper/Chat.txt'
    with open(chat_file_path, 'r', encoding='utf-8') as chat_file:
        chat_content = chat_file.read()

    # Insert the transcription before the audio file reference
    updated_chat_content = chat_content.replace(audio_file_name, f"{output_data}\n{audio_file_name}")

    # Append the updated content to the chat_txt_output.txt file
    output_file_path = '/Users/gusleonato/Personal/Whisper/chat_txt_output.txt'
    with open(output_file_path, 'a', encoding='utf-8') as output_file:
        output_file.write(updated_chat_content)

    print(f"Updated chat content appended to {output_file_path}")

# Example usage
# update_chat_with_transcription("audio-files/PTT-20190118-WA0145.opus", "This is the transcription text.")