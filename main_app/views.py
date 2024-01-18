import uuid
import boto3
import os
from django.shortcuts import render, redirect
# importing our Class-Based-Views (CBVs)
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Cat, Toy, Photo
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
@login_required
def cats_index(request):
    # collect our objects from the database
    # this uses the objects object on the Cat model class
    # the objects object has a method called all
    # all grabs all of the entities using the parent model(in this case, Cat)
    cats = Cat.objects.filter(user=request.user)

    # print(cats)
    # for cat in cats:
    #     print(cat)
    # just like in ejs, we can pass some data to our views
    return render(request, 'cats/index.html', { 'cats': cats })

# detail view - shows one cat at '/cats/:id'
@login_required
def cats_detail(request, cat_id):
    # find one cat with its id
    cat = Cat.objects.get(id=cat_id)
    # here we'll get a value list of the toy ids assoctiated with the cat
    id_list = cat.toys.all().values_list('id')
    # instantiate FeedingForm to be rendered in our template
    # for all toys cat doesn't have
    toys_cat_doesnt_have = Toy.objects.exclude(id__in=id_list)
    feeding_form = FeedingForm()
    

    return render(request, 'cats/detail.html', { 'cat': cat, 'feeding_form': feeding_form, 'toys': toys_cat_doesnt_have})


# inherit from the CBV - CreateView, to make our cats create view
class CatCreate(LoginRequiredMixin, CreateView):
    # tell the createview to use the Cat model for all its functionality
    model = Cat
    # this view creates a form, so we need to identify which fields to use
    fields = ['name', 'breed', 'description', 'age']
    # we can add other options inside this view
    # success_url = '/cats/{cat_id}'

    # This inherited method is called when a
    # valid cat form is being submitted
    def form_valid(self, form):
    # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user  # form.instance is the cat
        # Let the CreateView do its job as usual
        return super().form_valid(form)


# Update View - extends the UpdateView class
class CatUpdate(LoginRequiredMixin, UpdateView):
    model = Cat
    # let's make it so you can't rename a cat
    # we could simply say fields = '__all__', or we can customize like this:
    fields = ['breed', 'description', 'age']

# Delete View - extends DeleteView
class CatDelete(LoginRequiredMixin, DeleteView):
    model = Cat

    success_url = '/cats'

# FEEDING AND RELATIONSHIP VIEW FUNCTIONS
# this is to add a feeding to a cat
@login_required
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

# List of toy views
# Toy list
class ToyList(LoginRequiredMixin, ListView):
    model = Toy
    template_name = 'toys/index.html'
# Toy Detail
class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy
    template_name = 'toys/detail.html'

# toy create
class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = ['name', 'color']

    def form_valid(self, form):
        return super().form_valid(form)
# Toy Update
class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ['name', 'color']
# Toy Delete
class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = '/toys'

# add and remove toys from cats
@login_required
def assoc_toy(request, cat_id, toy_id):
    # we target the cat and pass it the toy id
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect('detail', cat_id=cat_id)

@login_required
def unassoc_toy(request, cat_id, toy_id):
    # we target the cat and pass it the toy id
    Cat.objects.get(id=cat_id).toys.remove(toy_id)
    return redirect('detail', cat_id=cat_id)

@login_required
def add_photo(request, cat_id):
    #photo-file will be the "name" attribute
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique key for s3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            Photo.objects.create(url=url, cat_id=cat_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', cat_id=cat_id)


def signup(request):
    error_message = ''
    if request.method == "POST":
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in via code
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid signup - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
