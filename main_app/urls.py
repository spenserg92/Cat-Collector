from django.urls import path
from . import views

# this file is how we map our urls to views
# views are like our controllers, they map HTTP requests to code. This file is how we match those requests to specific urls.
# the line `name='home'` is a kwarg, which gives the route a name. naming routes is optional, but best practices.
# later in the codealong, we'll see just how useful it is to name our routes.
urlpatterns = [
    # first arg - url endpoint
    # second arg - the view to render
    # thrid arg(opt) - names the route
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    # route for the index page of our cats
    path('cats/', views.cats_index, name='index'),
    # route for the detail page of our cats
    # we need an id, as well as way to refer to the id(a route parameter)
    path('cats/<int:cat_id>/', views.cats_detail, name='detail'),
    path('cats/create/', views.CatCreate.as_view(), name='cats_create'),
    path('cats/<int:pk>/update/', views.CatUpdate.as_view(), name='cats_update'),
    path('cats/<int:pk>/delete/', views.CatDelete.as_view(), name='cats_delete'),
    path('cats/<int:cat_id>/add_feeding/', views.add_feeding, name='add_feeding'),
    # Toy URLs
    path('toys/', views.ToyList.as_view(), name='toys_index'),
    path('toys/create/', views.ToyCreate.as_view(), name='toys_create'),
    path('toys/<int:pk>/update/', views.ToyUpdate.as_view(), name='toys_update'),
    path('toys/<int:pk>/delete/', views.ToyDelete.as_view(), name='toys_delete'),
    path('toys/<int:pk>/', views.ToyDetail.as_view(), name='toys_detail'),
    #once this is all set up directly, we will add some code to associate our toys with our cats as well as a url to unassociate toys and cats
    path('cats/<int:cat_id>/assoc_toy/<int:toy_id>/', views.assoc_toy, name='assoc_toy'),
    path('cats/<int:cat_id>/unassoc_toy/<int:toy_id>/', views.unassoc_toy, name='unassoc_toy'),
    # Photo urls
    path('cats/<int:cat_id>/add_photo/', views.add_photo, name='add_photo'),
]