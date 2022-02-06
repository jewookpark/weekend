from django.shortcuts import render, redirect
from .models import Board, Reply
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages

def index(request):
    # GET은 url을 통해서 전달되는 것이다. 숨어서 전달 x
    cate = request.GET.get("cate", "")
    kw = request.GET.get("kw",'')

    if kw:
        if cate == "sub":
            b = Board.objects.filter(subject__startswith = kw)
        elif cate == "sub":
            try:
                from acc.models import Usssssser
                # writer는 foreignkey사용 다른 테이블 특정 레코드 참조
                u = User.objects.get(username=kw)
                b = Board.objects.filter(writer=u)
            except:
                b = Board.objects.none()
        else:
            b = Board.objects.filter(content__contains = kw)
    else:
        b = Board.objects.all()

    pg = request.GET.get("page", 1)
    pag = Paginator(b, 5)
    obj = pag.get_page(pg)
    context = {
        "blist" : obj,
        "cate": cate,
        "kw":kw
    }
    return render(request, "board/index.html", context)

def creply(request, bpk):
    b = Board.objects.get(id=bpk)
    c = request.POST.get("com")
    Reply(b=b, comment=c, replyer=request.user, pubdate=timezone.now()).save()
    return redirect("board:detail", bpk)


def dreply(request, bpk, rpk):
    r = Reply.objects.get(id=rpk)
    if r.replyer == request.user:
        r.delete()
    else:
        messages.error(request, "삭제권한이 없습니다.")
    return redirect("board:detail", bpk)

def create(request):
    if request.method == "POST":
        s = request.POST.get("sub")
        c = request.POST.get("con")
        Board(subject=s, writer=request.user, content=c, pubdate=timezone.now()).save()
        return redirect("board:index")
    return render(request, "board/create.html")

def update(request, bpk):
    b = Board.objects.get(id=bpk)

    if request.user != b.writer:
        messages.error(request, "수정권한이 없습니다.")
        return redirect("board:index")

    if request.method == "POST":
        s = request.POST.get("sub")
        c = request.POST.get("con")
        b.subject = s
        b.content = c
        b.save()
        return redirect("board:detail", bpk)

    context = {
        "b" : b
    }
    return render(request, "board/update.html", context)

def delete(request, bpk):
    b = Board.objects.get(id=bpk)
    if request.user == b.writer:
        b.delete()
    else:
        messages.error(request, "삭제권한이 없습니다.")
    return redirect("board:index")

def detail(request, bpk):
    b = Board.objects.get(id=bpk)
    r = b.reply_set.all()
    context = {
        "b" : b,
        "rlist" : r,
    }
    return render(request, "board/detail.html", context)

def likey(request, bpk):
    b = Board.objects.get(id=bpk)
    # likey: 유저들의 레코드 queryset
    b.likey.add(request.user)
    return redirect('board:detail', bpk)

def unlikey(request, bpk):
    b = Board.objects.get(id=bpk)
    b.likey.remove(request.user)
    return redirect('board:detail', bpk)

# 좋아요를 누른 사람과 아닌 사람을 분리하여 UI 구성
# likey.all을 사용하여 좋아요를 누른 모든 사람을 확인 가능
# user가 만약 누른 사람인지에 따라서 구분
