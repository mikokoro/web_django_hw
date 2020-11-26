from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout

# login
def signin(request):
    userName = request.POST.get('username')
    passWord = request.POST.get('password')
    # django校验方法，密码加密
    user = authenticate(username=userName, password=passWord) 
    
    if user is not None:
        # active
        if user.is_active:
            # superuser
            if user.is_superuser:
                login(request, user)
                # 在session中存入用户类型...? 一次登陆的信息
                request.session['usertype'] = 'mgr'
                return JsonResponse({'ret': 0})
            else:
                return JsonResponse({'ret': 1, 'msg': '请使用管理员账户登录'})
        else:
            return JsonResponse({'ret': 0, 'msg': '用户已经被禁用'})
    else:
        return JsonResponse({'ret': 1, 'msg': '用户名或者密码错误'})

#logout
def signout(request):
    logout(request)
    return JsonResponse({'ret': 0})

