from django.db import models

class Item(models.Model):
    name=models.CharField(max_length=50,default=False)
    photo=models.ImageField(upload_to='profile_photo',help_text='Photo of cookie')
    speciality=models.TextField(default=False)
    price=models.FloatField(default=False)
    avg_rating=models.FloatField(default=0)
    no_of_review=models.IntegerField(default=0)
    def __str__(self):
        return self.name

class Review(models.Model):
    item=models.ForeignKey(Item,on_delete=None)
    customer_name=models.CharField(max_length=50)
    timestamp=models.DateTimeField()
    review=models.TextField()
    rating=models.IntegerField()
    review_type=models.BooleanField()
    is_verified=models.BooleanField()

    def __str__(self):
        return self.review

class Training_Review(models.Model):
    item=models.ForeignKey(Item,on_delete=None)
    customer_name=models.CharField(max_length=50)
    timestamp=models.DateTimeField()
    review=models.TextField()
    rating=models.IntegerField()
    review_type=models.BooleanField()
    def __str__(self):
        return self.review
class Old_Training_data(models.Model):
    review = models.TextField()
    review_type = models.BooleanField()
    def __str__(self):
        return self.review






# Create your models here.
