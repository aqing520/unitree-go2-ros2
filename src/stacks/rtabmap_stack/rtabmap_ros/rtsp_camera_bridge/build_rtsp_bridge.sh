#!/bin/bash
# 编译 rtsp_camera_bridge 包
# 在 unitree-go2-ros2 外层工作空间下执行

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WS_ROOT="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"
cd "$WS_ROOT"

echo "Workspace: $WS_ROOT"
echo "Building rtsp_camera_bridge ..."

bash scripts/build_workspace_with_rtabmap.sh --packages-select rtsp_camera_bridge

echo "Build done. Source: source $WS_ROOT/install/setup.bash"
