from django.shortcuts import render

cats = [
    {'name': 'Lolo', 'breed': 'tabby', 'description': 'furry little demon', 'age': 3},
    {'name': 'Sachi', 'breed': 'calico', 'description': 'gentle and loving', 'age': 2},
]
# Create your views here.

# Define home view here - '/'

def home(request):
    #unlike with EJS, we need our .html file extension
    return render(request, "home.html")

def about(request):
    return render(request, 'about.html')

# index view - shows all the cats at /cats

def cats_index(request):
    return render(request, 'cats/index.html', {'cats': cats})