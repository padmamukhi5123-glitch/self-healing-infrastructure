#!/bin/bash

PROJECT_DIR="$HOME/self-healing-infrastructure"
LOG_FILE="$PROJECT_DIR/logs/health.log"

log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

log_message "Self-healing health check script started."
log_message "System hostname: $(hostname)"
log_message "Memory status: $(free -h | awk '/Mem:/ {print $3 " used / " $2 " total"}')"
log_message "Health check completed."
