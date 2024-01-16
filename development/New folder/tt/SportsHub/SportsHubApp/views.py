from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.shortcuts import render
from Members.models import TrainingPlanAssignment

from django.shortcuts import render
from django.urls import reverse
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

razorpay_client = razorpay.Client(
auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def index(request):
    return render(request, 'index.html')
    
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
   

from django.shortcuts import render
from django.views.generic import ListView
from .models import SportsCenter,Payment

class SportsCenterListView(ListView):
    model = SportsCenter
    template_name = 'sports_center_list.html'
    context_object_name = 'sports_centers'
from django.shortcuts import render, get_object_or_404, redirect
from .models import SportsCenter, SportscenterSlot, Reservation


def select_slot(request, sports_center_id):
    try:
        sportscenter = SportsCenter.objects.get(id=sports_center_id)
    except SportsCenter.DoesNotExist:
        return render(request, 'sportscenter_not_found.html')

    if request.method == 'POST':
        selected_slot_id = request.POST.get('slot_id')
        reservation_date = request.POST.get('reservation_date')

        try:
            selected_slot = SportscenterSlot.objects.get(id=selected_slot_id)

            reservation = Reservation(
                reserver=request.user if request.user.is_authenticated else None,
                sport=sportscenter,
                slot=selected_slot,
                reservation_date=reservation_date,
            )
            reservation.save()

            # Redirect to the payment view with the reservation_id
            return redirect('payment_reservation', reservation_id=reservation.id)

        except SportscenterSlot.DoesNotExist:
            return HttpResponse('Selected slot not found', status=400)  # Return an error response

    return render(request, 'select_slot.html', {
        'sportscenter': sportscenter,
    })



from django.http import JsonResponse
from datetime import datetime

def get_available_slots(request, sportscenter_id, selected_date):
    try:
        sportscenter = SportsCenter.objects.get(id=sportscenter_id)
    except SportsCenter.DoesNotExist:
        return JsonResponse({'error': 'Sports center not found'}, status=404)

    try:
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)

    # Get available slots for the selected sports center and date
    reservations_for_sportscenter = Reservation.objects.filter(sport=sportscenter, reservation_date=selected_date,status=True)
    reserved_slot_ids = reservations_for_sportscenter.values_list('slot__id', flat=True)
    available_slots = SportscenterSlot.objects.exclude(id__in=reserved_slot_ids)

    # Serialize the available slots to JSON
    data = [{'id': slot.id, 'start_time': str(slot.start_time), 'end_time': str(slot.end_time)} for slot in available_slots]

    return JsonResponse({'available_slots': data})

razorpay_client = razorpay.Client(
auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def payment(request, reservation_id=None, assignment_id=None):
    # Determine whether to create a Reservation payment or a Subscription payment
    if reservation_id:
        # Handle payment for reservation
        reservation = get_object_or_404(Reservation, pk=reservation_id)
        amount = reservation.sport.price_per_slot
        description = f"Payment for Reservation - {reservation.id}"

        # For Razorpay integration
        currency = 'INR'
        amount_in_paise = int(amount * 100)

        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(
            amount=amount_in_paise,
            currency=currency,
            payment_capture='0'  # Capture payment manually after verifying it
        ))

        # Order ID of the newly created order
        razorpay_order_id = razorpay_order['id']
        callback_url = reverse('paymenthandler_reservation', args=[reservation_id])

        # Create a Payment record for reservation
        payment = Payment.objects.create(
            user=request.user,
            razorpay_order_id=razorpay_order_id,
            amount=amount,
            currency=currency,
            payment_status=Payment.PaymentStatusChoices.PENDING,
            reservation=reservation  # Associate payment with reservation
        )

        # Prepare the context data
        context = {
            'user': request.user,
            'order1': reservation,
            'razorpay_order_id': razorpay_order_id,
            'razorpay_merchant_key': settings.RAZOR_KEY_ID,
            'razorpay_amount': amount,
            'currency': currency,
            'description': description,
            'callback_url': callback_url,
        }

        return render(request, 'Payment.html', context)

    elif assignment_id:
        # Handle payment for assignment
        assignment = get_object_or_404(TrainingPlanAssignment, pk=assignment_id)
        amount = assignment.plan.amount
        description = f"Payment for Assignment - {assignment.id}"

        # For Razorpay integration
        currency = 'INR'
        amount_in_paise = int(amount * 100)

        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(
            amount=amount_in_paise,
            currency=currency,
            payment_capture='0'  # Capture payment manually after verifying it
        ))

        # Order ID of the newly created order
        razorpay_order_id = razorpay_order['id']
        callback_url = reverse('paymenthandler_assignment', args=[assignment_id])

        # Create a Payment record for assignment
        payment = Payment.objects.create(
            user=request.user,
            razorpay_order_id=razorpay_order_id,
            amount=amount,
            currency=currency,
            payment_status=Payment.PaymentStatusChoices.PENDING,
            TrainingPlanAssignment=assignment  # Associate payment with assignment
        )

        # Prepare the context data
        context = {
            'user': request.user,
            'order2': assignment,
            'razorpay_order_id': razorpay_order_id,
            'razorpay_merchant_key': settings.RAZOR_KEY_ID,
            'razorpay_amount': amount,
            'currency': currency,
            'description': description,
            'callback_url': callback_url,
        }

        return render(request, 'Payment.html', context)

    else:
        # Handle the case where neither reservation_id nor assignment_id is provided
        return HttpResponse("Invalid request")



@csrf_exempt
def paymenthandler(request, reservation_id=None, assignment_id=None):
    # Only accept POST requests.
    if request.method == "POST":
        # Get the required parameters from the POST request.
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        # Verify the payment signature.
        result = razorpay_client.utility.verify_payment_signature(params_dict)

        payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
        amount = int(payment.amount * 100)  # Convert Decimal to paise

        # Capture the payment.
        razorpay_client.payment.capture(payment_id, amount)

        # Update the order with payment ID and change status to "Successful."
        payment.payment_id = payment_id
        payment.payment_status = Payment.PaymentStatusChoices.SUCCESSFUL
        payment.save()

        if reservation_id:
            # Update the Reservation status to True.
            reservation = Reservation.objects.get(id=reservation_id)
            reservation.status = True
            reservation.save()
        elif assignment_id:
            # Update the Assignment status to True.
            assignment = TrainingPlanAssignment.objects.get(id=assignment_id)
            assignment.is_accepted = True
            assignment.save()

        # Render the success page on successful capture of payment.
        return render(request, 'index.html')

    else:
        # If other than POST request is made.
        return HttpResponseBadRequest()
    

from django.http import JsonResponse
from django.db.models import Sum
from .models import Reservation

def get_reservation_data(request):
    reservations_info = Reservation.objects.values(
        'sport__name',
    ).annotate(
        total_amount=Sum('payment__amount'),
        reservation_count=Count('id'),
    )

    data = {
        'sports_center_names': [info['sport__name'] for info in reservations_info],
        'total_amounts': [info['total_amount'] or 0 for info in reservations_info],
        'reservation_counts': [info['reservation_count'] for info in reservations_info],
    }

    return JsonResponse(data, safe=False)
