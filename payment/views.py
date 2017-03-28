import json
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
            return render(request, 'payment/process.html', {'form':form})

    return render(request, 'home.html', {'form': form,})


def paypal_payment_successful(sender, **kwargs):
    #Called when the payment is sucessful
    ipn_obj = sender
    user_id = ipn_obj.custom

    if ipn_obj.payment_status == "Completed":
        try:
            user_profile = models.UserProfile.objects.get(user=user_id)
            user_profile.account_balance += float(ipn_obj.mc_gross)
            user_profile.save()

        except models.UserProfile.DoesNotExist:
            pass # TODO email admin


@csrf_exempt
def payment_done(sender, **kwargs):
    ipn_obj = sender
    data = json.loads(ipn_obj.custom)

    return render(sender, 'payment/done.html', {'data': data})


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/canceled.html')
