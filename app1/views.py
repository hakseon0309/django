from django.shortcuts import render


posts = [
    {"id": 1, "title": "number1 post", "desc": "content1"},
    {"id": 2, "title": "number2 post", "desc": "content2"},
    {"id": 3, "title": "number3 post", "desc": "content3"},
]

profile = [{"name": "학선양", "server": "KR-Azshara"}]


def home(request):
    context = {"posts": posts}
    return render(request, "app1/home.html", context)


def post(request, pk):
    post = None
    for i in posts:
        if i["id"] == int(pk):
            post = i
    context = {"post": post}
    return render(request, "app1/post.html", context)
