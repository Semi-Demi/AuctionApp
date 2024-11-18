from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from auctions.models import AuctionItem

from authentication.views import logout_view


# Create your views here.
@login_required(login_url='/')
def profile_view(request):
    if request.method == 'GET':
        errorFlag = False
        return render(request, 'userProfile/profile.html')

    elif request.method == 'POST':
        if AuctionItem.objects.filter(seller=request.user,active=True).exists() or AuctionItem.objects.filter(highestBidder=request.user).exists():
            print("Cant delete account")
            return render(request, 'userProfile/profile.html', {'errorFlag': True,
                          'error': 'You cannot delete your account as you have an active auction or a winning bid on an active auctions.'})

        else:
            request.user.delete()
            return logout_view(request)
