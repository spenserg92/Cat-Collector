from django.urls import path
from . import views


urlpatterns = [	
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('cats/', views.cats_index, name='index'),
    # route for the detail page
    # we need an id
    path('cats/<int:cat_id>', views.cats_detail, name='detail')
]
