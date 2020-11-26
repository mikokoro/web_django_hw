from django.shortcuts import render
from django.http import HttpResponse
from common.models import Customer  # 导入Customer对象

def listorders(request):
    return HttpResponse('订单信息') 

def listcustomers(request):
    qs = Customer.objects.values()
    ph =  request.GET.get('phonenumber',None) 
    if ph: 
        qs = qs.filter(phonenumber=ph)  # 过滤条件
    retStr = ''
    for customer in qs:
        for name,value in customer.items():
            retStr += f'{name} : {value} | '
        retStr += '<br>'
    return HttpResponse(retStr)