#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class CommandInterface(Node):
    def __init__(self):
        super().__init__("command_interface")
        self.latest_command = ""
        self.subscription = self.create_subscription(
            String,
            "/vla_command",
            self.command_callback,
            10,
        )
        self.publisher = self.create_publisher(String, "/vla_command_normalized", 10)
        self.get_logger().info("command_interface ready, listening on /vla_command")

    def command_callback(self, msg: String):
        text = msg.data.strip()
        if not text:
            self.get_logger().warn("Received empty command, ignoring")
            return
        normalized = " ".join(text.lower().split())
        self.latest_command = normalized
        out = String()
        out.data = normalized
        self.publisher.publish(out)
        self.get_logger().info(f'Normalized command: "{normalized}"')


def main(args=None):
    rclpy.init(args=args)
    node = CommandInterface()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
