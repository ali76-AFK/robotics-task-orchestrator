#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo


class VisionBridge(Node):
    def __init__(self):
        super().__init__("vision_bridge")
        self.last_image_stamp = None
        self.last_camera_info_stamp = None

        self.image_sub = self.create_subscription(
            Image,
            "/image_raw",
            self.image_callback,
            10,
        )
        self.camera_info_sub = self.create_subscription(
            CameraInfo,
            "/camera_info",
            self.camera_info_callback,
            10,
        )

        self.timer = self.create_timer(2.0, self.timer_callback)
        self.get_logger().info("vision_bridge subscribed to /image_raw and /camera_info")

    def image_callback(self, msg: Image):
        self.last_image_stamp = msg.header.stamp

    def camera_info_callback(self, msg: CameraInfo):
        self.last_camera_info_stamp = msg.header.stamp

    def timer_callback(self):
        image_ok = self.last_image_stamp is not None
        info_ok = self.last_camera_info_stamp is not None
        self.get_logger().info(
            f"camera status: image_raw={'yes' if image_ok else 'no'}, camera_info={'yes' if info_ok else 'no'}"
        )


def main(args=None):
    rclpy.init(args=args)
    node = VisionBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
