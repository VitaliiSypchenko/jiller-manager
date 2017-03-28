import json
import subprocess
import os
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.template.loader import render_to_string

from company.models import Company


def payment_notification(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        sender.session['payment_status'] = True
        data = json.loads(ipn_obj.custom)
        company, created = Company.objects.get_or_create(
            name=data['name'], admin_name=data['admin_name'], admin_pass=data['admin_pass']
        )
        if created:
            with open('compose_files/{}_docker_compose.yml'.format(company.name), 'w+') as f:
                compose = render_to_string('docker-compose-statndard.tmpl', {'name': company.name})
                f.write(compose)
            subprocess.call(
                "docker-compose -f compose_files/{}_docker_compose.yml up -d".format(company.name),
                shell=True
            )
            os.environ['COMPANY_NAME'] = company.name

valid_ipn_received.connect(payment_notification)
