import json
import string

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import requests
from datetime import datetime

from common.models import Numbers
import numpy as np

#基础路径issueCount=1&issueStart=&issueEnd=&dayStart=&dayEnd=&pageNo=1&pageSize=30&week=&systemType=PC"
normal_url = "http://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice"
issueCount=10
init_params={
    "name":"kl8",#双色球
    "issueCount":issueCount,#默认期数 1
    "pageNo":1,
    "pageSize":100,
    "systemType":"PC"
}
# 显示所有的数据
def list_numbers(request):
    qs=Numbers.objects.values();
    retlist = list(qs)
    return JsonResponse({'ret':0,'retlist':retlist})

# 拉取最新一条的数据
def ask_numbers_by_one_response_issueCount(response):

    # 获取信息
    number_str = response['red']+","+response['blue']
    code = response['code']
    date = response['date'].split('(')[0]
    date= datetime.strptime(date, "%Y-%m-%d")
    # 存入数据库
    try:
        # 根据 id 从数据库中找到相应的客户记录
        numbers = Numbers.objects.get(code=code)
    except Numbers.DoesNotExist:
        record = Numbers.objects.create(code=code, number_str=number_str, public_time=date)
        return "0"

    return  code

# 拉取最新n条的数据
def pull_numbers_by_issueCount(response):
    # 多条信息
    print("===============================response================")
    init_params["issueCount"]=response.GET["num"]
    response = requests.get(url=normal_url, params=init_params).json()
    responses = response['result']
    fail_insert_list=[]
    for r in responses:
        code = ask_numbers_by_one_response_issueCount(r)
        if code != "0":
            fail_insert_list.append(code)
    if len(fail_insert_list)==0:
        return JsonResponse({'ret': 0, 'msg': '插入成功'}, json_dumps_params={"ensure_ascii": False})
    else:
        return JsonResponse({'ret': 1, 'msg':"code为"+str(fail_insert_list)+'数据已存在 其他都插入成功'}, json_dumps_params={"ensure_ascii": False})

# 列出数组里近n个数
def ask_numbers_from_db_by_issueCount(response):
    print("===============================response================")
    # 获取num
    num = response.GET["num"]
    # 根据num从数据库里面查数据
    # 创建数组80个 为0的二维数组
    # number_count=np.zeros(81,dtype=np.int)
    number_count= []
    for i in range(0,81):
        number_count.append(0)
    print("============================number_count=====================")

    try:
        str_list=Numbers.objects.raw(f'''select id,number_str from common_numbers
                                order by public_time DESC
                                limit {{}};'''.format(num))
    except Numbers.DoesNotExist:
      return JsonResponse({'ret': 1, 'msg': '数据库没有这么多数据'}, json_dumps_params={"ensure_ascii": False})
    # 获取数据
    for s in str_list:
        str2nums = (s.number_str).split(',')[:-1]
        for str2num in str2nums:
            str2num=int(str2num)
            number_count[str2num]=number_count[str2num]+1

    result=[]
    for i in range(1,len(number_count)):
        my_pair = {}
        my_pair["num"]=i
        my_pair["count"] = number_count[i]
        result.append(my_pair)

    if len(number_count)>0:
        return JsonResponse({'ret': 0, 'data': result}, json_dumps_params={"ensure_ascii": False})
    else:
        return JsonResponse({'ret': 1, 'msg': '出错了'}, json_dumps_params={"ensure_ascii": False})

# 列出数组里近n个数
def ask_numbers_from_db_Top_10_by_count(response):
    print("===============================response================")
    # 获取num
    num = response.GET["num"]
    # 根据num从数据库里面查数据
    # 创建数组80个 为0的二维数组
    # number_count=np.zeros(81,dtype=np.int)
    number_count= []
    for i in range(0,81):
        number_count.append(0)
    print("============================number_count=====================")

    try:
        str_list=Numbers.objects.raw(f'''select id,number_str from common_numbers
                                order by public_time DESC
                                limit {{}};'''.format(num))
    except Numbers.DoesNotExist:
      return JsonResponse({'ret': 1, 'msg': '数据库没有这么多数据'}, json_dumps_params={"ensure_ascii": False})
    # 获取数据
    for s in str_list:
        str2nums = (s.number_str).split(',')[:-1]
        for str2num in str2nums:
            str2num=int(str2num)
            number_count[str2num]=number_count[str2num]+1

    result=[]
    for i in range(1,len(number_count)):
        my_pair = {}
        my_pair["num"]=i
        my_pair["count"] = number_count[i]
        result.append(my_pair)

    result.sort(key=lambda x: x["count"], reverse=True)
    my_result=[]
    for i in range(10):
        my_result.append(result[i])
    if len(number_count)>0:
        return JsonResponse({'ret': 0, 'data': my_result}, json_dumps_params={"ensure_ascii": False})
    else:
        return JsonResponse({'ret': 1, 'msg': '出错了'}, json_dumps_params={"ensure_ascii": False})


# Create your views here.
