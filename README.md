# Job Manager

A simple job management system to handle job queues with priorities, implemented in Python.

## Features

- Add jobs to a queue with priority
- Check the status of jobs
- Execute jobs in the queue based on priority
- Persist job states across restarts
- Run jobs in the background using `nohup` and `screen`

## Usage

### Adding a Job

```sh
python3 job_manager.py add "your_command_here" [priority]
```

### Checking Job Status

```sh
python3 job_manager.py status job_id
```

### Running Jobs

```sh
./run_jobs.sh
```

### Example

```sh
# Add a job with priority 10
python3 job_manager.py add "echo 'Hello, High Priority World!'" 10

# Check the status of the job
python3 job_manager.py status 1

# Run the job manager to process the queue
./run_jobs.sh
```

### Requirements

- Python 3.x
- `screen` and `nohup` installed

### Error Handling

- Errors are logged in the `context.txt` file.
- Jobs that fail are marked as `failed` and their status is persisted.

### License

This project is licensed under the MIT License.
