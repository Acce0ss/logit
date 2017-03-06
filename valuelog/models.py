import datetime

from django.core.exceptions import ValidationError

from django.db import models, transaction
from django.utils import timezone,dateparse

from django.conf import settings

from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass

class LogUserManager(models.Manager):
    def validate_and_create_user(self, username, email, password):
        newuser = LogUser()
        
        with transaction.atomic():
            baseuser = User(username=username, email=email)
            baseuser.set_password(password)
            baseuser.full_clean()
            baseuser.save()
        
            newuser.user = baseuser
            newuser.full_clean()
            newuser.save()

        return newuser

class LogUser(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    objects = LogUserManager()

class Serie(models.Model):

    VALUE_TYPE = (
        ('flt', 'Float'),
        ('int', 'Integer'),
        ('str', 'String'),
        ('dbl', 'Double')
    )

    TIME_TYPE = (
        ('psx', 'POSIX'),
        ('iso', 'ISO'),
        ('abs', 'Absolute')
    )

    owner = models.ForeignKey(LogUser, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=200)
    created = models.DateTimeField(default=timezone.now)
    value_type = models.CharField(max_length=3, choices=VALUE_TYPE)
    time_type = models.CharField(max_length=3, choices=TIME_TYPE)

    def was_created_recently(self):
      return self.created >= timezone.now() - datetime.timedelta(days=1)

    def as_dict(self):
      return {
        'id': self.id,
        'name': self.name,
        'created': self.created.isoformat(),
        'value_type': self.value_type,
        'time_type': self.time_type,
        'owner': self.owner.id
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
    value = models.CharField(max_length=40)
    time = models.CharField(max_length=40)

    def type_check(target):
        def _type_check(value):
            try:
                if target(value) is None:
                    return False
                return True
            except (ValueError, TypeError):
                return False
        return _type_check
    
    VALIDATE_TIME = {
        'psx': type_check(int),
        'abs': type_check(int),
        'iso': type_check(dateparse.parse_datetime)
    }

    VALIDATE_VALUE = {
        'flt': type_check(float),
        'int': type_check(int),
        'dbl': type_check(float),
        'str': lambda t: True
    }
    
    def validate_value(self):
      if not self.VALIDATE_VALUE[self.serie.value_type](self.value):
        raise ValidationError({'value':'Invalid value'})

    def validate_time(self):
      if not self.VALIDATE_TIME[self.serie.time_type](self.time):
        raise ValidationError({'time':'Invalid time/date'})

    def get_time(self):
      if self.serie.time_type == "psx":
        return int(self.time)
      elif self.serie.time_type == "abs":
        return int(self.value)
      elif self.serie.time_type == "iso":
        return self.time
    
    def get_value(self):
      if self.serie.value_type == "flt":
        return float(self.value)
      elif self.serie.value_type == "int":
        return int(self.value)
      elif self.serie.value_type == "dbl":
        return float(self.value)
      elif self.serie.value_type == "str":
        return self.value 
    
    def as_dict(self):
      return {
        'id':self.id,
        'value':self.get_value(),
        'time':self.get_time()
      }
    
    def __str__(self):
        return "(" + self.time + ", " + self.value + ")"
