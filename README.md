# Robot-01 – Teleoperated Robot with ESP32 + ROS 2 Jazzy

Simple differential drive robot controlled via joystick over WiFi.

## Components
- ESP32-C3 (Lolin Mini) reads analog joystick → sends UDP packets
- Raspberry Pi 3B running ROS 2 Jazzy:
  - `udp_listener.py`: receives UDP → publishes `/cmd_vel` (Twist)
  - `motor_driver.py`: subscribes to `/cmd_vel` → drives motors via GPIO

## Setup
1. Source ROS 2: `source /opt/ros/jazzy/setup.bash`
2. Build workspace: `colcon build`
3. Source it: `source install/setup.bash`
4. Run nodes:
   - `ros2 run udp_joystick_bridge udp_listener`
   - `ros2 run udp_joystick_bridge motor_driver`

## Hardware
- Joystick → ESP32 GPIO 3 (X), 4 (Y)
- Motors → Pi GPIO (PWM + DIR pins – see motor_driver.py)

Work in progress 🚧

## Firmware (ESP32 side)

Located in `firmware/esp32_joystick_sender/`

- Reads analog joystick (X=GPIO3, Y=GPIO4)
- Sends JSON UDP packets to Pi IP:port 3333
- Arduino IDE sketch: `esp32_joystick_sender.ino`

### Upload instructions
1. Open in Arduino IDE
2. Select board: Lolin C3 Mini (or ESP32-C3 Dev Module)
3. Set partition scheme, upload speed, etc.
4. Upload!
