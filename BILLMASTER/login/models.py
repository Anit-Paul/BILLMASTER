from django.db import models

# Create your models here.
class account(models.Model):
    name=models.CharField((""), max_length=50)
    email=models.CharField((""), max_length=50,primary_key=True)
    password=models.CharField((""), max_length=12)