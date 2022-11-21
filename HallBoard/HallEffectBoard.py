import time

from HallBoard.Mqtt import Mqtt


class HallEffectBoard:

    def __init__(self):
        self.mqtt = Mqtt()
        self.dev_id_c = None
        self.dev_id_b = None
        self.mqtt.run()
        self.data_template = "{'dev_id': {0}, 'msg_code': {1}, 'msg': {}}"
        self.b_connect = 10
        self.b_standby = 11
        self.b_error = 12
        self.b_got = 13
        self.b_position = 14
        self.b_uci = 15
        self.c_connect = 20
        self.c_reset = 21
        self.c_check = 22
        self.c_side = 23
        self.c_retry = 24
        self.c_start = 25
        self.c_light = 30
        self.c_uci = 31

    def connectBoard(self):
        """
        获取此时topic下棋盘请求配对消息
        mqtt接收msg_code 10，接收msg设为自身dev_id_c
        mqtt返回msg_code 20，返回msg内容任意，这里设为对方的dev_id_b
        函数返回布尔值表示配对成功与否
        """
        while True:
            local_dict = self.mqtt.r_dict
            if local_dict['msg_code'] == 10:
                self.dev_id_c = local_dict['msg']
                self.dev_id_b = local_dict['dev_id']
                print("Info: board match request received.")
                self.mqtt.publish(self.data_template.format(self.dev_id_c, self.c_connect, self.dev_id_b))
                print("Info: controller match request sent.")
            elif local_dict['dev_id'] == self.dev_id_b and local_dict['msg_code'] == self.b_standby:
                print("Info: mqtt match success.")
                break

    def checkBoardSet(self):
        """
        检查棋盘初始化摆放情况
        mqtt发送msg_code 22，发送msg内容任意，此处设为"check"
        mqtt等待msg_code 13，等待msg内容不重要（应为"check start"）
        mqtt等待msg_code 11，等待msg内容不重要（应为"wait for side/start/reset"）
        """
        self.mqtt.publish(self.data_template.format(self.dev_id_c, self.c_check, "check"))
        print("Info: check command sent.")
        wait_cnt = 0
        got_flag = False
        while True:
            local_dict = self.mqtt.r_dict
            if local_dict['dev_id'] == self.dev_id_b and local_dict['msg_code'] == self.b_got:
                got_flag = True
                print("Info: board got check command.")
            elif local_dict['dev_id'] == self.dev_id_b and local_dict['msg_code'] == self.b_standby:
                print("Info: board check complete.")
                break
            elif wait_cnt >= 1000 and got_flag is False:
                print("Warn: board check command no respond, try again.")
                wait_cnt = 0
                self.mqtt.publish(self.data_template.format(self.dev_id_c, self.c_check, "check"))
                print("Info: check command sent again.")
            else:
                wait_cnt += 1
                time.sleep(0.001)

    def setPlayerSide(self, side):
        """
        mqtt发送玩家的选边，
        mqtt发送msg_code 23，发送msg内容为"white"或"black"
        mqtt等待msg_code 11，等待msg内容不重要（应为"side set and wait for check/start/reset"）
        """
        self.mqtt.publish(self.data_template.format(self.dev_id_c, self.c_side, side))
        print("Info: player side has been set as %s." % side)
        while True:
            local_dict = self.mqtt.r_dict
            if local_dict['dev_id'] == self.dev_id_b and local_dict['msg_code'] == self.b_standby:
                print("Info: board set player side.")
                break

    def startGame(self):
        """
        开始棋盘检测
        mqtt发送msg_code 25，发送msg内容任意，此处设为"start"
        mqtt等待msg_code 13，等待msg内容不重要（应为"game start"）
        """
        self.mqtt.publish(self.data_template.format(self.dev_id_c, self.c_start, "start"))
        print("Info: start command sent.")
        while True:
            local_dict = self.mqtt.r_dict
            if local_dict['dev_id'] == self.dev_id_b and local_dict['msg_code'] == self.b_got:
                print("Info: board start game.")
                break

    def resetBoard(self):
        """
        重启棋盘
        mqtt发送msg_code 21，发送msg内容任意，此处设为"reset"
        mqtt等待msg_code 13，等待msg内容不重要（应为"board reset"）
        """
        self.mqtt.publish(self.data_template.format(self.dev_id_c, self.c_start, "start"))
        print("Info: reset command sent.")
        while True:
            local_dict = self.mqtt.r_dict
            if local_dict['dev_id'] == self.dev_id_b and local_dict['msg_code'] == self.b_got:
                print("Info: board reset now.")
                break

    # TODO 错误流程完善
    def retry(self):
        """
        重试，用于错步
        mqtt发送msg_code 21，发送msg内容任意，此处设为"retry"
        mqtt等待msg_code 13，等待msg内容不重要（应为"board will retry"）
        """
        self.mqtt.publish(self.data_template.format(self.dev_id_c, self.c_retry, "retry"))
        print("Info: retry command sent.")
        while True:
            local_dict = self.mqtt.r_dict
            if local_dict['dev_id'] == self.dev_id_b and local_dict['msg_code'] == self.b_got:
                print("Info: board retry now.")
                break

    def getPosition(self):
        """
        获取检测的位置
        mqtt等待msg_code 14，等待msg内容为位置字符串（长度2）
        """
        print("Info: waiting board position...")
        while True:
            local_dict = self.mqtt.r_dict
            if local_dict['dev_id'] == self.dev_id_b and local_dict['msg_code'] == self.b_position:
                print("Info: got position.")
                return local_dict['msg']

    def sendLight(self, light_str):
        """
        发送亮灯位置
        mqtt发送msg_code 30，发送msg内容为亮灯位置及颜色字符串（长度=位置数*3+位置数）
        """
        self.mqtt.publish(self.data_template.format(self.dev_id_c, self.c_light, light_str))
        print("Info: light positions sent: %s" % light_str)

    def getUCI(self):
        """
        获取检测的棋步
        mqtt等待msg_code 15，等待msg内容为UCI字符串（长度4或5）
        """
        while True:
            local_dict = self.mqtt.r_dict
            if local_dict['dev_id'] == self.dev_id_b and local_dict['msg_code'] == self.b_uci:
                print("Info: got UCI %s." % local_dict['msg'])
                return local_dict['msg']

    def sendUCI(self, uci):
        """
        发送uci
        mqtt发送msg_code 31，发送msg内容为UCI字符串（长度4或5）
        """
        self.mqtt.publish(self.data_template.format(self.dev_id_c, self.c_uci, uci))
        print("Info: UCI sent: %s" % uci)
