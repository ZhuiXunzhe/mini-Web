""""
    web.py:
实现功能：
    根据请求资源路径的后缀明进行判断
        如果请求子元素路径的后缀名是.html则是动态资源，让web框架进行处理
        否则是静态资源请求，让web服务器程序进行处理
内部构造：
    class：web服务器类
    method:启动web服务器函数

"""
import socket
import threading
import sys
import framework


# 定义web服务器类
class HttpWebServer(object):
    def __init__(self,port):
        pass

    # 处理客户请求
    @staticmethod
    def handle_client_quest(new_socket):
        pass

    # 启动服务器函数
    def start(self):
        pass


# 项目启动函数
def main():
    pass


if __name__=='__main__':
    main()



