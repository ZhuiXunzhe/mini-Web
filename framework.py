"""
    framework.py:负责处理动态资源请求

实现功能：
    1.创建web框架程序
    2.接收web服务器的动态资源请求
    3.处理web服务器的动态资源请求并把处理结构返回给web服务器
    4.web服务器结构组装成响应报文发动给浏览器

内部构造：
"""
import time


# 获取首页数据
def index():
    # 响应状态
    status = "200 OK"
    # 响应头
    response_header = [("Server", "PWS2.0")]
    # 处理后的数据
    data = time.ctime()

    return status, response_header, data


# 获取login页面
def login():
    # 响应状态
    status = "200 OK"
    # 响应头
    response_header = [("Server", "PWS2.0")]
    # 处理后的数据
    data = time.ctime()

    return status, response_header, data


# 没有找到动态资源
def not_found():
    # 响应状态
    status = "404 Not Found"
    # 响应头
    response_header = [("Server", "PWS2.0")]
    # 处理后的数据
    data = "not found"

    return status, response_header, data


# 处理动态资源请求
def handle_request(env):
    # 获取动态资源请求路径
    request_path = env["request_path"]
    print("接收到的动态资源请求:", request_path)

    if request_path == "/index.html":
        # 获取首页数据
        result = index()
        return result
    elif request_path == "/login.html":
        result = login()
        return result
    else:
        # 没有找到资源
        result = not_found()
        return result
