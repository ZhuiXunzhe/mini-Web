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
        # 创建tcp服务套接字
        tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置端口号复用，程序退出端口立即释放
        tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        # 绑定端口号
        tcp_server_socket.bind(("", port))
        # 设置监听
        tcp_server_socket.listen(128)
        self.tcp_server_socket = tcp_server_socket

    # 处理客户请求
    @staticmethod
    def handle_client_quest(new_socket):
        # 代码执行至此说明连接已经建立成功
        recv_client_data = new_socket.recv(4096)
        if len(recv_client_data) == 0:
            # print("浏览器已经关闭了")
            # 关闭连接的套接字
            new_socket.close()
            print("已关闭连接套接字...")
            return

        # 收到的数据长度不为零，正常处理请求
        # 对二进制数据进行解码
        recv_client_content = recv_client_data.decode("utf-8")
        # print(recv_client_content)
        # 根据指定字符串进行分割，最大分割次数指定2
        request_list = recv_client_content.split(" ", maxsplit=2)

        # 获取请求资源的路径
        request_path = request_list[1]
        print("请求资源路径:", request_path + "--end" )

        # 判断请求的是否是根目录，条件成立返回index.html
        if request_path == "/":
            request_path = "/index.html"

        # 判断是否是动态资源
        if request_path.endswith(".html"):
            """动态资源移交给框架处理"""
            # 字典存储用户的请求数据
            env = {
                "request_path": request_path
            }
            # 获取处理结果
            status, headers, response_body = framework.handle_request(env)

            # 拼接响应报文
            # 响应行
            response_line = "HTTP/1.1 %s\r\n" % status
            # 响应头
            response_header = ""
            for header in headers:
                # 拼接多个响应头
                response_header += "%s:%s\r\n" % header

            # 拼接报文
            response_data = (response_line + response_header+"\r\n" + response_body).encode("utf-8")
            # 发送数据
            new_socket.send(response_data)
            # 关闭连接
            new_socket.close()
        else:
            """静态资源，服务器处理"""
            try:
                # 动态打开指定文件
                with open("static" + request_path,"rb") as file:
                    # 读取文件数据
                    file_data = file.read()
            except Exception as e:
                # 请求资源不存在返回404页面
                # 响应行
                response_line = "HTTP/1.1 404 Not Found\r\n"
                # 响应头
                response_head = "Server:PWS1.0\r\n"
                with open("static/error.html","rb") as file:
                    file_data = file.read()
                # 响应体
                response_body = file_data
                # 拼接报文
                response_data = (response_line + response_head + "\r\n").encode("utf-8") + response_body
                #发送数据
                new_socket.send(response_data)
            else:
                # 返回正常200页面
                # 响应行
                response_line = "HTTP/1.1 200 OK\r\n"
                # 响应头
                response_header = "Server: PWS1.0\r\n"

                # 响应体
                response_body = file_data

                # 拼接响应报文
                response_data = (response_line + response_header + "\r\n").encode("utf-8") + response_body
                # 发送数据
                new_socket.send(response_data)
            finally:
                # 关闭连接套接字
                new_socket.close()

    # 启动服务器函数
    def start(self):
        print("web服务器已启动...")
        while True:
            # 等待接受客户端的连接请求
            new_socket, ip_port = self.tcp_server_socket.accept()
            sub_thread = threading.Thread(target=self.handle_client_quest, args=(new_socket,))
            # 设置守护线程
            sub_thread.setDaemon(True)
            sub_thread.start()


# 项目启动函数
def main():

    # 获取命令行参数判断长度
    if len(sys.argv) != 2:
        print("执行命令如下：python3 xxx.py 9000")
        return

    # 判断端口号是否是数字
    if not sys.argv[1].isdigit():
        print("执行明林如下：python3 xxx.py 9000")
        return

    # 需要转成int类型
    port = int(sys.argv[1])

    # 创建web服务器
    web_server = HttpWebServer(port)

    # 启动web服务器
    web_server.start()


if __name__=='__main__':
    main()



