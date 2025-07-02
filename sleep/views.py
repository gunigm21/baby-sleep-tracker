from django.shortcuts import render, redirect,get_object_or_404
from .models import SleepSession
from .forms import SleepSessionForm

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
