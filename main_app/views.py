from django.shortcuts import render
# importing our Class-based-views (CBV's)
from django.views.generic.edit import CreateView, UpdateView, DeleteView
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

# Inherit from the CBV - CreateView

class CatCreate(CreateView):
    model = Cat
    # this view creates a form
    fields = '__all__'
    # We can add other options inside this view
    success_url = '/cats/'

# Update View

class CatUpdate(UpdateView):
    model = Cat
    fields = {'breed', 'description', 'age'}

# Delete - View

class CatDelete(DeleteView):
    model = Cat
    success_url = "/cats"
