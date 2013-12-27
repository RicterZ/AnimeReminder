# -*- coding:utf-8 -*-
import json

MethodErrorMessage    = '请求方式不被允许'
KeyErrorMessage       = 'key出错，请重新登录'
LoginErrorMessage     = '用户名或者密码错误，请注意大小写'
EmailErrorMessage     = 'Email格式不符合规范'
EmailExistMessage     = 'Email已被注册'
PasswordFormatMessage = '密码位数不在6~16字符之内'
UnknowErrorMessage    = '发生未知错误'
OperateErrorMessage   = '操作失败'
OperateSuccessMessage = '操作成功'
ScheduleErrorMessage  = '获取更新列表失败'
AnimeNotExistMessage  = '添加的内容不存在于片库中'
AddRepateMessage      = '请不要重复添加'
AnimeErrorMessage     = '订阅不在您的订阅列表里'
EpisodeErrorMessage   = '集数不符合规范'

def returnData(status=200, message="", data=[]):
    return json.dumps({
        "status": status,
        "message": message,
        "data": data
    })