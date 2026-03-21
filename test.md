# RTAB-Map 测试

## 1. 启动

```bash
cd /home/wzy/ROS2/unitree-go2-ros2
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch go2_config sim_rtabmap.launch.py
```

正常现象：

- Gazebo 打开
- RViz 打开
- 机器人生成成功

## 2. 键盘控制

新开一个终端：

```bash
cd /home/wzy/ROS2/unitree-go2-ros2
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```


## 3. 导出 3D 点云

```bash
cd /home/wzy/ROS2/unitree-go2-ros2
source /opt/ros/humble/setup.bash
source install/setup.bash
python3 scripts/export_live_cloud_map.py --output /home/wzy/ROS2/unitree-go2-ros2/cloud_map/go2_live_cloud_map_final.ply
```

输出文件：

- `/home/wzy/ROS2/unitree-go2-ros2/cloud_map/go2_live_cloud_map_final.ply`

## 4. 导出 2D 地图

```bash
/home/wzy/ROS2/backup/third_party/rtabmap-0.23.4/build_export_x86/bin/rtabmap-export \
  --map \
  --opt 2 \
  --output go2_rtabmap_map_final \
  --output_dir /home/wzy/ROS2/unitree-go2-ros2/cloud_map \
  /home/wzy/.ros/go2_rtabmap_sim.db
```

输出文件：

- `/home/wzy/ROS2/unitree-go2-ros2/cloud_map/go2_rtabmap_map_final.pgm`
- `/home/wzy/ROS2/unitree-go2-ros2/cloud_map/go2_rtabmap_map_final.yaml`
