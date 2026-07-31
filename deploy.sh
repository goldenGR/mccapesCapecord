#!/bin/bash

set -e

echo "======================================"
echo " CapeCord Bot Deployement"
echo "======================================"

CONTAINER="mccapescapecord-bot-1"
CONTAINER="mccapescapecord-bot-1"

if docker inspect "$CONTAINER" >/dev/null 2>&1; then
    STATUS=$(docker inspect -f '{{.State.Status}}' "$CONTAINER")

    START_TS=$(date -d "$(docker inspect -f '{{.State.StartedAt}}' "$CONTAINER")" +%s)
    NOW_TS=$(date +%s)

    UPTIME_SEC=$((NOW_TS - START_TS))

    DAYS=$((UPTIME_SEC / 86400))
    HOURS=$(((UPTIME_SEC % 86400) / 3600))
    MINS=$(((UPTIME_SEC % 3600) / 60))
    SECS=$((UPTIME_SEC % 60))

    UPTIME="${DAYS}d ${HOURS}h ${MINS}m ${SECS}s"

    read CPU MEM MEMP NETIO BLOCKIO PIDS <<<$(docker stats --no-stream \
        --format "{{.CPUPerc}} {{.MemUsage}} {{.MemPerc}} {{.NetIO}} {{.BlockIO}} {{.PIDs}}" \
        "$CONTAINER")

    echo ""
    echo "┌──────────────────────────────────────────────────────────────┐"
    printf "│ %-60s │\n" "Latest logs/info"
    echo "├──────────────────────────────────────────────────────────────┤"
    printf "│ %-20s %-39s │\n" "Container:" "$CONTAINER"
    printf "│ %-20s %-39s │\n" "Status:" "$STATUS"
    printf "│ %-20s %-39s │\n" "Uptime:" "$UPTIME"
    echo "├──────────────────────────────────────────────────────────────┤"
    printf "│ %-20s %-39s │\n" "CPU Usage:" "$CPU"
    printf "│ %-20s %-39s │\n" "Memory:" "$MEM ($MEMP)"
    printf "│ %-20s %-39s │\n" "Network I/O:" "$NETIO"
    printf "│ %-20s %-39s │\n" "Block I/O:" "$BLOCKIO"
    printf "│ %-20s %-39s │\n" "Processes:" "$PIDS"
    echo "└──────────────────────────────────────────────────────────────┘"
else
    echo ""
    echo "No existing container found. Skipping container info."
fi

echo "======================================"
echo " Updating MCCapes CapeCord Bot"
echo "======================================"

# Go to your project directory
cd ./mccapesCapecord/

echo ""
echo "Stopping running containers..."
sudo docker compose down

echo ""
echo "Pulling latest changes..."
git pull

echo ""
echo "Building Docker image..."
sudo docker build -t mccapescapecord-bot -f bot/Dockerfile ./bot

echo ""
echo "Available Docker images:"
sudo docker images

echo ""
echo "Starting containers..."
sudo docker compose up -d
echo ""
echo "======================================"
echo " Deployment complete!"
echo "======================================"