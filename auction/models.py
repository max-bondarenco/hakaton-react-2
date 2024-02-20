import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    avatar = models.ImageField(
        upload_to="media/avatars",
        default="media/avatars/default_user.png"
    )
    phone = models.CharField(max_length=14, default=0)


class Transation(models.Model):
    sender = models.ForeignKey(
        to=User,
        on_delete=models.DO_NOTHING,
        related_name="transations_sender"
    )
    recipient = models.ForeignKey(
        to=User,
        on_delete=models.DO_NOTHING,
        related_name="transations_getter"
    )
    sum_of_transaction = models.DecimalField(max_digits=15, decimal_places=2)
    time_of_transaction = models.DateTimeField(auto_now_add=True)


class Auction(models.Model):
    name = models.CharField(max_length=255, default="Auction")
    description = models.TextField(blank=True, null=True, max_length=700)
    image = models.ImageField(
        upload_to="auction-images/",
        blank=True,
        null=True
    )
    creator = models.ForeignKey(
        to=User,
        on_delete=models.DO_NOTHING,
        related_name="auctions"
    )

    current_better = models.ForeignKey(
        to=User,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="auctions_betters"
    )
    start_price = models.DecimalField(max_digits=15, decimal_places=2)
    minimal_bet = models.DecimalField(max_digits=15, decimal_places=2)
    current_bet = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )
    price_of_ransom = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True
    )
    time_of_creation = models.DateTimeField(auto_now_add=True)
    time_of_start = models.DateTimeField()
    seconds_to_end = models.IntegerField(default=60)
    is_completed = models.BooleanField(default=False)
    participants = models.ManyToManyField(User)

    class Meta:
        ordering = ["-time_of_start"]

    def __str__(self):
        return f"{self.name} {self.time_of_start}"

    def start_time_value(self):
        return datetime.datetime.strftime(
            self.time_of_start,
            "%Y-%m-%dT%H:%M"
        )

    def str_date(self):
        return datetime.datetime.strftime(
            self.time_of_start,
            "%m/%d/%Y, %H:%M:%S"
        )


class Lot(models.Model):
    sender = models.ForeignKey(
        to=User,
        on_delete=models.DO_NOTHING,
        related_name="lots"
    )
    sum_of_bet = models.DecimalField(max_digits=15, decimal_places=2)
    time_of_lot = models.DateTimeField(auto_now_add=True)
    auction = models.ForeignKey(to=Auction, on_delete=models.DO_NOTHING)
    is_completed = models.BooleanField()

    def str_date(self):
        return datetime.datetime.strftime(self.time_of_lot, "%H:%M:%S")

class Auction2(models.Model):
    name = models.CharField(max_length=255, default="Auction")
    description = models.TextField(blank=True, null=True, max_length=700)
    start_price = models.DecimalField(max_digits=15, decimal_places=2)
    minimal_bet = models.DecimalField(max_digits=15, decimal_places=2)
    price_of_ransom = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True
    )
    time_of_creation = models.DateTimeField(auto_now_add=True)
    time_of_start = models.DateTimeField(null=True)
