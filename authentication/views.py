from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            login(request, form.save())
            return redirect('auctions:list')
    else:
        form = UserCreationForm()
    return render(request, 'authentication/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            login(request, form.get_user())

            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('auctions:list')
    else:
        form = AuthenticationForm()
    return render(request, 'authentication/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('authentication:login')
