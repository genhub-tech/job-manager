import os
import csv
import subprocess
from time import sleep
import json

QUEUE_FILE = '/Volumes/macOS-extravol/majinbo/job_queue.txt'
CONTEXT_FILE = '/Volumes/macOS-extravol/majinbo/context.txt'
STATE_FILE = '/Volumes/macOS-extravol/majinbo/job_state.json'

# Function to add a job to the queue with priority
def add_job(command, priority=1):
    job_id = get_next_job_id()
    with open(QUEUE_FILE, 'a') as f:
        writer = csv.writer(f)
        writer.writerow([job_id, command, 'queued', priority])
    update_context(f'Job {job_id} added to the queue with command: {command} and priority: {priority}')
    return job_id

# Function to get the next job ID
def get_next_job_id():
    if not os.path.exists(QUEUE_FILE):
        return 1
    with open(QUEUE_FILE, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)
        if len(rows) <= 1:
            return 1
        last_id = int(rows[-1][0])
        return last_id + 1

# Function to check the status of a job
def check_job_status(job_id):
    if not os.path.exists(QUEUE_FILE):
        return 'Job not found'
    with open(QUEUE_FILE, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == str(job_id):
                return row[2]
    return 'Job not found'

# Function to execute jobs in the queue based on priority
def execute_jobs():
    restore_state()
    while True:
        stop_existing_jobs()
        with open(QUEUE_FILE, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
        if len(rows) <= 1:
            sleep(2)
            continue
        valid_rows = [row for row in rows[1:] if len(row) == 4]  # Ensure row has the expected length
        if not valid_rows:
            sleep(2)
            continue
        valid_rows = sorted(valid_rows, key=lambda x: int(x[3]), reverse=True)  # Sort by priority
        for row in valid_rows:
            job_id, command, status, priority = row
            if status == 'queued':
                if is_job_running(command):
                    continue
                update_job_status(job_id, 'running')
                save_state(job_id, 'running')
                try:
                    subprocess.Popen(f'screen -dmS job_{job_id} bash -c "{command}" && echo {job_id} completed', shell=True)
                    sleep(2)
                    update_job_status(job_id, 'completed')
                    save_state(job_id, 'completed')
                    update_context(f'Job {job_id} with command "{command}" has been completed')
                except Exception as e:
                    update_context(f'Error executing job {job_id} with command "{command}": {e}')
                    update_job_status(job_id, 'failed')
                    save_state(job_id, 'failed')
        sleep(2)

# Function to check if a job with the same command is already running
def is_job_running(command):
    result = subprocess.run(['pgrep', '-f', command], stdout=subprocess.PIPE)
    return result.returncode == 0

# Function to stop existing jobs
def stop_existing_jobs():
    subprocess.run(['pkill', '-f', 'job_manager.py run'])
    update_context('Stopped existing job_manager.py run processes')

# Function to update the status of a job
def update_job_status(job_id, status):
    with open(QUEUE_FILE, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)
    with open(QUEUE_FILE, 'w') as f:
        writer = csv.writer(f)
        for row in rows:
            if len(row) == 4 and row[0] == str(job_id):  # Ensure row has the expected length
                row[2] = status
            writer.writerow(row)

# Function to update the context file
def update_context(message):
    with open(CONTEXT_FILE, 'a') as f:
        f.write(f'CONTEXT: {message}\n')

# Function to save the state of jobs
def save_state(job_id, status):
    state = {}
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
    state[job_id] = status
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

# Function to restore the state of jobs
def restore_state():
    if not os.path.exists(STATE_FILE):
        return
    with open(STATE_FILE, 'r') as f:
        state = json.load(f)
    with open(QUEUE_FILE, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)
    with open(QUEUE_FILE, 'w') as f:
        writer = csv.writer(f)
        for row in rows:
            if len(row) == 4 and row[0] in state:  # Ensure row has the expected length
                row[2] = state[row[0]]
            writer.writerow(row)

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: python job_manager.py <add|status|run> [args...]')
        sys.exit(1)
    command = sys.argv[1]
    if command == 'add' and len(sys.argv) >= 3:
        job_command = sys.argv[2]
        priority = int(sys.argv[3]) if len(sys.argv) == 4 else 1
        job_id = add_job(job_command, priority)
        print(f'Job {job_id} added to the queue with priority {priority}')
    elif command == 'status' and len(sys.argv) == 3:
        job_id = int(sys.argv[2])
        status = check_job_status(job_id)
        print(f'Job {job_id} status: {status}')
    elif command == 'run':
        execute_jobs()
    else:
        print('Invalid command or arguments')
        sys.exit(1)
