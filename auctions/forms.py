from django import forms
from . import models


class CreateAuctionItem(forms.ModelForm):
    class Meta:
        model = models.AuctionItem
        fields = ['name', 'description', 'starting_bid', 'time_limit', 'picture']
