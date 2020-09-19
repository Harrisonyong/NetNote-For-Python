import hashlib

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from .models import User

@csrf_exempt
#进行用户注册
def reg_view(request):
    if request.method == 'GET':
        return render(request,"user/register.html",locals())
    elif request.method == "POST":
        #获取提交的表单值
        username = request.POST.get("username")
        password_1 = request.POST.get("password_1")
        password_2 = request.POST.get("password_2")
        #非空检查
        if not username or not password_1 or not password_2:
            return render(request,"user/error_1.html",locals())
        # 密码一致性检查
        if password_1 != password_2:
            return render(request,"user/error_2.html",locals())
        # 检查用户是否被占用
        old_user = User.objects.filter(username = username)
        if old_user:
            return HttpResponse("用户已存在")
        # 计算密码的Hash
        md5 = hashlib.md5()
        md5.update(password_1.encode())
        password_h = md5.hexdigest()

        # 用户添加到数据库
        try:
            user = User.objects.create(username= username,password = password_h)
        except Exception as e:
            print("error is %s" % e)
            return HttpResponse("用户已存在")
        return HttpResponse("用户注册成功！")