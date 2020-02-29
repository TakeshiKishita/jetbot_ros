import rclpy
from rclpy.node import Node

from Adafruit_MotorHAT import Adafruit_MotorHAT
from std_msgs.msg import String


class JetbotMotorController(Node):
    def __init__(self):
        super().__init__('jetbot_motor_controller')
        # String型のchatterトピックを送信するpublisherの定義
	    self.subscription = self.create_subscription(String, 'chatter', self.listener_callback)
        # 送信周期毎にtimer_callbackを呼び出し（送信周期は0.5秒）
        self.timer = self.create_timer(0.5, self.timer_callback)

    # sets motor speed between [-1.0, 1.0]
    def set_speed(self, motor_id, value):
        max_pwm = 115.0
        speed = int(min(max(abs(value * max_pwm), 0), max_pwm))

        if motor_id == 1:
            motor = motor_left
        elif motor_id == 2:
            motor = motor_right
        else:
            self.get_logger().error('set_speed(%d, %f) -> invalid motor_ID=%d', motor_id, value, motor_id)
            return

        motor.setSpeed(speed)

        if value > 0:
            motor.run(Adafruit_MotorHAT.FORWARD)
        else:
            motor.run(Adafruit_MotorHAT.BACKWARD)

    # stops all motors
    @staticmethod
    def all_stop():
        motor_left.setSpeed(0)
        motor_right.setSpeed(0)

        motor_left.run(Adafruit_MotorHAT.RELEASE)
        motor_right.run(Adafruit_MotorHAT.RELEASE)

    # directional commands (degree, speed)
    def on_cmd_dir(self, msg):
        self.get_logger().info(rospy.get_caller_id() + ' cmd_dir=%s', msg.data)

    # raw L/R motor commands (speed, speed)
    def on_cmd_raw(self, msg):
        self.get_logger().info(rospy.get_caller_id() + ' cmd_raw=%s', msg.data)

    # simple string commands (left/right/forward/backward/stop)
    def on_cmd_str(self, msg):
        self.get_logger().info(rospy.get_caller_id() + ' cmd_str=%s', msg.data)

        if msg.data.lower() == "left":
            self.set_speed(motor_left_ID, -1.0)
            self.set_speed(motor_right_ID, 1.0)
        elif msg.data.lower() == "right":
            self.set_speed(motor_left_ID, 1.0)
            self.set_speed(motor_right_ID, -1.0)
        elif msg.data.lower() == "forward":
            self.set_speed(motor_left_ID, 1.0)
            self.set_speed(motor_right_ID, 1.0)
        elif msg.data.lower() == "backward":
            self.set_speed(motor_left_ID, -1.0)
            self.set_speed(motor_right_ID, -1.0)
        elif msg.data.lower() == "stop":
            self.all_stop()
        else:
            self.get_logger().error(rospy.get_caller_id() + ' invalid cmd_str=%s', msg.data)


# initialization
if __name__ == '__main__':
    # setup motor controller
    motor_driver = Adafruit_MotorHAT(i2c_bus=1)

    motor_left_ID = 1
    motor_right_ID = 2

    motor_left = motor_driver.getMotor(motor_left_ID)
    motor_right = motor_driver.getMotor(motor_right_ID)
    # Pythonクライアントライブラリの初期化
    rclpy.init(args=args)

    jetbot_motor_controller = JetbotMotorController()

    # stop the motors as precaution
    jetbot_motor_controller.all_stop()

    # setup ros node
    rospy.init_node('jetbot_motors')

    rospy.Subscriber('~cmd_dir', String, on_cmd_dir)
    rospy.Subscriber('~cmd_raw', String, on_cmd_raw)
    rospy.Subscriber('~cmd_str', String, on_cmd_str)

    # minimal_publisherノードの実行開始
    rclpy.spin(jetbot_motor_controller)
    # Pythonクライアントライブラリの終了
    rclpy.shutdown()

    # stop motors before exiting
    all_stop()
