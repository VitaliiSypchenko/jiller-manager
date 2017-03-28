from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.urlresolvers import reverse
from paypal.standard.forms import PayPalPaymentsForm

from company.forms import CreateCompanyForm


def payment_process(request):
    form = CreateCompanyForm()
    if request.method == 'POST':
        host = request.get_host()

        form = CreateCompanyForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name'].lower()
            admin_name = form.cleaned_data['admin_name']
            admin_pass = form.cleaned_data['admin_pass']

            paypal_dict = {
                'business': settings.PAYPAL_RECEIVER_EMAIL,
                'amount': '15',
                'item_name': 'jiller',
                'invoice': name,
                'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
                'return_url': 'http://{}{}'.format(host, reverse('payment:done')),
                'cancel_return': 'http://{}{}'.format(host, reverse('payment:canceled')),
                'custom': "{" + "\"name\": \"" + name + "\"," +
                          "\"admin_name\": \"" + admin_name + "\"," +
                          "\"admin_pass\": \"" + admin_pass + "\"}"
            }

            form = PayPalPaymentsForm(initial=paypal_dict)
            return render(request, 'payment/process.html', {
                # 'order':order,
                'form':form})

    return render(request, 'home.html', {'form': form,})


@csrf_exempt
def payment_done(request):
    return render(request, 'payment/done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/canceled.html')
