import datetime

from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractUser

# Create your models here.

class LogUser(AbstractUser):
    pass

class Serie(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(default=timezone.now)
    value_type = models.CharField(max_length=30)
    time_type = models.CharField(max_length=30)

    def was_created_recently(self):
      return self.created >= timezone.now() - datetime.timedelta(days=1)

    def as_dict(self):
      return {
        'name': self.name,
        'created': self.created.isoformat(),
        'value_type': self.value_type,
        'time_type': self.time_type
      }

    def values_as_list(self):
      data = self.datapoint_set.all()
      return [ p.as_dict() for p in data ]
    
    def __str__(self):
      return self.name

class DataPoint(models.Model):
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE)

    # values and times are stored as strings on purpose, to
    # make first implementation faster. Later, more specific
    # scheme for different datapoint types needs to be deviced.
    value = models.CharField(max_length=30)
    time = models.CharField(max_length=30)

    def get_time(self):
      if self.serie.time_type == "posix_us":
        return int(self.time)
      elif self.serie.time_type == "absolute":
        return int(self.value)
      elif self.serie.time_type == "ISO":
        return self.time
      
    def get_value(self):
      if self.serie.value_type == "float":
        return float(self.value)
      elif self.serie.value_type == "integer":
        return int(self.value)
      elif self.serie.value_type == "double":
        return float(self.value)
      elif self.serie.value_type == "string":
        return self.value 
    
    def as_dict(self):
      return {
        'id':self.id,
        'value':self.get_value(),
        'time':self.get_time()
      }
    
    def __str__(self):
        return "(" + self.time + ", " + self.value + ")"
