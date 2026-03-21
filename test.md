# Go2 Gazebo + RTAB-Map Test Guide

这份文档对应当前仓库里的仿真链路：

- Gazebo 作为仿真环境
- Go2 + Livox 仿真传感器
- RTAB-Map 作为 SLAM
- Nav2 作为导航
- `map_assembler` 在线发布 `/cloud_map`

## 1. 编译

在项目根目录执行：

```bash
cd /home/wzy/ROS2/unitree-go2-ros2
source /opt/ros/humble/setup.bash
bash scripts/build_workspace_with_rtabmap.sh --packages-up-to go2_config
source install/setup.bash
```

## 2. 启动整套系统

直接启动默认 outdoor 世界：

```bash
cd /home/wzy/ROS2/unitree-go2-ros2
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch go2_config sim_rtabmap.launch.py
```

当前默认会一起启动：

- Gazebo
- Go2
- RTAB-Map
- Nav2
- RViz
- `map_assembler`

如果你只想确认 `cloud_map` 这条链是否打开，可以单独检查：

```bash
ros2 topic list | grep cloud_map
```

正常应能看到：

```bash
/cloud_map
```

## 3. 键盘控制机器人

新开一个终端：

```bash
cd /home/wzy/ROS2/unitree-go2-ros2
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

常用按键：

- `i` 前进
- `,` 后退
- `j` 左转
- `l` 右转
- `k` 停止

建议先慢速绕场景走一圈，尽量覆盖想建图的区域。

## 4. 运行时检查

新开一个终端，检查系统状态：

```bash
cd /home/wzy/ROS2/unitree-go2-ros2
source /opt/ros/humble/setup.bash
source install/setup.bash

ros2 lifecycle get /controller_server
ros2 lifecycle get /planner_server
ros2 lifecycle get /bt_navigator
ros2 topic hz /livox_points
ros2 topic hz /odom
ros2 topic echo --once /mapGraph
```

通过标准：

- `controller_server`、`planner_server`、`bt_navigator` 都是 `active [3]`
- `/livox_points` 有频率
- `/odom` 有频率
- `/mapGraph` 能收到消息

## 5. 在 RViz 里看地图

RViz 中建议重点看这些显示项：

- `Livox Points`
- `Cloud Map`
- `MapCloud`
- `MapGraph`
- `TF`

注意：

- `Fixed Frame` 保持为 `map`
- `Cloud Map` 是 `map_assembler` 在线拼出来的全局点云
- `MapCloud` 是 RTAB-Map 插件基于 `/mapData` 的可视化
- 如果 `Occupancy Map` 勾上后显卡报 shader 错，可以先只看 `Cloud Map + MapGraph`

## 6. 导出 3D 点云地图

确认机器人已经跑过一段时间后，新开终端执行：

```bash
cd /home/wzy/ROS2/unitree-go2-ros2
source /opt/ros/humble/setup.bash
source install/setup.bash
python3 scripts/export_live_cloud_map.py
```

默认会把点云地图存到项目里的：

```bash
/home/wzy/ROS2/unitree-go2-ros2/cloud_map/go2_live_cloud_map_<timestamp>.ply
```

也可以显式指定输出绝对路径：

```bash
python3 scripts/export_live_cloud_map.py --output /home/wzy/ROS2/unitree-go2-ros2/cloud_map/outdoor_cloud_map.ply
```

如果脚本报超时，通常说明：

- 主系统还没完全起好
- `/cloud_map` 还没开始发布
- 机器人还没怎么移动，地图缓存还没初始化完成

可以先检查：

```bash
ros2 topic echo --once /cloud_map
```

## 7. 导出 2D 栅格地图

当前最稳的是直接从 RTAB-Map 数据库导出。

数据库默认在：

```bash
/home/wzy/.ros/go2_rtabmap_sim.db
```

对应的 `0.23.4` 导出工具在：

```bash
/home/wzy/ROS2/backup/third_party/rtabmap-0.23.4/build_export_x86/bin/rtabmap-export
```

导出命令：

```bash
/home/wzy/ROS2/backup/third_party/rtabmap-0.23.4/build_export_x86/bin/rtabmap-export \
  --map \
  --opt 2 \
  --output go2_rtabmap_map \
  --output_dir /home/wzy/ROS2/unitree-go2-ros2/cloud_map \
  /home/wzy/.ros/go2_rtabmap_sim.db
```

导出后会得到：

- `/home/wzy/ROS2/unitree-go2-ros2/cloud_map/go2_rtabmap_map.pgm`
- `/home/wzy/ROS2/unitree-go2-ros2/cloud_map/go2_rtabmap_map.yaml`

## 8. 离线导出脚本说明

仓库里已有一个离线脚本：

```bash
scripts/export_rtabmap_cloud_map.sh
```

它会优先查找刚编好的 `0.23.4` `rtabmap-export`，避免误用系统自带的 `0.22.1`。

不过要注意：

- 这个脚本走的是“数据库离线拼云”路线
- 如果数据库里没有完整保存可离线重建的 scan cloud，导出的 `PLY` 仍然可能为空
- 这也是为什么当前更推荐用 `map_assembler + /cloud_map + export_live_cloud_map.py` 这条在线导出链

## 9. 最小验收标准

这套链路跑通时，至少要满足：

- `ros2 launch go2_config sim_rtabmap.launch.py` 能完整启动
- Gazebo 里机器人正常生成
- RViz 能看到 `Cloud Map` 或 `MapCloud`
- 机器人移动后地图持续增长
- `python3 scripts/export_live_cloud_map.py` 能导出项目内的 `PLY`
- `rtabmap-export --map --opt 2 ...` 能导出 `pgm + yaml`
