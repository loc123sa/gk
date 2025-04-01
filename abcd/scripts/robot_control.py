#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import sys
import select
import termios
import tty

# Hướng dẫn sử dụng
msg = """
Điều khiển robot 4 bánh:
------------------------
w : Tiến lên
s : Lùi lại
a : Rẽ trái
d : Rẽ phải
x : Dừng lại
q : Thoát

Nhấn phím để điều khiển!
"""

# Hàm để lấy phím nhấn từ bàn phím
def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

# Hàm chính
if __name__ == "__main__":
    # Lưu cài đặt terminal
    settings = termios.tcgetattr(sys.stdin)

    # Khởi tạo node ROS
    rospy.init_node('robot_teleop', anonymous=True)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)  # 10 Hz

    # Biến Twist để gửi lệnh vận tốc
    twist = Twist()
    linear_speed = 0.5   # Tốc độ tuyến tính (m/s)
    angular_speed = 1.0  # Tốc độ góc (rad/s)

    print(msg)

    try:
        while not rospy.is_shutdown():
            key = getKey()

            # Điều khiển dựa trên phím nhấn
            if key == 'w':  # Tiến lên
                twist.linear.x = linear_speed
                twist.angular.z = 0.0
            elif key == 's':  # Lùi lại
                twist.linear.x = -linear_speed
                twist.angular.z = 0.0
            elif key == 'a':  # Rẽ trái
                twist.linear.x = 0.0
                twist.angular.z = angular_speed
            elif key == 'd':  # Rẽ phải
                twist.linear.x = 0.0
                twist.angular.z = -angular_speed
            elif key == 'x':  # Dừng lại
                twist.linear.x = 0.0
                twist.angular.z = 0.0
            elif key == 'q':  # Thoát
                break
            else:
                # Nếu không nhấn phím, giữ nguyên trạng thái trước đó
                pass

            # Xuất bản lệnh vận tốc
            pub.publish(twist)
            rate.sleep()

    except Exception as e:
        print(e)

    finally:
        # Dừng robot khi thoát
        twist.linear.x = 0.0
        twist.angular.z = 0.0
        pub.publish(twist)

        # Khôi phục cài đặt terminal
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)