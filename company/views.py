import re

from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from company.forms import CreateCompanyForm
from company.models import Company


def home_view(request):
    form = CreateCompanyForm()
    if request.method == 'POST':
        form = CreateCompanyForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name'].lower()
            form.save(commit=False)
            form.name = name
            form.save()
            f = open('compose_files/{}_docker_compose.yml'.format(name), 'w+')
            data = render_to_string('docker_compose_standard.yml', {'name': name})
            f.write(data)
            f.close()
            return redirect(reverse('home'))


    return render(request, 'home.html', {'form': form,})
