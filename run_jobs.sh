#!/bin/bash

nohup python3 /Volumes/macOS-extravol/majinbo/job_manager.py run > /Volumes/macOS-extravol/majinbo/job_manager.log 2>&1 &
echo "Job manager running in background with nohup"
