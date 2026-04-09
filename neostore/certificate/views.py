from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CertificateForm


@login_required
def upload_certificate(request):
    error = ''
    if request.method == 'POST':
        form = CertificateForm(request.POST)
        if form.is_valid():
            cert = form.save(commit=False)
            cert.user = request.user
            cert.save()
            return redirect('user-profile')
        else:
            error = 'Wrong data!'

    form = CertificateForm()
    data = {'form': form, 'error': error}
    return render(request, 'certificate/upload.html', data)
