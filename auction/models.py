from django.db import models
from django.contrib.auth.models import AbstractUser

# countries = ["Ukraine", "Poland", "Slovakia", "Estonia", "Spain",]


class User(AbstractUser):
    # country = models.TextChoices()
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class Lot(models.Model):
    sender = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, related_name="lots")
    # getter = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, related_name="lots")
    sum_of_bet = models.DecimalField(max_digits=10, decimal_places=2)
    time_of_lot = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField()


class Transation(models.Model):
    sender = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, related_name="transations")
    # getter = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, related_name="transations")
    sum_of_transaction = models.DecimalField(max_digits=10, decimal_places=2)
    time_of_transaction = models.DateTimeField(auto_now_add=True)


class Auction(models.Model):
    creator = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, related_name="auctions")
    # buyer = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="auctions")
    start_price = models.DecimalField(max_digits=10, decimal_places=2)
    minimal_bet = models.DecimalField(max_digits=10, decimal_places=2)
    price_of_ransom = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    time_of_creation = models.DateTimeField(auto_now_add=True)
    time_of_start = models.DateTimeField()

    def __str__(self):
        return f"Auction: {self.time_of_start} - {self.creator}"
