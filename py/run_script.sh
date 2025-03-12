#!/bin/bash

# Set log file with timestamp
LOG_FILE="/home/ec2-user/whisper-ec2-aws/log/whisper_output_$(date +%Y%m%d_%H%M%S).log"
SCRIPT_PATH="/home/ec2-user/whisper-ec2-aws/py/run_whisper_bulk_aws.py"

echo "Starting Whisper transcription process..."
echo "Logs will be written to: $LOG_FILE"

# Activate conda environment if needed
# source /home/ec2-user/miniconda3/bin/activate whisper_env

# Run the script in the background with proper output redirection
nohup python $SCRIPT_PATH > $LOG_FILE 2>&1 &

# Save the process ID
PID=$!
echo $PID > /home/ec2-user/whisper_pid.txt

echo "Process started with PID $PID"
echo "To monitor the logs in real-time, run: tail -f $LOG_FILE"
echo "To stop the process, run: kill $PID"