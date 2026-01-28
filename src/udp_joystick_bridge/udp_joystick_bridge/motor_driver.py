import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import RPi.GPIO as GPIO

# === CHANGE THESE TO MATCH YOUR WIRING ===
LEFT_PWM_PIN  = 12   # GPIO pin for left motor PWM
LEFT_DIR_PIN  = 13   # GPIO pin for left motor direction
RIGHT_PWM_PIN = 18   # GPIO pin for right motor PWM
RIGHT_DIR_PIN = 19   # GPIO pin for right motor direction

WHEEL_BASE = 0.20    # distance between wheels in meters (measure your robot)
MAX_DUTY   = 100     # max PWM duty cycle (usually 100 for software PWM)

class MotorDriver(Node):
    def __init__(self):
        super().__init__('motor_driver')
        self.subscription = self.create_subscription(
            Twist, '/cmd_vel', self.cmd_vel_callback, 10)

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        for pin in [LEFT_PWM_PIN, LEFT_DIR_PIN, RIGHT_PWM_PIN, RIGHT_DIR_PIN]:
            GPIO.setup(pin, GPIO.OUT)

        self.left_pwm = GPIO.PWM(LEFT_PWM_PIN, 1000)   # 1 kHz PWM
        self.right_pwm = GPIO.PWM(RIGHT_PWM_PIN, 1000)
        self.left_pwm.start(0)
        self.right_pwm.start(0)

        self.get_logger().info("Motor driver node started - listening to /cmd_vel")

    def cmd_vel_callback(self, msg):
        linear = msg.linear.x
        angular = msg.angular.z

        # Differential drive inverse kinematics
        left_speed  = linear - angular * WHEEL_BASE / 2.0
        right_speed = linear + angular * WHEEL_BASE / 2.0

        # Scale to duty cycle (-100 .. 100)
        left_duty  = max(min(left_speed * MAX_DUTY, MAX_DUTY), -MAX_DUTY)
        right_duty = max(min(right_speed * MAX_DUTY, MAX_DUTY), -MAX_DUTY)

        # Set direction pins (assuming HIGH = forward)
        GPIO.output(LEFT_DIR_PIN,  left_duty  >= 0)
        GPIO.output(RIGHT_DIR_PIN, right_duty >= 0)

        # Set PWM
        self.left_pwm.ChangeDutyCycle(abs(left_duty))
        self.right_pwm.ChangeDutyCycle(abs(right_duty))

        # Optional: log for debugging
        # self.get_logger().info(f"L: {left_duty:.1f}%, R: {right_duty:.1f}%")

    def destroy_node(self):
        self.left_pwm.stop()
        self.right_pwm.stop()
        GPIO.cleanup()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = MotorDriver()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
