from django.db import models
from django.contrib.auth.models import AbstractUser


class Country(models.TextChoices):
    UKRAINE = 'UA', 'Ukraine'
    POLAND = 'POL', 'Poland'
    USA = 'USA', 'United States of America'
    CANADA = 'CAN', 'Canada'
    UK = 'UK', 'United Kingdom'
    FRANCE = 'FRA', 'France'
    GERMANY = 'GER', 'Germany'
    AUSTRALIA = 'AUS', 'Australia'


class User(AbstractUser):
    country = models.CharField(max_length=4, choices=Country.choices, default="UA")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class Transation(models.Model):
    sender = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, related_name="transations_sender")
    recipient = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, related_name="transations_getter")
    sum_of_transaction = models.DecimalField(max_digits=10, decimal_places=2)
    time_of_transaction = models.DateTimeField(auto_now_add=True)


class Auction(models.Model):
    creator = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, related_name="auctions")
    buyer = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, null=True, blank=True,
                              related_name="auctions_bought")
    start_price = models.DecimalField(max_digits=10, decimal_places=2)
    minimal_bet = models.DecimalField(max_digits=10, decimal_places=2)
    price_of_ransom = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    time_of_creation = models.DateTimeField(auto_now_add=True)
    time_of_start = models.DateTimeField()

    def __str__(self):
        return f"Auction: {self.time_of_start} - {self.creator}"


class Lot(models.Model):
    sender = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, related_name="lots")
    sum_of_bet = models.DecimalField(max_digits=10, decimal_places=2)
    time_of_lot = models.DateTimeField(auto_now_add=True)
    auction = models.ForeignKey(to=Auction, on_delete=models.DO_NOTHING)
    is_completed = models.BooleanField()
