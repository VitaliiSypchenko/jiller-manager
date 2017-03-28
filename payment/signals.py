from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from company.forms import CreateCompanyForm
from django.contrib.auth.hashers import make_password
import json


def PaymentNotification(sender, **kwargs):
    ipn_obj = sender
    print type(ipn_obj.custom)
    print ipn_obj.custom
    print ipn_obj.payment_status
    # data = json.loads(ipn_obj.custom)
    # print data.get("admin_name", None)
    # form = CreateCompanyForm(data)
    # form.save(commit=False)
    # print form
    # form.admin_pass = make_password(data.get('admin_pass'))
    # print make_password(data.get('admin_pass'))
    # print form.admin_pass
    # form.save()
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        data = json.loads(ipn_obj.custom)
        form = CreateCompanyForm(data)
        form.save(commit=False)
        form.admin_pass = make_password(data.get('admin_pass'))
        form.save()

valid_ipn_received.connect(PaymentNotification)
