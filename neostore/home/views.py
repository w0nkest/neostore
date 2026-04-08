from django.shortcuts import render, HttpResponse, redirect

def redirect_to_home(request):
    return redirect('home')

def home(request):
    return render(request, 'home/home.html')

def register(request):
    return render(request, 'home/register.html')
