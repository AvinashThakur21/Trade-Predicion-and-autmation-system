from django.db import models


from django.urls import reverse # Used in get_absolute_url() to get URL for specified ID

from django.db.models import UniqueConstraint # Constrains fields to unique values
from django.db.models.functions import Lower # Returns lower cased value of field
# Create your models here.


# only col in created , key contraints ...remaining 
class stock(models.Model):
    script_id = models.AutoField(primary_key=True,help_text='Nse script id ')
    stock_name = models.CharField(max_length= 50,help_text ='Stock Full or General used Name ' )
    script_symbol = models.CharField(max_length = 50, unique=True,help_text = 'Stock standard scripy_symbol name given by nse')

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class trade(models.Model):
    #script_id = models.ForeignKey(stock,on_delete=models.CASCADE)
    #trade_id = models.AutoField()
    entry = models.FloatField()
    stoploss = models.FloatField()
    target = models.FloatField()
    quantity = models.FloatField()
    

    def __str__(self):
        """String for representing the Model object."""
        return str(self.entry)

class user(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=50)  
    user_username = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=50)
    broker = models.CharField(max_length=50)
    api = models.TextField(help_text='api by broker or entry and exit')

    def __str__(self):
        return str('user_username')
    
class user_personalization(models.Model):
    user_id = models.OneToOneField(user,on_delete=models.CASCADE)
    auto_trading = models.BooleanField()

class result(models.Model):
    trade_id = models.OneToOneField(trade,on_delete=models.CASCADE,unique=True)
    trade_result = models.TextField()
    trade_summery = models.TextField()

    def __str__(self):
        return str('trade_id')
