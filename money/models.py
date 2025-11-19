from django.db import models

# Create your models here.
class User(models.Model):
    Username = models.CharField()
    Email = models.EmailField()
    Password = models.CharField()
    Balance = models.FloatField(null=True,default=0)
    # Income = models.FloatField(default=0)
    # Expenses = models.FloatField(default=0)
    
    def __str__(self):
        return self.Username

class Transection_Type(models.Model):
    transection_Type = models.CharField()
    
    def __str__(self):
        return self.transection_Type

class Transection_Category(models.Model):
    Category = models.CharField()
    
    def __str__(self):
        return self.Category
    
class Transection_History(models.Model):
    uid = models.CharField()
    Date = models.CharField()
    Description = models.CharField()
    transection_Type = models.ForeignKey(Transection_Type, on_delete=models.CASCADE, related_name='type')
    Category = models.ForeignKey(Transection_Category, on_delete=models.CASCADE, related_name='category')
    Amount = models.FloatField()
