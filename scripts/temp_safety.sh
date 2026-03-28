#!/bin/bash
# ==========================================
# Pi Temperature Safety Monitor
# - Alert at 80°C
# - Auto-shutdown at 85°C
# ==========================================

TEMP=$(vcgencmd measure_temp | grep -oP '\d+\.\d+')
TEMP_INT=${TEMP%.*}

LOG_FILE="/home/pi4eiei/tutoring-company/logs/temp_safety.log"
mkdir -p "$(dirname $LOG_FILE)"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Temp: ${TEMP}°C" >> $LOG_FILE

# Thresholds
WARN_TEMP=65
CRITICAL_TEMP=70
SHUTDOWN_TEMP=70

if [ "$TEMP_INT" -ge $CRITICAL_TEMP ]; then
    echo "🚨 CRITICAL: Temperature is ${TEMP}°C - Shutting down NOW!" >> $LOG_FILE
    echo "🚨 Pi is overheating! Shutting down at ${TEMP}°C"
    
    # Send notification before shutdown
    # Could add Telegram/Line notification here
    
    # Shutdown
    sudo shutdown -h now
elif [ "$TEMP_INT" -ge $WARN_TEMP ]; then
    echo "⚠️ WARNING: Temperature is ${TEMP}°C" >> $LOG_FILE
    echo "⚠️ อุณหภูมิสูง: ${TEMP}°C"
elif [ "$TEMP_INT" -ge $SHUTDOWN_TEMP ]; then
    echo "🔴 ALERT: Temperature is ${TEMP}°C (will shutdown at ${CRITICAL_TEMP}°C)" >> $LOG_FILE
fi
