from django.db import models
from django.urls import reverse
from datetime import date

MEALS = (
    # this is a tuple with multiple tuples
    # each of these is called a 2-tuple
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner'),
)

# Create your models here.
class Cat(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()

    def __str__(self):
        return self.name
    
    # this is the get_absolute_url method, it redirects to the detail page where appropriate
    def get_absolute_url(self):
        return reverse('detail', kwargs={'cat_id': self.id})
    
    # this is how we can view related data from the main parent model
    def fed_for_today(self):
        # we can use django's filter, which produces a queryset for all feedings.
        # we'll look at the array(QuerySet) and compare it to the length of the MEALS tuple
        # we can return a boolean, that will be useful in our detail template
        return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)


# The model for feedings - this is a 1:M relationship with cats
    # one cat can have many feedings
class Feeding(models.Model):
    # our model attributes go here
    # we can add a custom label to show up on our forms
    date = models.DateField('feeding date')
    # meals are a charfield with max_length of one, because we're only going to save the first initial of each meal
    # this will help generate a dropdown in the automagically created modelform
    # B-reakfast
    # L-unch
    # D-inner
    meal = models.CharField(
        max_length=1,
        # add the custom 'choices' field option
        # this is what will create our dropdown menu
        choices=MEALS,
        # set the default choice, to be 'B'
        default=MEALS[0][0]
    )
    # creates the one to many relationship - Cat -< Feedings
    # models.ForeignKey needs two args, the model, and what to do if the parent model is deleted.
    # in the db, the column in the feedings table for the FK will be called cat_id, because django, by default, appends _id to the name of the model
    # DO NOT CONFUSE THIS WITH MONGODB AND THEIR `._id` NOT THE SAME
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_meal_display()} on {self.date} for {self.cat}"
    
    # change the default sort
    class Meta:
        ordering = ['-date']