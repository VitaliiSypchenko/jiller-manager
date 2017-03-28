from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from company.models import Company


@csrf_exempt
def payment_done(request):
    company = request.session.get('company')
    try:
        current_company = Company.objects.get(name=company)
    except Company.DoesNotExist:
        return render(request, 'payment/done.html')

    return render(request, 'payment/done.html', {'company': current_company})


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/canceled.html')
