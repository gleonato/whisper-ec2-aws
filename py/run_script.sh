#!/bin/bash

# Shell to run on ec2 instance
# This script will run the python script whisper_bulk_aws.py and log the output to output.log
nohup python /home/ec2-user/whisper-ec2-aws/py/whisper_bulk_aws.py > output.log 2>&1 &

# Print the process ID so you can monitor or kill it later
echo "Process started with PID $!"