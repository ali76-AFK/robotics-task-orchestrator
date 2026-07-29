#!/usr/bin/env python3
import rclpy
import numpy as np
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from moveit.planning import MoveItPy
from moveit.core.robot_state import RobotState


class ExecutionBridge(Node):
    def __init__(self):
        super().__init__("execution_bridge")

        self.latest_arm_goal = None
        self.latest_gripper_goal = None

        self.arm_sub = self.create_subscription(
            Float64MultiArray,
            "/vla_arm_joint_goal",
            self.arm_callback,
            10,
        )
        self.gripper_sub = self.create_subscription(
            Float64MultiArray,
            "/vla_gripper_joint_goal",
            self.gripper_callback,
            10,
        )

        self.arduinobot = MoveItPy(node_name="moveit_py_execution")
        self.arm_component = self.arduinobot.get_planning_component("arm")
        self.gripper_component = self.arduinobot.get_planning_component("gripper")

        self.get_logger().info("execution_bridge ready")

    def arm_callback(self, msg: Float64MultiArray):
        self.latest_arm_goal = list(msg.data)
        self.try_execute()

    def gripper_callback(self, msg: Float64MultiArray):
        self.latest_gripper_goal = list(msg.data)
        self.try_execute()

    def try_execute(self):
        if self.latest_arm_goal is None or self.latest_gripper_goal is None:
            return

        if len(self.latest_arm_goal) != 3:
            self.get_logger().error("Arm goal must have 3 values")
            return
        if len(self.latest_gripper_goal) != 2:
            self.get_logger().error("Gripper goal must have 2 values")
            return

        arm_state = RobotState(self.arduinobot.get_robot_model())
        gripper_state = RobotState(self.arduinobot.get_robot_model())

        arm_state.set_joint_group_positions("arm", np.array(self.latest_arm_goal))
        gripper_state.set_joint_group_positions("gripper", np.array(self.latest_gripper_goal))

        self.arm_component.set_start_state_to_current_state()
        self.gripper_component.set_start_state_to_current_state()

        self.arm_component.set_goal_state(robot_state=arm_state)
        self.gripper_component.set_goal_state(robot_state=gripper_state)

        arm_plan = self.arm_component.plan()
        gripper_plan = self.gripper_component.plan()

        if arm_plan and gripper_plan:
            self.get_logger().info("Plans succeeded, executing arm and gripper goals")
            self.arduinobot.execute(arm_plan.trajectory, controllers=[])
            self.arduinobot.execute(gripper_plan.trajectory, controllers=[])
        else:
            self.get_logger().error("Planning failed for arm or gripper")


def main(args=None):
    rclpy.init(args=args)
    node = ExecutionBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
