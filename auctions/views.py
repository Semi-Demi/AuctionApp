from datetime import timedelta
from urllib import request

from channels.layers import get_channel_layer
from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import JsonResponse, HttpResponse

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
                highestBidUpdate(auctionItem)
                return JsonResponse({'new_bid': auctionItem.current_bid})
        else:
            return JsonResponse({'error': 'You cannot bid on your own item.'})

    return render(request, 'auctions/auction_page.html', {'auction': auctionItem})


@login_required(login_url='/')
def auction_new(request):
    if request.method == 'POST':
        form = forms.CreateAuctionItem(request.POST, request.FILES)

        if form.is_valid():
            newAuction = form.save(commit=False)
            newAuction.seller = request.user

            print(newAuction.created_at)
            newAuction.expires_at = timezone.now() + timedelta(minutes=newAuction.time_limit)
            newAuction.active = True
            newAuction.save()
            print(newAuction.created_at)

            return redirect("auctions:list")
    else:
        form = forms.CreateAuctionItem()
    return render(request, 'auctions/auction_new.html', {'form': form})


def checkAuction(request, itemId):
    if request.method == 'GET':
        auctionItem = AuctionItem.objects.get(itemId=itemId)

        if auctionItem.highestBidder is None:
            auctionItem.expires_at = timezone.now() + timedelta(minutes=auctionItem.time_limit)
            auctionItem.active = True
            auctionItem.save()
            timeLeft = auctionItem.expires_at - timezone.now()

            timeLeftS = int(timeLeft.total_seconds()) % 60
            timeLeftM = timeLeftS // 60
            data = {"restart": "true", "timeM": timeLeftM, "timeS": timeLeftS}
            return JsonResponse(data)
        else:
            data = {"restart": "false"}
            return JsonResponse(data)


def calculateCountdown(request, itemId):
    auctionItem = AuctionItem.objects.get(itemId=itemId)
    timeLeft = auctionItem.expires_at - timezone.now()
    timeLeft = int(timeLeft.total_seconds())
    timeLeftS = timeLeft % 60
    timeLeftM = timeLeft // 60
    data = {"timeM": timeLeftM, "timeS": timeLeftS}
    return JsonResponse(data)


def setStatus(request, itemId):
    auctionItem = AuctionItem.objects.get(itemId=itemId)
    auctionItem.active = False
    auctionItem.save()
    return HttpResponse(status=200)


def highestBidUpdate(auctionItem):
    channel = get_channel_layer()
    message = {
        'bidder': str(auctionItem.highestBidder),
        'bid_price': str(auctionItem.current_bid),
        'auction_name': str(auctionItem.name),
        'auction_id': str(auctionItem.itemId),
        'remaining_time': str(auctionItem.expires_at - timezone.now())  # You can send the remaining time in seconds
    }
    channel.group_send('bids', {
        'type': 'send_notif',
        'message': message
    })

    print(message)
