def update_chat_with_transcription(audio_file, output_data, s3_client=None):
    """
    Update the chat_txt_output.txt file in S3 by inserting the transcription before the audio file reference.
    If the file doesn't exist, create it using the content from Chat.txt in S3.

    :param audio_file: The full path of the audio file.
    :param output_data: The transcription text to insert before the audio file reference.
    :param s3_client: Boto3 S3 client. If None, a new client will be created.
    """
    import os
    import boto3
    from io import BytesIO

    # Create S3 client if not provided
    if s3_client is None:
        session = boto3.Session(profile_name='AWSAdministratorAccessPersonal')
        s3_client = session.client('s3')

    # Trim the path prefix to leave only the file name
    audio_file_name = os.path.basename(audio_file)

    # Define S3 paths
    bucket_name = "whisper-gus"
    chat_file_key = "input/chat.txt"
    output_file_key = "output/chat_txt_output.txt"

    # Read the chat.txt file from S3
    try:
        chat_obj = s3_client.get_object(Bucket=bucket_name, Key=chat_file_key)
        chat_content = chat_obj['Body'].read().decode('utf-8')
    except Exception as e:
        print(f"Error reading S3 input file: {e}")
        return

    # Insert the transcription before the audio file reference
    updated_content = chat_content.replace(audio_file_name, f"{output_data}\n{audio_file_name}")

    # Check if output file exists in S3
    try:
        output_exists = True
        output_obj = s3_client.get_object(Bucket=bucket_name, Key=output_file_key)
        existing_content = output_obj['Body'].read().decode('utf-8')
        
        # Insert the transcription in the existing file
        existing_content = existing_content.replace(audio_file_name, f"{output_data}\n{audio_file_name}")
        content_to_write = existing_content
    except s3_client.exceptions.NoSuchKey:
        output_exists = False
        content_to_write = updated_content

    # Write content to S3
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=output_file_key,
            Body=content_to_write.encode('utf-8')
        )
        status = "updated" if output_exists else "created"
        print(f"Transcription for {audio_file_name} {status} in s3://{bucket_name}/{output_file_key}")
    except Exception as e:
        print(f"Error writing to S3: {e}")

# Example usage
# update_chat_with_transcription("audio-files/PTT-20190118-WA0145.opus", "This is the transcription text.")