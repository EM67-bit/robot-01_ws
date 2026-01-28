import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import socket
import json

class UDPListener(Node):
    def __init__(self):
        super().__init__('udp_listener')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind(('', 3333))  # Bind to port 3333 on all interfaces
        self.get_logger().info('UDP listener started on port 3333')
        self.timer = self.create_timer(0.01, self.listen_udp)  # Check every 10ms

    def listen_udp(self):
        try:
            data, addr = self.udp_socket.recvfrom(1024)  # Non-blocking? For simplicity, assume single-thread
            decoded = data.decode('utf-8')
            values = json.loads(decoded)
            twist = Twist()
            twist.linear.x = values['lin']
            twist.angular.z = values['ang']
            self.publisher_.publish(twist)
            self.get_logger().info(f'Published Twist: lin={twist.linear.x}, ang={twist.angular.z}')
        except socket.error:
            pass  # No data, skip
        except Exception as e:
            self.get_logger().error(f'Error: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = UDPListener()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
