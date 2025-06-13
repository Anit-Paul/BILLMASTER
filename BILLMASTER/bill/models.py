
from django.db import models
from login.models import account

# Create your models here.
class product(models.Model):
    product_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(account, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, null=True)
    product_quantity = models.IntegerField()
    cost = models.IntegerField()


    