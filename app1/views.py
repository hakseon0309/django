from django.shortcuts import render


rooms = [
    {"id": 1, "name": "Lets learn python!"},
    {"id": 2, "name": "Design with me"},
    {"id": 3, "name": "Frontend developer"},
]

profile = [{"name": 1, "server": "KR-Azshara"}]


def main(request):
    context = {"profile": profile}
    return render(request, "app1/home.html", context)


def content(request, pk):
    return render(request, "app1/content.html")
