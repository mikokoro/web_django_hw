from common.models import Customer
from django.http import JsonResponse
import json

# list
def listcustomers(request):
    qs = Customer.objects.values()
    retlist = list(qs)
    return JsonResponse({'ret': 0, 'retlist': retlist})

# add
def addcustomer(request):
    info = request.params['data']
    # create方法添加记录
    record = Customer.objects.create(name=info['name'],
                                     phonenumber=info['phonenumber'],
                                     address=info['address'])  
    return JsonResponse({'ret': 0, 'id':record.id})

# modify
def modifycustomer(request):
    customerid = request.params['id']
    newdata = request.params['newdata']
    # get方法查找
    try:
        customer = Customer.objects.get(id=customerid)
    except Customer.DoesNotExist:
        return  {
                'ret': 1,
                'msg': f'id 为`{customerid}`的客户不存在'
        }
    if 'name' in  newdata:
        customer.name = newdata['name']
    if 'phonenumber' in  newdata:
        customer.phonenumber = newdata['phonenumber']
    if 'address' in  newdata:
        customer.address = newdata['address']
    customer.save()
    return JsonResponse({'ret': 0})

# delete
def deletecustomer(request):
    customerid = request.params['id']
    try:
        customer = Customer.objects.get(id=customerid)
    except Customer.DoesNotExist:
        return  {
                'ret': 1,
                'msg': f'id 为`{customerid}`的客户不存在'
        }
    customer.delete()
    return JsonResponse({'ret': 0})

def dispatcher(request):
    # session 判断
    if 'usertype' not in request.session:
        return JsonResponse({
            'ret': 302,
            'msg': '未登录',
            'redirect': '/mgr/sign.html'}, 
            status=302)
    if request.session['usertype'] != 'mgr' :
        return JsonResponse({
            'ret': 302,
            'msg': '用户非mgr类型',
            'redirect': '/mgr/sign.html'} ,
            status=302)

    if request.method == 'GET':
        request.params = request.GET
    elif request.method in ['POST','PUT','DELETE']:
        request.params = json.loads(request.body)
    action = request.params['action']
    if action == 'list_customer':
        return listcustomers(request)
    elif action == 'add_customer':
        return addcustomer(request)
    elif action == 'modify_customer':
        return modifycustomer(request)
    elif action == 'del_customer':
        return deletecustomer(request)
    else:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})


