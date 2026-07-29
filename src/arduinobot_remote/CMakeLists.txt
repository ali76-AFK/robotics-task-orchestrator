cmake_minimum_required(VERSION 3.8)
project(arduinobot_remote)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)

ament_python_install_package(${PROJECT_NAME})

install(
  DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

install(PROGRAMS
  ${PROJECT_NAME}/command_interface.py
  ${PROJECT_NAME}/vision_bridge.py
  ${PROJECT_NAME}/vla_policy.py
  ${PROJECT_NAME}/execution_bridge.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
