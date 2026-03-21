cmake_minimum_required(VERSION 3.8)
project(rtabmap_stack_env)

find_package(ament_cmake REQUIRED)

ament_environment_hooks(
  "${CMAKE_CURRENT_SOURCE_DIR}/environment/rtabmap_stack_env.sh"
)

ament_package()
