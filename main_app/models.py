from django.db import models
from django.urls import reverse

# Create your models here.

class Cat(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()

    def __str__(self):
        return self.name
    
# this is the get_absolute_url method, it redirects

def get_absolute_url(self):
    return reverse('detail', kwargs={'cat_id': self.id})

MEALS = (
    # this is a tuple with multiple tuples
    # each of these is called a 2-tuple
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)

# The model for feedings 1:M
# One cat can have many feedings
class Feeding(models.Model):
    date = models.DateField()
    meal = models.CharField(
        max_length=1,
        #add the custom 'choices' field option
        # this is what will create our dropdown menu
        choices=MEALS,
        #set the default to B
        default=MEALS[0][0]
    )
    # Creates the one to many relationship - Cat -< Feedings
    # models.ForeignKey needs 2 args, the model, and what to do if the parent model is deleted
    # in the db, the column in the feedings table for the FK will be called cat_id, because Django, by default, appends_id to the name of the model
    # DONT CONFUSE THIS WITH MONGODB AND THEIR `._id` NOT THE SAME
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_meal_display()} on {self.date} for {self.cat}"