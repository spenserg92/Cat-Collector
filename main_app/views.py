from django.shortcuts import render
from .models import Cat
## this was to build our intial view
# cats = [
#     {'name': 'Lolo', 'breed': 'tabby', 'description': 'furry little demon', 'age': 3},
#     {'name': 'Sachi', 'breed': 'calico', 'description': 'gentle and loving', 'age': 2},
# ]
# Create your views here.

# Define home view here - '/'

def home(request):
    #unlike with EJS, we need our .html file extension
    return render(request, "home.html")

def about(request):
    return render(request, 'about.html')

# index view - shows all the cats at /cats

def cats_index(request):
    # collect objects
    cats = Cat.objects.all()

    # for cat in cats:
    #     print(cat)
    return render(request, 'cats/index.html', {'cats': cats})

## detail view

def cats_detail(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    return render(request, 'cats/detail.html', {'cat' : cat})