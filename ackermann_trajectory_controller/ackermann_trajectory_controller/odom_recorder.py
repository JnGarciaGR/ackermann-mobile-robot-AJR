#!/usr/bin/env python3
import csv
import math
import rclpy
from nav_msgs.msg import Odometry
from rclpy.node import Node


def yaw_from_quaternion(q):
  siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
  cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
  return math.atan2(siny_cosp, cosy_cosp)


class OdomRecorder(Node):

  def __init__(self):
    super().__init__('odom_recorder')
    self.sub = self.create_subscription(
        Odometry, '/odom', self.odom_callback, 10
    )

    self.file = open('odom_data.csv', 'w', newline='')
    self.writer = csv.writer(self.file)
    self.writer.writerow([
        'timestamp',
        'x_odom',
        'y_odom',
        'yaw_odom',
        'v_odom',
        'w_odom',
    ])

    self.start_time = None
    self.get_logger().info('Registrador de Odometría iniciado. Guardando en odom_data.csv...')

  def odom_callback(self, msg: Odometry):
    curr_time = (
        msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
    )
    if self.start_time is None:
      self.start_time = curr_time

    t = curr_time - self.start_time

    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y
    yaw = yaw_from_quaternion(msg.pose.pose.orientation)

    v = msg.twist.twist.linear.x
    w = msg.twist.twist.angular.z

    self.writer.writerow([t, x, y, yaw, v, w])

  def destroy_node(self):
    self.file.close()
    super().destroy_node()


def main(args=None):
  rclpy.init(args=args)
  node = OdomRecorder()
  try:
    rclpy.spin(node)
  except KeyboardInterrupt:
    pass
  finally:
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
  main()
