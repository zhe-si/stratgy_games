import pickle
import socket
import sys

import pygame.image
from pygame import Surface

from exception import LogicException
from pat_pat.role import Role, Action
from pat_pat.user.interface import UserInterface

LENGTH_BYTES_NUM = 8


def receive_all(s: socket.socket, count: int):
    buf = b''
    while count != 0:
        new_buf = s.recv(count)
        if not new_buf:
            return None
        buf += new_buf
        count -= len(new_buf)
    return buf


class SendUserProxy(UserInterface):
    """策略发送用户代理

    主动连接接收代理，但主动等待接收代理发送调用请求
    调用请求id：0对应decision, 1对应get_user_name, 2对应get_role_id
    """

    def __init__(self, user: UserInterface, ip: str, port: int):
        self.__user = user
        self.__receive_proxy_address = (ip, port)
        try:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket.connect(self.__receive_proxy_address)
            print("Receive Proxy {} connect successful".format(self.__receive_proxy_address))
        except socket.error as err:
            print(err)
            sys.exit(1)

    def __del__(self):
        self.__socket.close()

    def run(self):
        while True:
            call_data_length = receive_all(self.__socket, LENGTH_BYTES_NUM)
            # 断开连接等原因导致读入数据失败
            if call_data_length is None:
                return
            call_data_length = int.from_bytes(call_data_length, byteorder="little", signed=True)
            call_data = receive_all(self.__socket, call_data_length)
            call_args = pickle.loads(call_data)
            if call_args[0] == 0:
                action = self.decision(call_args[1], call_args[2])
                self.__send_return(action)
            elif call_args[0] == 1:
                user_name = self.get_user_name()
                self.__send_return(user_name)
            elif call_args[0] == 2:
                roles_pics_turn = call_args[1]
                roles_pics = [[pygame.image.fromstring(role_pic_pair[0], role_pic_pair[1], "RGBA") for role_pic_pair in
                               role_pics_turn] for role_pics_turn in roles_pics_turn]
                role_id = self.get_role_id(roles_pics)
                self.__send_return(role_id)
            else:
                self.__socket.close()
                raise LogicException("receive user proxy call wrong function id")

    def __send_return(self, return_object):
        return_data = pickle.dumps(return_object)
        self.__socket.sendall(len(return_data).to_bytes(LENGTH_BYTES_NUM, byteorder="little", signed=True))
        self.__socket.sendall(return_data)

    def decision(self, my_role: Role, enemies_role: list[tuple[str, Role]]) -> Action:
        return self.__user.decision(my_role, enemies_role)

    def get_user_name(self) -> str:
        return self.__user.get_user_name()

    def get_role_id(self, roles_pics: list[list[Surface]]) -> int:
        return self.__user.get_role_id(roles_pics)


class ReceiveUserProxy(UserInterface):
    """策略接收用户代理

    被动连接发送代理，但主动调用接口方法
    """

    BIND_IP = "0.0.0.0"
    BIND_PORT = 7789
    server_socket = None
    conn_num = 0
    computer_ip = socket.gethostbyname(socket.gethostname())

    def __init__(self, connect: socket.socket, connect_addr):
        self.__connect = connect
        self.__connect_addr = connect_addr

    def __del__(self):
        self.conn_num -= 1
        self.__connect.close()
        if self.conn_num == 0:
            self.server_socket.close()
            self.server_socket = None

    @classmethod
    def wait_connect(cls):
        """产生连接，创建接收代理的静态方法"""
        print("ReceiveUser Proxy Server URI: {}:{}".format(cls.computer_ip, ReceiveUserProxy.BIND_PORT))

        if cls.server_socket is None:
            cls.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cls.server_socket.bind((cls.BIND_IP, cls.BIND_PORT))
            cls.server_socket.listen(10)

        conn, addr = cls.server_socket.accept()
        cls.conn_num += 1
        print("Sender Proxy {} connect successful".format(addr))
        return ReceiveUserProxy(conn, addr)

    def decision(self, my_role: Role, enemies_role: list[tuple[str, Role]]) -> Action:
        args = [0, Role, enemies_role]
        self.__send_args(args)
        action = self.__receive_return()
        return action

    def get_user_name(self) -> str:
        args = [1]
        self.__send_args(args)
        user_name = self.__receive_return()
        return user_name

    def get_role_id(self, roles_pics: list[list[Surface]]) -> int:
        roles_pics_turn = [[(pygame.image.tostring(role_pic, "RGBA"), role_pic.get_size()) for role_pic in role_pics]
                           for role_pics in roles_pics]
        args = [2, roles_pics_turn]
        self.__send_args(args)
        role_id = self.__receive_return()
        return role_id

    def __send_args(self, args):
        args_data = pickle.dumps(args)
        self.__connect.sendall(len(args_data).to_bytes(LENGTH_BYTES_NUM, byteorder="little", signed=True))
        self.__connect.sendall(args_data)

    def __receive_return(self):
        return_data_length = receive_all(self.__connect, LENGTH_BYTES_NUM)
        return_data_length = int.from_bytes(return_data_length, byteorder="little", signed=True)
        return_data = receive_all(self.__connect, return_data_length)
        return_object = pickle.loads(return_data)
        return return_object


def main():
    role1 = Role(2, 4)
    role2 = Role(1, 3)
    r_p = ReceiveUserProxy.wait_connect()
    print(r_p.decision(role1, [("1", role2)]))


if __name__ == '__main__':
    main()
