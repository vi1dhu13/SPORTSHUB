from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.shortcuts import render
from .models import SportsCenter

from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

razorpay_client = razorpay.Client(
auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def index(request):
    
    if request.method == 'POST' and 'razorpay_payment_id' in request.POST:
        # Handle the Razorpay callback here if needed
        pass
    
    currency = 'INR'
    amount = 20000  # Rs. 200

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(
        amount=amount,
        currency=currency,
        payment_capture='0'
    ))

    # Order ID of the newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'

    # Pass these details to the frontend.
    context = {
        'user': request.user,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,
        'currency': currency,
        'callback_url': callback_url
    }

    return render(request, 'index.html', context=context)


def sports_center_list(request):
    sports_centers = SportsCenter.objects.all()
    return render(request, 'services.html', {'sports_centers': sports_centers})

def add_center(request):
    if request.method == 'POST':
        center_name = request.POST['center_name']
        center_location = request.POST['center_location']
        center_capacity = request.POST['center_capacity']
        
        # Create a new SportsCenter object
        center = SportsCenter.objects.create(
            name=center_name,
            location=center_location,
            capacity=center_capacity
        )
        
        # You can also add more fields and logic here if needed
        
        return redirect('services')  # Redirect to the services page after submission
    
    return render(request, 'services.html')



from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

razorpay_client = razorpay.Client(
auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
   
@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = 20000  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                    return render(request, 'paymentsuccess.html')
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:
 
                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()