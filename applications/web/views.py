from django.shortcuts import render

# Create your views here.
def news(request):

    data = {
        
    }
    return render(request, 'web/news.html', data)