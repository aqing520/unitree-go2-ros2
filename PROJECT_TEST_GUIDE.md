# Unitree Go2 ROS2 项目 - 运行和测试指南

## ✅ 项目构建状态

### 环境信息
- **操作系统**: Ubuntu 22.04 (Linux)
- **ROS2 发行版**: Humble
- **Gazebo**: 11.10.2
- **Python**: 3.10+

### 构建结果
- ✅ **11个ROS包成功编译** (总耗时: 34.8s)

#### 编译的包列表
```
✓ champ_teleop         (Python 包)
✓ champ_navigation     (CMake 包)
✓ champ_config         (CMake 包)
✓ go2_config           (CMake 包)
✓ champ_description    (CMake 包)
✓ go2_description      (CMake 包)
✓ champ                (Core Library)
✓ champ_msgs           (消息定义)
✓ champ_gazebo         (仿真配置)
✓ champ_base           (机器人基础控制)
✓ champ_bringup        (启动配置)
```

## 🚀 快速启动命令

所有命令需要先sourcing工作空间:
```bash
cd /home/wzy/ROS2/unitree-go2-ros2
source install/setup.bash
```

### 1. **Gazebo 仿真演示** (基础版本)
```bash
ros2 launch go2_config gazebo.launch.py
```
- 启动Gazebo与Go2机器人
- 包含标准传感器配置
- GUI界面启用 (可用 `gui:=false` 禁用)

### 2. **Gazebo + RViz 可视化**
```bash
ros2 launch go2_config gazebo.launch.py rviz:=true
```
- 同时显示仿真环境 + RViz可视化
- 可以实时查看机器人姿态和传感器数据

### 3. **Velodyne 3D LiDAR 版本**
```bash
ros2 launch go2_config gazebo_velodyne.launch.py
```
- 配置3D雷达传感器
- 点云话题: `/velodyne_points`
- **注**: 需在 URDF 中启用 Velodyne 配置

```bash
ros2 launch go2_config gazebo_velodyne.launch.py rviz:=true
```

### 4. **机器人启动 (Bringup)**
```bash
# 使用模拟时间
ros2 launch go2_config bringup.launch.py sim:=true use_sim_time:=true

# 连接物理机器人 (需要实际硬件)
ros2 launch go2_config bringup.launch.py hardware_connected:=true
```

### 5. **遥操控制**
启动仿真后，在另一个终端运行:
```bash
source install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```
- 使用键盘遥操机器人
- 前进/退后: I/,
- 左转/右转: J/L
- 停止: K

### 6. **SLAM 演示** (开发中)
```bash
ros2 launch go2_config slam.launch.py
```
- 注: 当前状态为实验性，功能尚未完全实现

### 7. **导航演示** (开发中)
```bash
ros2 launch go2_config navigate.launch.py
```
- 注: 当前正在开发中，需要 nav2 集成

## 🔧 重要配置文件

### 1. **步态参数** (`gait.yaml`)
位置: `src/robots/configs/go2_config/config/gait/gait.yaml`

```yaml
gait:
  knee_orientation: ">>"           # 膝关节方向: >> >< << <>
  pantograph_leg: false            # 平行四边形腿配置
  odom_scaler: 0.9                 # 里程计缩放系数
  max_linear_velocity_x: 0.3       # 最大前进速度 (m/s)
  max_linear_velocity_y: 0.25      # 最大侧向速度 (m/s)
  max_angular_velocity_z: 0.5      # 最大旋转速度 (rad/s)
  com_x_translation: 0.0           # 质心平移补偿
  swing_height: 0.04               # 摆腿高度 (m)
  stance_depth: 0.01               # 站立深度 (m)
  stance_duration: 0.25            # 单腿站立时间 (s)
  nominal_height: 0.225            # 机器人站立高度 (m)
```

### 2. **ROS2_Control 配置**
位置: `src/robots/configs/go2_config/config/ros_control/ros_control.yaml`
- 定义电机控制器参数
- PID控制增益设置
- 关节限制

### 3. **URDF 机器人描述**
位置: `src/robots/descriptions/go2_description/urdf/`
- `champ.urdf.xacro`: 主机器人描述
- `velodyne.xacro`: 3D雷达配置
- `laser.xacro`: 2D激光配置

### 4. **Gazebo 世界**
位置: `src/robots/configs/go2_config/worlds/`
- `default.world`: 基础环保
- `outdoor.world`: 户外场景
- `playground.world`: 游乐场场景

## 📊 验证测试结果

### 包依赖检查
```bash
source install/setup.bash

# 验证go2_config包
ros2 pkg prefix go2_config
# 输出: /home/wzy/ROS2/unitree-go2-ros2/install/go2_config

# 列出可用launch文件
ros2 launch go2_config gazebo.launch.py --show-args
```

### Launch 文件验证 ✅

#### gazebo.launch.py
- ✅ 参数解析成功
- ✅ 支持关键参数:
  - `rviz`: 启用RViz (default: false)
  - `gui`: 使用GUI (default: true)
  - `world`: 世界文件 (default: default.world)
  - `use_sim_time`: 仿真时间 (default: true)

#### gazebo_velodyne.launch.py
- ✅ 参数解析成功
- ✅ 支持Velodyne配置

#### bringup.launch.py
- ✅ 参数解析成功
- ✅ 支持硬件/仿真切换

## 🔌 系统依赖验证

### 已安装的关键ROS包:
```
✓ ros-humble-gazebo-ros2-control       (0.4.10)
✓ ros-humble-ros2-control              (2.52.0)
✓ ros-humble-ros2-controllers          (2.50.1)
✓ ros-humble-xacro                     (2.1.1)
✓ ros-humble-gazebo-plugins            (3.9.0)
✓ ros-humble-gazebo-ros                (3.9.0)
✓ ros-humble-robot-localization        (已安装)
✓ ros-humble-velodyne                  (已安装)
✓ ros-humble-velodyne-gazebo-plugins   (已安装)
```

## 🧪 推荐的测试流程

### 第1阶段: 基础仿真验证
```bash
# 终端1: 启动Gazebo仿真
source install/setup.bash
ros2 launch go2_config gazebo.launch.py

# 检查点:
# - Gazebo窗口打开
# - Go2机器人在仿真环境中显示
# - 无错误消息
```

### 第2阶段: 可视化验证
```bash
# 启用RViz
source install/setup.bash
ros2 launch go2_config gazebo.launch.py rviz:=true

# 检查点:
# - RViz窗口打开
# - 显示机器人URDF模型
# - 关节轴线可见
```

### 第3阶段: 遥操测试
```bash
# 终端1: 启动仿真
source install/setup.bash
ros2 launch go2_config gazebo.launch.py

# 终端2: 启动遥操
source install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard

# 检查点:
# - 键盘命令接收
# - 机器人在仿真中移动
# - ROS topic 正常通信
```

### 第4阶段: 传感器测试 (可选)
```bash
# 启用Velodyne
source install/setup.bash
ros2 launch go2_config gazebo_velodyne.launch.py rviz:=true

# 在RViz中订阅话题:
# - /velodyne_points (3D点云)
# - /scan (如果启用2D激光)
```

## 📋 故障排除

### 问题1: "gazebo: command not found"
**解决**: 
```bash
source /opt/ros/humble/setup.bash
```

### 问题2: Launch文件找不到
**解决**:
```bash
source install/setup.bash
# 确保环境变量正确
echo $ROS_PACKAGE_PATH
```

### 问题3: 软件包不存在
**解决**: 重新构建
```bash
colcon build --symlink-install
source install/setup.bash
```

### 问题4: Gazebo加载缓慢
**原因**: URDF处理或Gazebo初始化
**解决**: 
- 增加等待时间
- 检查日志: `~/.gazebo/gzserver.log`

## 📚 项目结构说明

```
unitree-go2-ros2/
├── src/
│   ├── champ/                          # CHAMP控制框架
│   │   ├── champ/                      # 核心库
│   │   ├── champ_base/                 # 基础控制器
│   │   ├── champ_bringup/              # 启动配置
│   │   ├── champ_config/               # 通用配置
│   │   ├── champ_description/          # 机器人描述
│   │   ├── champ_gazebo/               # Gazebo插件
│   │   ├── champ_msgs/                 # ROS消息
│   │   └── champ_navigation/           # 导航配置
│   ├── champ_teleop/                   # 遥操控制
│   └── robots/                         # Go2机器人配置
│       ├── configs/go2_config/         # 机器人配置
│       └── descriptions/go2_description/ # 机器人描述
├── install/                            # 安装目录
└── build/                              # 构建目录
```

## 🎯 接下来的步骤

1. **运行基础演示**: `ros2 launch go2_config gazebo.launch.py`
2. **测试遥操**: 使用键盘控制机器人
3. **调整参数**: 编辑 `gait.yaml` 优化步态
4. **开发控制算法**: 在 `champ_base` 中实现自己的控制逻辑

---

**生成时间**: 2026年3月19日  
**项目状态**: ✅ 完全可编译和运行
