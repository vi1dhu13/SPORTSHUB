from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse 
from .models import Events 
 
# Create your views here.
def indexee(request):  
    all_events = Events.objects.all()
    context = {
        "events":all_events,
    }
    return render(request,'indexee.html',context)
 
def all_events(request):                                                                                                 
    all_events = Events.objects.all()                                                                                    
    out = []                                                                                                             
    for event in all_events:                                                                                             
        out.append({                                                                                                     
            'title': event.name,                                                                                         
            'id': event.id,                                                                                              
            'start': event.start.strftime("%m/%d/%Y, %H:%M:%S"),                                                         
            'end': event.end.strftime("%m/%d/%Y, %H:%M:%S"),                                                             
        })                                                                                                               
                                                                                                                      
    return JsonResponse(out, safe=False) 
 
def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    event = Events(name=str(title), start=start, end=end)
    event.save()
    data = {}
    return JsonResponse(data)
 
def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.start = start
    event.end = end
    event.name = title
    event.save()
    data = {}
    return JsonResponse(data)
 
def remove(request):
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data)


# views.py
from django.shortcuts import render
from .models import DailyEvents
from Members.models import FitnessTrainer, FitnessUser
from Training.models import Workout
from django.http import JsonResponse

def calendar_view(request):
    trainers = FitnessTrainer.objects.all()
    clients = FitnessUser.objects.all()
    workouts = Workout.objects.all()

    context = {
        'trainers': trainers,
        'clients': clients,
        'workouts': workouts,
    }

    return render(request, 'calendar_view.html', context)

def save_daily_event(request):
    if request.method == 'POST':
        trainer_id = request.POST.get('trainer')
        client_id = request.POST.get('client')
        workout_ids = request.POST.getlist('workouts[]')
        start = request.POST.get('start')
        end = request.POST.get('end')

        trainer = FitnessTrainer.objects.get(pk=trainer_id)
        client = FitnessUser.objects.get(pk=client_id)
        workouts = Workout.objects.filter(pk__in=workout_ids)

        daily_event = DailyEvents(
            trainer=trainer,
            fitness_user=client,
            start=start,
            end=end,
            name="Daily Event",  # You may customize the name as needed
        )
        daily_event.save()
        daily_event.workouts.set(workouts)

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})

# views.py
from django.shortcuts import render, redirect
from .models import DailyEvents
from .forms import WorkoutForm
from Members.models import FitnessUser
# views.py
from django.shortcuts import render, redirect
from .models import DailyEvents
from .forms import WorkoutForm
from Members.models import FitnessUser
from django.shortcuts import render, redirect
from .forms import WorkoutForm
from .models import DailyEvents, FitnessUser, Workout,FitnessTrainer

from django.shortcuts import render, redirect
from .forms import WorkoutForm
from .models import DailyEvents, FitnessUser, Workout

from django.shortcuts import render, redirect
from .forms import WorkoutForm
from .models import DailyEvents, FitnessUser, Workout

from django.shortcuts import render, redirect
from .forms import WorkoutForm  # Import the WorkoutForm
from .models import FitnessUser, DailyEvents  # Import your models

from django.shortcuts import render, redirect
from .forms import WorkoutForm
from django.shortcuts import render, redirect
from .forms import WorkoutForm
from .models import FitnessUser, DailyEvents, Workout
from django.shortcuts import render, redirect
from .forms import WorkoutForm
from .models import FitnessUser, DailyEvents, Workout

def save_workouts_for_client(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST)

        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            workout_ids = form.cleaned_data['workouts']
            client_id = form.cleaned_data['client'].id

            client = FitnessUser.objects.get(pk=client_id)

            try:
                daily_event = DailyEvents.objects.create(
                    name="Client Workout",
                    start=start_date,
                    end=end_date,
                    trainer=request.user,  # Use request.user directly as the FitnessTrainer instance
                    fitness_user=client
                )
                daily_event.workouts.set(workout_ids)
            except Exception as e:
                print(f"Exception during saving: {e}")
                return render(request, 'save_workouts.html', {'form': form, 'error_message': 'Error during saving'})

            return redirect('client_workouts', client_id=client.id)
    else:
        form = WorkoutForm()

    return render(request, 'save_workouts.html', {'form': form})






def client_workouts(request):
    # Access the client_id from the session
    client_id = request.session.get('client_id', None)

    # Your logic to display client workouts based on client_id
    # ...

    return render(request, 'client_workouts.html', {'client_id': client_id})



