#!/bin/bash

# Shell to run on ec2 instance
# This script will run the python script whisper_bulk_aws2.py and log the output to output.log
python /home/ec2-user/whisper-ec2-aws/py/whisper_bulk_aws2.py > output.log 2>&1