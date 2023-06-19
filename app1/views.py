from django.shortcuts import render


rooms = [
    {"id": 1, "name": "Lets learn python!"},
    {"id": 2, "name": "Design with me"},
    {"id": 3, "name": "Frontend developer"},
]

profile = [{"name": "학선양", "server": "KR-Azshara"}]


def home(request):
    context = {"profile": profile}
    return render(request, "app1/home.html", context)


def content(request, pk):
    content = None
    for i in rooms:
        if i["id"] == int(pk):
            room = i
    context = {"room": room}
    return render(request, "app1/content.html")
