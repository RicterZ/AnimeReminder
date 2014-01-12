# -*- coding:utf-8 -*-
import json

MethodErrorMessage    = '403 请求方式不被允许'
KeyErrorMessage       = '400 key出错，请重新登录'
LoginErrorMessage     = '401 用户名或者密码错误，请注意大小写'
EmailErrorMessage     = '500 Email格式不符合规范'
EmailExistMessage     = '407 Email已被注册'
PasswordFormatMessage = '500 密码位数不在6~16字符之内'
UnknowErrorMessage    = '500 发生未知错误'
OperateErrorMessage   = '500 操作失败'
OperateSuccessMessage = '200 操作成功'
ScheduleErrorMessage  = '500 获取更新列表失败'
AnimeNotExistMessage  = '501 添加的内容不存在于片库中'
AddRepateMessage      = '503 请不要重复添加'
AnimeErrorMessage     = '501 订阅不在您的订阅列表里'
EpisodeErrorMessage   = '502 集数不符合规范'
DataErrorMessage      = '500 数据错误'
SearchErrorMessage    = '500 搜索的内容未找到'

def returnData(message = OperateSuccessMessage, data = []):
    status = message[0:3]
    msg    = message[4: ]
    return json.dumps({
        "status": int(status),
        "message": msg,
        "data": data
    })