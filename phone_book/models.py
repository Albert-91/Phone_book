from django.core.validators import RegexValidator
from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    description = models.TextField()


class Phone(models.Model):
    types = (
        (1, "home"),
        (2, "business"),
        (3, "mobile")
    )
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'")
    phone_number = models.CharField(validators=[phone_regex], max_length=16)
    phone_type = models.IntegerField(choices=types, default=0)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)


class Address(models.Model):
    city = models.CharField(max_length=64)
    street = models.CharField(max_length=64)
    house_number = models.CharField(max_length=4)
    apartment_number = models.CharField(max_length=4)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)


class Email(models.Model):
    types = (
        (1, "home"),
        (2, "business"),
        (3, "mobile")
    )
    email_address = models.CharField(max_length=64)
    email_type = models.IntegerField(choices=types, default=0)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)


class Groups(models.Model):
    group_name = models.CharField(max_length=64)
    person = models.ManyToManyField(Person)


