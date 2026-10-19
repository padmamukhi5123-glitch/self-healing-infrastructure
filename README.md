# Self-Healing Infrastructure on AWS

## Project Overview
This project implements a lightweight self-healing mechanism on an AWS EC2 Ubuntu instance using Bash scripting, Python's HTTP server, and cron scheduling.

The system monitors a web service, detects service failures, attempts automatic recovery, and records health and recovery events in log files.

## Architecture
- **Cloud:** AWS EC2
- **Operating System:** Ubuntu 26.04 LTS
- **Automation:** Bash Shell scripting
- **Test Service:** Python HTTP server
- **Monitoring:** `curl` HTTP health checks
- **Scheduling:** Cron
- **Logging:** Linux log files

## Project Structure
```text
self-healing-infrastructure/
├── app/
│   └── index.html
├── logs/
│   ├── health.log
│   └── service.log
├── scripts/
│   ├── health_check.sh
│   └── self_heal.sh
└── README.md
```

## Features
- Checks web-service health using HTTP requests.
- Detects when the service becomes unavailable.
- Attempts to restart the service automatically.
- Runs scheduled health checks every minute using cron.
- Records health status and recovery attempts in logs.

## Verification
The project was tested by deliberately stopping the HTTP server.

The scheduled health check detected the failure, restarted the service, and recorded a successful recovery. A subsequent HTTP request returned the expected healthy response.

## Run the Project
1. Connect to an Ubuntu EC2 instance.
2. Install the required tools: `curl` and `procps`.
3. Start the test HTTP server on port 8080.
4. Run the self-healing script:

   `./scripts/self_heal.sh`

5. Schedule the script using cron:

   `* * * * * /home/ubuntu/self-healing-infrastructure/scripts/self_heal.sh`

## Learning Outcomes
- Linux administration on AWS EC2.
- Bash scripting and process management.
- Automated health checks and service recovery.
- Cron scheduling and log-based troubleshooting.

## Future Improvements
- Add recovery retry limits and alert notifications.
- Improve process identification and service management.
- Integrate CloudWatch monitoring and alarms.
