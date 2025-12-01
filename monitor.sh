#!/bin/bash

echo "Monitoring experiment progress..."
echo "Press Ctrl+C to stop monitoring"
echo ""

while true; do
    clear
    python check_status.py
    sleep 10
done

