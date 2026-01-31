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


### Robot-01 Stable Camera Streamer  

Optimized for Raspberry Pi 3B on Ubuntu 24.04 (Noble Numbat)  
This repository contains a high-stability MJPEG streaming server. It is specifically designed to bypass the buggy libcamera assertions found in Ubuntu 24.04 when running on older Raspberry Pi 3 hardware.

⚙️ Phase 1: Hardware & Firmware Configuration  
You must perform these steps first. The modern Ubuntu camera stack is unstable on Pi 3B; these steps switch the Pi to the "Legacy" driver which is rock-solid.

Open the boot configuration file:  

sudo nano /boot/firmware/config.txt  


Locate and modify these specific lines (or add them to the bottom):  

camera_auto_detect=0  
dtoverlay=vc4-fkms-v3d  
start_x=1  
gpu_mem=128  
Save (Ctrl+O, Enter) and Exit (Ctrl+X).  

Reboot the system:  

sudo reboot  


📦 Phase 2: Dependencies & Libraries  
Ubuntu 24.04 requires specific system-level libraries for Python to access the camera hardware without crashing.  

Run the following commands in order:  

# Update the package lists  
sudo apt update  

# Install OpenCV (The engine that captures the video)  
sudo apt install python3-opencv -y  

# Install Flask (The web server)  
sudo apt install python3-flask -y  

# Install Video4Linux tools (To manage the camera device)  
sudo apt install v4l-utils -y  
