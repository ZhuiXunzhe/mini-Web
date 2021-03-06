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
import pymysql


# 定义路由列表
route_list = []


# 定义带参数的装饰器
def route(path):
    # 装饰器
    def decorator(func):
        # 当执行装饰器装饰指定函数的时候，把路径和函数添加到路由列表
        route_list.append((path, func))

        def inner():
            # 执行指定函数
            return func()

        return inner

    # 返回装饰器
    return decorator


# 获取login数据
@route("/login.html")
def login():
    # 响应状态
    status = "200 OK"
    # 响应头
    response_header = [("Server", "PWS2.0")]
    # 处理后的数据
    data = time.ctime()

    return status, response_header, data


# 获取首页数据
@route("/index.html")
def index():
    print("执行了index函数")
    # 响应状态
    status = "200 OK"
    # 响应头
    response_header = [("Server", "PWS2.0")]

    # 1. 打开模板文件，读取数据
    with open("template/index.html", "r") as file:
        file_data = file.read()

    # 处理后的数据, 从数据库查询
    conn = pymysql.connect(
        host="10.170.15.41",
        port=3306,
        user="root",
        password="287714",
        database="stock_db",
        charset="utf8"
    )

    # 获取游标
    cursor = conn.cursor()
    # 查询sql语句
    sql = "select * from info;"
    # 执行sql
    cursor.execute(sql)
    # 获取结果集
    result = cursor.fetchall()
    # print(result)

    data = ""
    for row in result:
        data += '''<tr>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                   </tr>''' % row

    # 2. 替换模板文件中的模板遍历
    result = file_data.replace("{%content%}", data)
    return status, response_header, result


# # 获取个人中心数据
# @route("/center.html")
# def center():
#     # 响应状态
#     status = "200 OK";
#     # 响应头
#     response_header = [("Server", "PWS2.0")]
#
#     # 打开模板文件，读取数据
#     with open("template/center.html", "r") as file:
#         file_data = file.read()
#
#     # 处理后的数据, 从数据库查询
#     data = time.ctime()
#     # 替换模板文件中的模板遍历
#     result = file_data.replace("{%content%}", data)
#
#     return status, response_header, result


# 没有找到动态资源
def not_found():
    # 响应状态
    status = "404 Not Found"
    # 响应头
    response_header = [("Server", "PWS1.0")]

    # 1. 打开模板文件，读取数据
    with open("static/error.html", "r") as file:
        file_data = file.read()

    return status, response_header, file_data
    # # 响应状态
    # status = "404 Not Found"
    # # 响应头
    # response_header = [("Server", "PWS2.0")]
    # # 处理后的数据
    # data = "not found"
    #
    # return status, response_header, data


# # 定义路由列表
# route_list = [
#     ("/index.html", index),
#     ("/login.html", login)
# ]


# 处理动态资源请求
def handle_request(env):
    # 获取动态资源请求路径
    request_path = env["request_path"]
    print("接收到的动态资源请求:", request_path)

    # 遍历路由列表，选择执行的函数
    for (path, func) in route_list:
        if request_path == path:
            print("查到了路由")
            print("路由列表:",route_list)
            result = func()
            return result
    else:
        # 没有动态资源
        print("没查到路由")
        result = not_found()
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
