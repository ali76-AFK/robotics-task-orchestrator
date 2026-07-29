#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float64MultiArray
from sensor_msgs.msg import Image


class VlaPolicy(Node):
    def __init__(self):
        super().__init__("vla_policy")

        self.latest_command = None
        self.have_image = False

        self.command_sub = self.create_subscription(
            String,
            "/vla_command_normalized",
            self.command_callback,
            10,
        )
        self.image_sub = self.create_subscription(
            Image,
            "/image_raw",
            self.image_callback,
            10,
        )

        self.arm_pub = self.create_publisher(Float64MultiArray, "/vla_arm_joint_goal", 10)
        self.gripper_pub = self.create_publisher(Float64MultiArray, "/vla_gripper_joint_goal", 10)

        self.get_logger().info("vla_policy ready")

    def image_callback(self, _msg: Image):
        self.have_image = True

    def command_callback(self, msg: String):
        self.latest_command = msg.data
        if not self.have_image:
            self.get_logger().warn("Command received, but no camera frame has arrived yet")
            return

        arm_goal = Float64MultiArray()
        gripper_goal = Float64MultiArray()

        cmd = self.latest_command

        if "home" in cmd or "reset" in cmd:
            arm_goal.data = [0.0, 0.0, 0.0]
            gripper_goal.data = [-0.7, 0.7]
        elif "pick" in cmd or "close" in cmd:
            arm_goal.data = [-1.14, -0.6, -0.07]
            gripper_goal.data = [0.0, 0.0]
        elif "sleep" in cmd or "rest" in cmd:
            arm_goal.data = [-1.57, 0.0, -0.9]
            gripper_goal.data = [0.0, 0.0]
        else:
            self.get_logger().warn(
                f'No policy mapping yet for command "{cmd}". Try: home, pick, sleep'
            )
            return

        self.arm_pub.publish(arm_goal)
        self.gripper_pub.publish(gripper_goal)
        self.get_logger().info(f'Published policy output for command "{cmd}"')


def main(args=None):
    rclpy.init(args=args)
    node = VlaPolicy()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
