#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math

class AckermannPhasedTrajectory(Node):
    def __init__(self):
        super().__init__('ackermann_phased_trajectory')
        
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer_period = 0.05  # 20 Hz
        self.timer = self.create_timer(self.timer_period, self.timer_callback)
        
        self.time_elapsed = 0.0

        # Parameters by Phase
        # Phase 1: Straight entry (0 to 5 s)
        # Phase 2: Wide left turn (5 to 15 s)
        # Phase 3: Figure-eight (15 to 45 s)
        # Phase 4: Exit section and braking (45 to 50 s)
        
        self.get_logger().info('Controlador de Trayectoria Compuesta por Fases Iniciado.')

    def timer_callback(self):
        msg = Twist()
        t = self.time_elapsed

        if t < 5.0:
            # PHASE 1: Initial straight section with gentle acceleration
            ramp = min(1.0, t / 1.5)
            msg.linear.x = 0.30 * ramp
            msg.angular.z = 0.0
            phase_name = "Fase 1: Recta inicial"

        elif 5.0 <= t < 15.0:
            # PHASE 2: Wide, constant-radius left-hand curve
            msg.linear.x = 0.28
            msg.angular.z = 0.35
            phase_name = "Fase 2: Curva abierta"

        elif 15.0 <= t < 45.0:
            # PHASE 3: Figure-8 (lemniscate) with compensation
            t_8 = t - 15.0
            period_8 = 30.0
            max_w = 0.45
            
            target_w = max_w * math.sin(2.0 * math.pi * t_8 / period_8)
            
            # Compensation if one direction rotates less than the other
            left_gain = 1.10
            right_gain = 1.00
            if target_w > 0.0:
                target_w *= left_gain
            else:
                target_w *= right_gain

            msg.linear.x = 0.25
            msg.angular.z = target_w
            phase_name = "Fase 3: Figura en 8"

        elif 45.0 <= t < 50.0:
            # PHASE 4: Straight deceleration and braking section
            t_brake = 50.0 - t
            msg.linear.x = 0.25 * (t_brake / 5.0)
            msg.angular.z = 0.0
            phase_name = "Fase 4: Frenado suave"

        else:
            # FINAL: Robot completely stopped
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            phase_name = "Finalizado"

        self.publisher_.publish(msg)
        self.get_logger().info(f'[{phase_name}] t={t:.1f}s | v={msg.linear.x:.2f} m/s | w={msg.angular.z:.2f} rad/s', throttle_duration_sec=2.0)
        
        self.time_elapsed += self.timer_period

def main(args=None):
    rclpy.init(args=args)
    node = AckermannPhasedTrajectory()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        stop_msg = Twist()
        node.publisher_.publish(stop_msg)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
