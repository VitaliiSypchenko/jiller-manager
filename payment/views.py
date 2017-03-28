import json
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from company.models import Company


@csrf_exempt
def payment_done(request):
    print request.session.get('payment_status')
    print request.session.get('company')
    company = request.session.get('company')
    try:
        current_company = Company.objects.get(name=company)
    except Company.DoesNotExist:
        return render(request, 'payment/done.html')

    return render(request, 'payment/done.html', {'company': current_company})


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/canceled.html')
