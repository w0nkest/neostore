from django.shortcuts import render, redirect
from .forms import ThingsForm
from home.models import Thing

def display(request):
    things = Thing.objects.all()
    return render(request, 'things/shop.html', {'things': things})


def add(request):
    error = ''
    if request.method == 'POST':
        form = ThingsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('display')
        else:
            print(form.errors)
            print()
            print(form)
            error = 'Данные не верны!'

    form = ThingsForm()
    data = {'form': form, 'error': error}
    return render(request, 'things/adder.html', data)