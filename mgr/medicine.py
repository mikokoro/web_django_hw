from django.http import JsonResponse
from  common.models import Medicine
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
    if action == 'list_medicine':
        return listmedicine(request)
    elif action == 'add_medicine':
        return addmedicine(request)
    elif action == 'modify_medicine':
        return modifymedicine(request)
    elif action == 'del_medicine':
        return deletemedicine(request)
    else:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})

def listmedicine(request):
    qs = Medicine.objects.values()
    retlist = list(qs)
    return JsonResponse({'ret': 0, 'retlist': retlist})

def addmedicine(request):
    info = request.params['data']
    medicine = Medicine.objects.create(name=info['name'] ,
                            sn=info['sn'] ,
                            desc=info['desc'])
    return JsonResponse({'ret': 0, 'id':medicine.id})

def modifymedicine(request):
    medicineid = request.params['id']
    newdata    = request.params['newdata']
    try:
        medicine = Medicine.objects.get(id=medicineid)
    except Medicine.DoesNotExist:
        return  {
                'ret': 1,
                'msg': f'id 为`{medicineid}`的药品不存在'
        }
    if 'name' in  newdata:
        medicine.name = newdata['name']
    if 'sn' in  newdata:
        medicine.sn = newdata['sn']
    if 'desc' in  newdata:
        medicine.desc = newdata['desc']
    medicine.save()
    return JsonResponse({'ret': 0})

def deletemedicine(request):
    medicineid = request.params['id']
    try:
        medicine = Medicine.objects.get(id=medicineid)
    except Medicine.DoesNotExist:
        return  {
                'ret': 1,
                'msg': f'id 为`{medicineid}`的客户不存在'
        }
    medicine.delete()
    return JsonResponse({'ret': 0})