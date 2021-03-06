import json
import subprocess
import os
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.template.loader import render_to_string
from company.models import Company
from twilio.rest import TwilioRestClient
from django.contrib.auth.hashers import make_password

ACCOUNT_SID = "AC0df4f762f288d92b23ebc4b51d54c098"
AUTH_TOKEN = "1770400f1d504900d614bb38ac97f7fd"

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

def payment_notification(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        data = json.loads(ipn_obj.custom)
        company, created = Company.objects.get_or_create(
            name=data['name'], admin_name=data['admin_name'], admin_pass=data['admin_pass']
        )
        if created:
            with open('../../Jillerenv/Jiller/project/fixtures/init_data1.json', 'w+') as h:
                init_data = render_to_string('init_data1.json', {'admin_name': company.admin_name, 'admin_pass': make_password(company.admin_pass)})
                h.write(init_data)
            with open('compose_files/{}_docker_compose.yml'.format(company.name), 'w+') as f:
                compose = render_to_string('docker-compose-statndard.tmpl', {'name': company.name})
                f.write(compose)
            subprocess.call(
                "docker-compose -f compose_files/{}_docker_compose.yml up -d".format(company.name),
                shell=True
            )
            os.environ['COMPANY_NAME'] = company.name
            message = client.messages.create(
                to="+15005550007",
                from_="+15005550006",
                body="Congratulations, {1}, you registered your own Jiller! Your credentials are:"
                     " Your Jiller url: {0}.jiller.com , Your login: {1}, Your pass: {2}".format(company.name,
                                                                                                 company.admin_name,
                                                                                                 company.admin_pass),
            )
            import logging
            # Get an instance of a logger
            logger = logging.getLogger(__name__)
            logger.error(message.sid)
            logger.error(str(message))

            # print(message.sid)
            # print(message)

valid_ipn_received.connect(payment_notification)