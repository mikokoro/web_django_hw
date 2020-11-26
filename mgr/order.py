from django.http import JsonResponse
from django.db.models import F
from django.db import IntegrityError, transaction
from  common.models import  Order,OrderMedicine
import json

def dispatcher(request):
    if 'usertype' not in request.session:
        return JsonResponse({
            'ret': 302,
            'msg': '未登录',
            'redirect': '/mgr/sign.html'},
            status=302)
    if request.session['usertype'] != 'mgr':
        return JsonResponse({
            'ret': 302,
            'msg': '用户非mgr类型',
            'redirect': '/mgr/sign.html'},
            status=302)
    if request.method == 'GET':
        request.params = request.GET
    elif request.method in ['POST','PUT','DELETE']:
        request.params = json.loads(request.body)
    action = request.params['action']
    if action == 'list_order':
        return listorder(request)
    elif action == 'add_order':
        return addorder(request)
    else:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})


def addorder(request):
    info = request.params['data']
    with transaction.atomic():
        new_order = Order.objects.create(name=info['name'],
                                         customer_id=info['customerid'])
        batch = [OrderMedicine(order_id=new_order.id, medicine_id=mid, amount=1)
                 for mid in info['medicineids']]
        OrderMedicine.objects.bulk_create(batch)
    return JsonResponse({'ret': 0, 'id': new_order.id})

def listorder(request):
    qs = Order.objects \
        .annotate(
                customer_name=F('customer__name'),
                medicines_name=F('medicines__name')
        )\
        .values(
        'id', 'name', 'create_date',
        'customer_name',
        'medicines_name'
    )
    retlist = list(qs)
    newlist = []
    id2order = {}
    for one in retlist:
        orderid = one['id']
        if orderid not in id2order:
            newlist.append(one)
            id2order[orderid] = one
        else:
            id2order[orderid]['medicines_name'] += ' | ' + one['medicines_name']
    return JsonResponse({'ret': 0, 'retlist': newlist})
