from django.db import models
# from django.utils import timezone
# from datetime import datetime, timedelta
import heapq

class TrainStation(models.Model):
    name = models.CharField(max_length=100,default="")
    code = models.CharField(max_length=10, unique=True)
    platforms = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Train(models.Model):
    TRAIN_TYPES = [
        ('EXPRESS', 'Express Train'),
        ('PASSENGER', 'Passenger Train'),
        ('FREIGHT', 'Freight Train'),
    ]
    
    PRIORITY_LEVELS = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
    ]
    
    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('ARRIVING', 'Arriving'),
        ('AT_STATION', 'At Station'),
        ('DEPARTED', 'Departed'),
        ('DELAYED', 'Delayed'),
        ('CANCELLED', 'Cancelled'),
    ]

    train_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    train_types = models.CharField(max_length=20, choices=TRAIN_TYPES)
    priority = models.IntegerField(choices=PRIORITY_LEVELS, default=2)
    current_station = models.ForeignKey(
        TrainStation, 
        on_delete=models.CASCADE,
        related_name='current_trains'
    )
    platform = models.IntegerField()
    scheduled_arrival = models.DateTimeField()
    scheduled_departure = models.DateTimeField()
    actual_arrival = models.DateTimeField(null=True, blank=True)
    actual_departure = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES,
        default='SCHEDULED'
    )
    delay_minutes = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.train_number} - {self.name}"

    class Meta:
        ordering = ['scheduled_arrival']

class PriorityTrainQueue:
    def __init__(self):
        self.queue = []
        self._index = 0  # For maintaining FIFO order within same priority
    
    def push(self, train):
        # Lower number means higher priority
        priority_score = (
            -train.priority,  # Negative for max-heap behavior
            train.scheduled_arrival,
            self._index
        )
        heapq.heappush(self.queue, (priority_score, train))
        self._index += 1
    
    def pop(self):
        if self.queue:
            return heapq.heappop(self.queue)[1]
        return None
    
    def peek(self):
        if self.queue:
            return self.queue[0][1]
        return None
    
    def is_empty(self):
        return len(self.queue) == 0

class TrainLog(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    event_type = models.CharField(max_length=50)
    description = models.TextField()
    
    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.train.name} {self.event_type}"
