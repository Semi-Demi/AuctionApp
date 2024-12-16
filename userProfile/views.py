from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from auctions.models import AuctionItem

from authentication.views import logout_view
import auctions.views
from auctions.models import AuctionItem

@login_required(login_url='/')
def profile_view(request):
    errorFlag = False
    if request.method == 'GET':
        auctions = AuctionItem.objects.filter(seller=request.user, active=True)
        bids = AuctionItem.objects.filter(highestBidder=request.user, active=True)
        finishedAuctions = AuctionItem.objects.filter(active=False)
        auctionsWon = []

        for auction in finishedAuctions:
            if auction.highestBidder == request.user:
                auctionsWon.append(auction)

        return render(request, 'userProfile/profile.html',
                      {'auctions': auctions, 'bids': bids, 'auctionsWon': auctionsWon, 'user': request.user})

    elif request.method == 'POST':
        auctions = AuctionItem.objects.filter(seller=request.user, active=True)
        bids = AuctionItem.objects.filter(highestBidder=request.user, active=True)
        finishedAuctions = AuctionItem.objects.filter(active=False)
        auctionsWon = []

        for auction in finishedAuctions:
            if auction.highestBidder == request.user:
                auctionsWon.append(auction)

        if bids or auctions:
            print("Cant delete account")
            return render(request, 'userProfile/profile.html', {'auctions': auctions, 'bids': bids, 'auctionsWon': auctionsWon, 'user': request.user,'errorFlag': True,
                                                                'error': 'You cannot delete your account as you have an active auction or a winning bid on an active auctions.'})
        else:
            request.user.delete()
            return logout_view(request)
