from django.shortcuts import render

def index(request):
    user = request.GET.get('name', 'Guest')
    context = {
        'page_title': 'Hello from Django',
        'user': user
    }
    return render(request, 'index.html', context)