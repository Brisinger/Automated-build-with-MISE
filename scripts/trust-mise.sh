#!/usr/bin/env bash
# scripts/trust-mise.sh
# Run `mise trust` once for the current directory's `mise.toml` and record the action

set -euo pipefail

# Make the script itself executable so future runs can be invoked directly
SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/$(basename "${BASH_SOURCE[0]}")"
if [ ! -x "$SCRIPT_PATH" ]; then
  chmod +x "$SCRIPT_PATH" || true
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MARKER_FILE="$ROOT_DIR/.mise_trusted"

echo "Project root: $ROOT_DIR"

if [ -f "$MARKER_FILE" ]; then
  echo "mise.toml already trusted (marker present at $MARKER_FILE). Skipping."
  exit 0
fi

if ! command -v mise >/dev/null 2>&1; then
  echo "mise is not installed or not on PATH. Install or add mise to PATH and re-run this script." >&2
  exit 2
fi

echo "Running: mise trust"
if mise trust; then
  # Prepare marker contents: ISO8601 UTC timestamp and IP
  TIMESTAMP_UTC=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  # Try to obtain public IP (short timeout). Fall back to local interface addresses.
  PUBLIC_IP=""
  if command -v curl >/dev/null 2>&1; then
    PUBLIC_IP=$(curl -s --max-time 3 https://api.ipify.org || true)
    if [ -z "$PUBLIC_IP" ]; then
      PUBLIC_IP=$(curl -s --max-time 3 https://ifconfig.co || true)
    fi
  fi

  LOCAL_IP=""
  # macOS: try ipconfig, Linux: try hostname -I or ip
  if [ -z "$PUBLIC_IP" ]; then
    if command -v ip >/dev/null 2>&1; then
      LOCAL_IP=$(ip route get 1.1.1.1 2>/dev/null | awk '{for(i=1;i<=NF;i++) if($i=="src") print $(i+1)}' | head -n1 || true)
    fi
    if [ -z "$LOCAL_IP" ] && command -v hostname >/dev/null 2>&1; then
      # hostname -I is not available on macOS; try ipconfig on mac
      if command -v ipconfig >/dev/null 2>&1; then
        LOCAL_IP=$(ipconfig getifaddr en0 2>/dev/null || true)
      fi
      if [ -z "$LOCAL_IP" ]; then
        LOCAL_IP=$(hostname -I 2>/dev/null | awk '{print $1}' || true)
      fi
    fi
  fi

  # Choose which IP to log
  if [ -n "$PUBLIC_IP" ]; then
    CHOSEN_IP="$PUBLIC_IP"
  elif [ -n "$LOCAL_IP" ]; then
    CHOSEN_IP="$LOCAL_IP"
  else
    CHOSEN_IP="unknown"
  fi

  cat > "$MARKER_FILE" <<EOF
trusted: true
timestamp_utc: $TIMESTAMP_UTC
ip: $CHOSEN_IP
EOF

  echo "mise.toml trusted and marker created at $MARKER_FILE"
else
  echo "mise trust failed." >&2
  exit 3
fi

exit 0
