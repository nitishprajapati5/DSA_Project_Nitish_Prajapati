from django.shortcuts import render,redirect
from django.utils import timezone
from django.contrib import messages
from .models import Train, TrainLog,TrainStation,PriorityTrainQueue
from django.db.models import Q
# Create your views here.

def train_board(request,station_code=None):
    stations = TrainStation.objects.all()
    print(stations)
    selected_station = None
    upcoming_trains = []
    departed_trains = []

    if station_code:
        selected_station = TrainStation.objects.get(code=station_code)

        #Create Queue for Upcoming Trains
        queue = PriorityTrainQueue()
        upcoming = Train.objects.filter(
            current_station=selected_station,
            scheduled_departure__gt=timezone.now(),
            status__in=['SCHEDULED', 'ARRIVING', 'AT_STATION']
        )

        for t in upcoming:
            queue.push(t)


        while not queue.is_empty():
            upcoming_trains.append(queue.pop())

        departed_trains = Train.objects.filter(
            current_station=selected_station,
            actual_departure__isnull=False,
            status='DEPARTED'
        ).order_by('-actual_departure')[:10]

    return render(request, 'train_scheduler/train_board.html', {
        'stations': stations,
        'selected_station': selected_station,
        'upcoming_trains': upcoming_trains,
        'departed_trains': departed_trains,
    })  

def update_train_status(request, train_id):
    print(train_id)
    train = Train.objects.get(id=train_id)
    print(train)
    current_time = timezone.now()
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status == 'ARRIVING':
            train.status = 'ARRIVING'
            train.delay_minutes = max(0, int((current_time - train.scheduled_arrival).total_seconds() / 60))
        elif new_status == 'AT_STATION':
            train.status = 'AT_STATION'
            train.actual_arrival = current_time
        elif new_status == 'DEPARTED':
            train.status = 'DEPARTED'
            train.actual_departure = current_time
        
        train.save()
        
        # Log the event
        TrainLog.objects.create(
            train=train,
            event_type=new_status,
            description=f"Train status updated to {new_status}"
        )
        
        messages.success(request, f"Train {train.train_number} status updated to {new_status}")
    print(train.current_station.code)
    return redirect('station_board',train.current_station.code)
