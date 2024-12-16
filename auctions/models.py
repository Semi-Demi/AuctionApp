import uuid
from datetime import timezone, timedelta
from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.

class AuctionItem(models.Model):
    itemId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auctionItems')
    highestBidder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='highestBidder')

    name = models.CharField(max_length=100)
    description = models.TextField()
    picture = models.ImageField(upload_to='media')
    starting_bid = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    current_bid = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    time_limit = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    time_left = models.DateTimeField(default=timezone.now)

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name
