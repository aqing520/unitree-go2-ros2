# rtabmap_ros（中文说明）

本目录是当前工程使用的 `rtabmap_ros` 源码树，和 `go2_config` 的 launch /
config 一起组成 Go2 仿真 SLAM/Nav2 链路。

## 1. 本项目中的职责分层

- `RTAB-Map`：全局 SLAM、回环、重定位（发布 `map -> odom`）
- `robot_localization(EKF)`：本地连续里程计（发布 `odom -> base_footprint`）
- `Nav2`：规划、控制、避障

关键纪律：

- 只允许 RTAB-Map 发布 `map -> odom`
- `local_costmap=odom`，`global_costmap=map`

## 2. 目录说明

- `rtabmap_launch/`：RTAB-Map 主 launch
- `rtabmap_slam/`：SLAM 核心节点
- `rtabmap_odom/`：视觉/激光里程计
- `rtabmap_sync/`：多传感器同步
- `rtabmap_util/`：工具节点
- `rtabmap_msgs/`：消息定义
- `rtabmap_rviz_plugins/`：RViz 插件
- `rtabmap_examples/`：传感器样例
- `rtabmap_demos/`：机器人样例

## 3. 版本要求（重点）

本仓库当前已配置为：

- `find_package(RTABMap 0.23.4 REQUIRED)`

因此不要再使用系统默认的 `RTABMap 0.22.x`，请优先使用仓库内置的预编译核心：

- `vendor/rtabmap_stack/rtabmap-0.23.4/install`

## 4. 构建步骤

### 4.1 构建外层工作区

```bash
cd <unitree-go2-ros2>
bash scripts/build_workspace_with_rtabmap.sh
source install/setup.bash
```

这个构建入口会自动复用 `vendor/rtabmap_stack/rtabmap-0.23.4/install`，
不会重新编译 RTAB-Map 核心 C++。

## 5. 运行入口（本项目）

当前项目中常用的 RTAB-Map 入口是：

- `ros2 launch go2_config slam.launch.py slam_backend:=rtabmap`
- `ros2 launch go2_config sim_rtabmap.launch.py`

示例：

```bash
ros2 launch go2_config slam.launch.py slam_backend:=rtabmap sim:=true
ros2 launch go2_config sim_rtabmap.launch.py
```

## 6. 最小验收清单

```bash
ros2 node list
ros2 topic hz /odometry/local
ros2 topic hz /map
ros2 run tf2_ros tf2_echo map odom
ros2 run tf2_ros tf2_echo odom base_footprint
```

## 7. 常见问题

1. 报错找不到 `RTABMap 0.23.4`
先执行：`bash scripts/build_workspace_with_rtabmap.sh`，再 `source install/setup.bash`。

2. `cc1plus` 被 kill
是内存不足，降低并行度到 `-j2` 或增加 swap。

3. 只有 `CMake Warning (dev)`
是警告，不是失败根因；看最后 `Summary` 是否有 `Failed <<<`。

## 8. 上游参考

- RTAB-Map：<https://github.com/introlab/rtabmap>
- rtabmap_ros：<https://github.com/introlab/rtabmap_ros/tree/ros2>
- 历史文档：<http://wiki.ros.org/rtabmap_ros>
