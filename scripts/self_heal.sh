#!/bin/bash

PROJECT_DIR="$HOME/self-healing-infrastructure"
LOG_FILE="$PROJECT_DIR/logs/health.log"
SERVICE_PORT=8080
APP_DIR="$PROJECT_DIR/app"

PROCESS_PATTERN="^python3 -m http.server ${SERVICE_PORT} --directory ${APP_DIR}$"

log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

if curl -fsS --max-time 3 "http://localhost:$SERVICE_PORT/" >/dev/null; then
    log_message "HEALTHY: Web service is responding."
    exit 0
fi

log_message "UNHEALTHY: Web service is not responding."
log_message "Attempting automatic recovery..."

if pgrep -f "$PROCESS_PATTERN" >/dev/null; then
    pkill -f "$PROCESS_PATTERN" || true
    sleep 2
fi

nohup python3 -m http.server "$SERVICE_PORT" \
    --directory "$APP_DIR" \
    > "$PROJECT_DIR/logs/service.log" 2>&1 < /dev/null &

sleep 2

if curl -fsS --max-time 3 "http://localhost:$SERVICE_PORT/" >/dev/null; then
    log_message "RECOVERY SUCCESS: Web service restarted."
else
    log_message "RECOVERY FAILED: Manual investigation required."
    exit 1
fi
