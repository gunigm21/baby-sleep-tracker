from django.shortcuts import render, redirect,get_object_or_404
from .models import SleepSession
from .forms import SleepSessionForm
from django.db import models
from django.db.models import F, DurationField, ExpressionWrapper, Sum
from django.db.models.functions import TruncDate
from django.http import JsonResponse
from datetime import timedelta

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
    sessions = SleepSession.objects.all()
    aggregated = (
        sessions
        .annotate(date=TruncDate('start_time'))
        .values('date')
        .annotate(total_sleep=Sum(models.ExpressionWrapper(models.F('end_time') - models.F('start_time'), output_field=models.DurationField())))
        .order_by('date')
    )

    labels = [entry['date'].strftime('%d.%m') for entry in aggregated]
    data = [round(entry['total_sleep'].total_seconds() / 3600, 2) for entry in aggregated]

    return render(request, 'sleep/chart.html', {
        'labels': labels,
        'data': data,
    })