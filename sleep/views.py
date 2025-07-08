from django.shortcuts import render, redirect,get_object_or_404
from .models import SleepSession
from .forms import SleepSessionForm
from django.db import models
from django.db.models import F, DurationField, ExpressionWrapper, Sum
from django.db.models.functions import TruncDate
from django.http import JsonResponse
from datetime import timedelta
from collections import defaultdict

def sleep_list(request):
    sessions = SleepSession.objects.order_by('-start_time')
    return render(request, 'sleep/list.html', {'sessions': sessions})

def sleep_add(request):
    if request.method == 'POST':
        form = SleepSessionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sleep_list')
    else:
        form = SleepSessionForm()
    return render(request, 'sleep/add.html', {'form': form})

def sleep_edit(request, pk):
    session = get_object_or_404(SleepSession, pk=pk)
    if request.method == 'POST':
        form = SleepSessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            return redirect('sleep_list')
    else:
        form = SleepSessionForm(instance=session)
    return render(request, 'sleep/edit.html', {'form': form, 'session': session})

def sleep_delete(request, pk):
    session = get_object_or_404(SleepSession, pk=pk)
    if request.method == 'POST':
        session.delete()
        return redirect('sleep_list')
    return render(request, 'sleep/delete.html', {'session': session})

def sleep_chart(request):
    sessions = SleepSession.objects.all().order_by('start_time')

    sleep_by_date = defaultdict(timedelta)

    for session in sessions:
        date = session.start_time.date()
        duration = session.end_time - session.start_time
        sleep_by_date[date] += duration

    dates = [date.strftime('%Y-%m-%d') for date in sorted(sleep_by_date)]
    durations_hours = [round(sleep_by_date[date].total_seconds() / 3600, 2) for date in sorted(sleep_by_date)]

    context = {
        'dates': dates,
        'durations': durations_hours,
    }

    return render(request, 'sleep/chart.html', context)