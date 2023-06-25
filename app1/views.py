from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Topic, Message
from .forms import PostForm


def loginPage(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "사용자를 찾을 수 없습니다.")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "아이디나 비밀번호가 올바르지 않습니다.")

    context = {"page": page}
    return render(request, "app1/login_register.html", context)


def logoutUser(request):
    logout(request)
    return redirect("home")


def registerPage(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "계정을 만드는 과정에서 문제가 발생했습니다.")

    return render(request, "app1/login_register.html", {"form": form})


def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    posts = Post.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    post_count = posts.count()

    post_messages = Message.objects.filter(Q(post__topic__name__icontains=q))

    context = {
        "posts": posts,
        "topics": topics,
        "post_count": post_count,
        "post_messages": post_messages,
    }
    return render(request, "app1/home.html", context)


def post(request, pk):
    post = Post.objects.get(id=pk)
    post_messages = post.message_set.all().order_by("-created")
    participants = post.participants.all()
    topics = Topic.objects.all()

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user, post=post, body=request.POST.get("body")
        )
        post.participants.add(request.user)
        return redirect("post", pk=post.id)

    context = {
        "post": post,
        "post_messages": post_messages,
        "participants": participants,
        "topics": topics,
    }
    return render(request, "app1/post.html", context)


@login_required(login_url="login")
def createPost(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form": form}
    return render(request, "app1/post_form.html", context)


@login_required(login_url="login")
def updatePost(request, pk):
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)

    if request.user != post.host:
        return HttpResponse("당신은 이 글을 수정할 수 없습니다")

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form": form}
    return render(request, "app1/post_form.html", context)


@login_required(login_url="login")
def deletePost(request, pk):
    post = Post.objects.get(id=pk)
    if request.user != post.host:
        return HttpResponse("당신은 이 글을 수정할 수 없습니다")
    if request.method == "POST":
        post.delete()
        return redirect("home")
    return render(request, "app1/delete.html", {"obj": post})


@login_required(login_url="login")
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != messages.user:
        return HttpResponse("당신은 이 댓글을 수정할 수 없습니다")
    if request.method == "POST":
        message.delete()
        return redirect("home")
    return render(request, "app1/delete.html", {"obj": message})
