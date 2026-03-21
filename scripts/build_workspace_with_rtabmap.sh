#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROS_SETUP="/opt/ros/humble/setup.bash"

if [[ ! -f "$ROS_SETUP" ]]; then
  echo "[ERROR] ROS 2 Humble setup script not found: $ROS_SETUP" >&2
  exit 1
fi

# ROS setup scripts may reference unset variables.
set +u
# shellcheck disable=SC1090
source "$ROS_SETUP"
set -u
# shellcheck disable=SC1091
source "$ROOT_DIR/scripts/use_rtabmap_prebuilt_env.sh"

cd "$ROOT_DIR"
colcon build --symlink-install "$@"

echo "[DONE] Workspace build finished."
echo "[NEXT] source \"$ROOT_DIR/install/setup.bash\""
