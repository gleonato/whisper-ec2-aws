# Whisper on AWS

## Overview
Whisper on AWS is a framework designed to facilitate the transcription of audio files using OpenAI's Whisper model on AWS infrastructure. This setup allows for scalable and efficient processing of large batches of audio files. It uses OPEN-AI Whisper general-purpose speech recognition. https://github.com/openai/whisper

## Whatsapp export

Export the entire whatsapp chat (INCLUDING MEDIA) and save it;

unzip and move all audio files (*.OPUS) to a foldew (i.e /audio-files)

move also the .txt file and saive it WhatsApp Chat with XXXXX for instance; This is going to be used so input the trasncriptions in the future;

para usar o s3: 

crie uma estrutura de diretorios

audio-files/
input/
input/chat.txt
output/



## Setup Instructions

### 1. Install Miniconda
Miniconda is a minimal installer for conda, a package manager, and environment management system. Follow the steps below to install Miniconda on your system using Homebrew:

1. Open a terminal.
2. Install Homebrew if you haven't already by running the following command:
   ```sh
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. Install Miniconda using Homebrew:
   ```sh
   brew install --cask miniconda
   ```
4. Initialize conda:
   ```sh
   conda init
   ```
5. Close and reopen your terminal.
6. Verify the installation by running:
   ```sh
   conda --version
   ```

### 2. Create and Activate a Conda Environment

1. Create a new conda environment with Python 3.8:
   ```sh
   conda create -n whisper_env python=3.8
   ```
2. Activate the environment:
   ```sh
   conda activate whisper_env
   ```

### 3. Install Required Packages

1. Navigate to the `py` directory:
   ```sh
   cd /Users/gusleonato/Personal/Whisper/py
   ```
2. Install the required packages using `pip`:
   ```sh
   pip install -r requirements.txt
   ```

Your environment is now set up and ready to use the Whisper on AWS framework.




s3 files to be deleted:
output/transcription-all.txt
output/chat_txt_output.txt

local file:
py/transcription_progress.json