from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib import messages

def update(request):
    if request.method == "POST":
        u = request.user
        pw = request.POST.get("upass")
        co = request.POST.get("comment")
        pi = request.FILES.get("upic")
        if pw:
            u.set_password(pw)
        if pi:
            u.pic.delete()
            u.pic = pi
        u.comment = co
        u.save()
        login(request, u)
        return redirect("acc:profile")

    return render(request, "acc/update.html")

def delete(request):
    # 사진 삭제는 따로 지정해 주어야 한다. 자동 파일 삭제 x
    request.user.pic.delete()
    request.user.delete()
    return redirect("acc:index")

def profile(request):
    return render(request, "acc/profile.html")

def signup(request):
    if request.method == "POST":
        un = request.POST.get("uname")
        pw = request.POST.get("upass")
        ag = request.POST.get("age")
        co = request.POST.get("ucomm")
        pi = request.FILES.get("upic")
        try:
            User.objects.create_user(username=un, password=pw, age=ag, comment=co, pic=pi)
        except:
            messages.error(request, "이미 사용중인 user입니다.")
        return redirect("acc:login")
    return render(request, "acc/signup.html")

def logout_user(request):
    logout(request)
    messages.info(request, "안녕히 돌아가세요!")
    return redirect("acc:index")

# Create your views here.
def index(request):
    return render(request, "acc/index.html")

def login_user(request):
    if request.method == "POST":
        un = request.POST.get("uname")
        pw = request.POST.get("upass")
        user = authenticate(username=un, password=pw)
        if user:
            login(request, user)
            messages.success(request, f"{user}님 환영합니다!")
        else:
            messages.error(request, "정보가 없습니다 회원가입 요망!")
        return redirect("acc:index")
    return render(request, "acc/login.html")