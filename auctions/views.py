from datetime import timedelta

from django.shortcuts import render, redirect
from .models import AuctionItem
from django.contrib.auth.decorators import login_required
from . import forms


# Create your views here.
@login_required(login_url='/')
def auctions_list(request):
    auctions = AuctionItem.objects.all().order_by('-created_at')
    return render(request, 'auctions/auctions_list.html', {'auctions': auctions})


@login_required(login_url='/')
def auction_page(request, itemId):
    auctionItem = AuctionItem.objects.get(itemId=itemId)

    if request.method == 'POST':
        if auctionItem.seller != request.user:
            potentialBid = float(request.POST.get('bid'))
            if auctionItem.current_bid < potentialBid:
                auctionItem.current_bid = potentialBid
                auctionItem.highestBidder = request.user
                auctionItem.save()
                print("Bid updated")
        else:
            return render(request, 'auctions/auction_page.html', {'auction': auctionItem,'errorFlag': True, 'error': 'You cannot bid on your own item.'})

    return render(request, 'auctions/auction_page.html', {'auction': auctionItem})


@login_required(login_url='/')
def auction_new(request):
    if request.method == 'POST':
        form = forms.CreateAuctionItem(request.POST, request.FILES)

        if form.is_valid():
            newAuction = form.save(commit=False)
            newAuction.seller = request.user
            newAuction.save()
            print(newAuction.created_at)
            newAuction.expires_at = newAuction.created_at + timedelta(minutes=newAuction.time_limit)
            newAuction.active = True
            newAuction.save()
            return redirect("auctions:list")
    else:
        form = forms.CreateAuctionItem()
    return render(request, 'auctions/auction_new.html', {'form': form})