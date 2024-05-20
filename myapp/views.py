from django.shortcuts import render

# Create your views here.
def type_game(response):

    return render(response,'templates/myapp/index.html')
