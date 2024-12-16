from datetime import timedelta

from asgiref.sync import async_to_sync
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
    auctions = AuctionItem.objects.all().order_by('-active')

    return render(request, 'auctions/auctions_list.html', {'auctions': auctions})


@login_required(login_url='/')
def auction_page(request, itemId):
    auctionItem = AuctionItem.objects.get(itemId=itemId)

    if request.method == 'POST':
        errorFlag = False

        try:
            if auctionItem.seller != request.user:
                potentialBid = float(request.POST.get('bid'))
                if auctionItem.current_bid < potentialBid:
                    auctionItem.current_bid = potentialBid
                    auctionItem.highestBidder = request.user
                    auctionItem.save()
                    print("Bid updated")
                    highestBidUpdate(auctionItem)
                elif auctionItem.current_bid >= potentialBid:
                    return render(request, 'auctions/auction_page.html',
                                  {'auction': auctionItem, 'errorFlag': True, 'error': 'Your bid is smaller than the current highest bid.'})
            else:
                return render(request, 'auctions/auction_page.html', {'auction': auctionItem, 'errorFlag': True, 'error': 'You cannot bid on your own item.'})
        except Exception:
            return render(request, 'auctions/auction_page.html',
                          {'auction': auctionItem, 'errorFlag': True, 'error': 'Your bid is too high! Please only bid 999 or less at a time'})

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
        print("checking")
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
        elif auctionItem.expires_at < timezone.now():
            setStatus(request, itemId)
            data = {"restart": "false"}
            return JsonResponse(data)


def calculateCountdown(request, itemId):
    auctionItem = AuctionItem.objects.get(itemId=itemId)
    timeLeft = auctionItem.expires_at - timezone.now()
    timeLeft = int(timeLeft.total_seconds())
    timeLeftS = timeLeft % 60
    timeLeftM = timeLeft // 60
    data = {"timeM": timeLeftM, "timeS": timeLeftS, 'highestBidder':  str(auctionItem.highestBidder), 'bid': str(auctionItem.current_bid)}
    return JsonResponse(data)


def setStatus(request, itemId):
    auctionItem = AuctionItem.objects.get(itemId=itemId)

    if not auctionItem.active:
        return HttpResponse(status=400)

    auctionItem.active = False
    auctionItem.save()

    channel = get_channel_layer()
    group = 'bids'
    event = {
        'bid_price': str(auctionItem.current_bid),
        'bidder_name': str(auctionItem.highestBidder),
        'auction_name': str(auctionItem.name),
        'auction_ID': str(auctionItem.itemId)
    }

    async_to_sync(channel.group_send)(
        group,
        {
            'type': 'send_winner',
            'message': event
        }
    )
    return HttpResponse(status=200)


def highestBidUpdate(auctionItem):
    channel = get_channel_layer()
    group = 'bids'
    event = {
        'bid_price': str(auctionItem.current_bid),
        'remaining_time': str(auctionItem.expires_at - timezone.now()),  # You can send the remaining time in seconds
        'bidder_name': str(auctionItem.highestBidder),
        'auction_name': str(auctionItem.name),
        'auction_ID': str(auctionItem.itemId)
    }

    async_to_sync(channel.group_send)(
        group,
        {
            'type': 'send_notif',
            'message': event
        }
    )
