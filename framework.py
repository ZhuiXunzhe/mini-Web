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


# 获取login数据
def login():
    # 响应状态
    status = "200 OK"
    # 响应头
    response_header = [("Server", "PWS2.0")]
    # 处理后的数据
    data = time.ctime()

    return status, response_header, data


# 获取首页数据
def index():
    # 响应状态
    status = "200 OK"
    # 响应头
    response_header = [("Server", "PWS2.0")]

    # 1. 打开模板文件，读取数据
    with open("template/index.html", "r") as file:
        file_data = file.read()

    # 处理后的数据, 从数据库查询
    data = time.ctime()
    # 2. 替换模板文件中的模板遍历
    result = file_data.replace("{%content%}", data)

    return status, response_header, result


# 没有找到动态资源
def not_found():
    # 响应状态
    status = "404 Not Found"
    # 响应头
    response_header = [("Server", "PWS2.0")]
    # 处理后的数据
    data = "not found"

    return status, response_header, data


# 定义路由列表
route_list = [
    ("/index.html", index),
    ("/login.html", login)
]


# 处理动态资源请求
def handle_request(env):
    # 获取动态资源请求路径
    request_path = env["request_path"]
    print("接收到的动态资源请求:", request_path)

    # 遍历路由列表，选择执行的函数
    for path, func in route_list:
        if request_path == path:
            result = func()
            return result

    # if request_path == "/index.html":
    #     # 获取首页数据
    #     result = index()
    #     return result
    # elif request_path == "/login.html":
    #     result = login()
    #     return result
    # else:
    #     # 没有找到资源
    #     result = not_found()
    #     return result
