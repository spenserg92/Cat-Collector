from django.shortcuts import render, redirect
# importing our Class-Based-Views (CBVs)
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Cat
from .forms import FeedingForm
# Add this cats list below the imports
# this was to build our inital view - now we have cats in the db
# cats = [
#   {'name': 'Lolo', 'breed': 'tabby', 'description': 'furry little demon', 'age': 3},
#   {'name': 'Sachi', 'breed': 'calico', 'description': 'gentle and loving', 'age': 2},
#   {'name': 'Donut', 'breed': 'siamese', 'description': 'cute but kinda scary', 'age': 0},
# ]

# Create your views here.

# define home view here - '/'
# GET - Home
def home(request):
    # unlike with ejs, we need our .html file extension
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

# index view - shows all the cats at '/cats'
def cats_index(request):
    # collect our objects from the database
    # this uses the objects object on the Cat model class
    # the objects object has a method called all
    # all grabs all of the entities using the parent model(in this case, Cat)
    cats = Cat.objects.all()
    # print(cats)
    # for cat in cats:
    #     print(cat)
    # just like in ejs, we can pass some data to our views
    return render(request, 'cats/index.html', { 'cats': cats })

# detail view - shows one cat at '/cats/:id'
def cats_detail(request, cat_id):
    # find one cat with its id
    cat = Cat.objects.get(id=cat_id)
    # instantiate FeedingForm to be rendered in our template
    feeding_form = FeedingForm()

    return render(request, 'cats/detail.html', { 'cat': cat, 'feeding_form': feeding_form })

# inherit from the CBV - CreateView, to make our cats create view
class CatCreate(CreateView):
    # tell the createview to use the Cat model for all its functionality
    model = Cat
    # this view creates a form, so we need to identify which fields to use
    fields = '__all__'
    # we can add other options inside this view
    # success_url = '/cats/{cat_id}'

# Update View - extends the UpdateView class
class CatUpdate(UpdateView):
    model = Cat
    # let's make it so you can't rename a cat
    # we could simply say fields = '__all__', or we can customize like this:
    fields = ['breed', 'description', 'age']

# Delete View - extends DeleteView
class CatDelete(DeleteView):
    model = Cat

    success_url = '/cats'

# FEEDING AND RELATIONSHIP VIEW FUNCTIONS
# this is to add a feeding to a cat
def add_feeding(request, cat_id):
    # create a ModelForm instance using the data in request.POST
    form = FeedingForm(request.POST)
    # it's also important to validate forms.
    # django gives us a built in function for that
    if form.is_valid():
        # dont want to save the feeding to the db until we have a cat id
        new_feeding = form.save(commit=False)
        # this is where we add the cat id
        new_feeding.cat_id = cat_id
        new_feeding.save()
    # finally, redirect to the cat detail page
    return redirect('detail', cat_id=cat_id)