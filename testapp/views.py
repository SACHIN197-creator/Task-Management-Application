from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from .models import Task
from .forms import TaskForm, RegisterForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

def home(request):

    return redirect('login')

def signup_view(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('login')

    else:

        form = RegisterForm()

    return render(
        request,
        'testapp/signup.html',
        {'form': form}
    )

@login_required(login_url='login')
def dashboard(request):

    tasks = Task.objects.filter(
        user=request.user
    )

    return render(
        request,
        'testapp/dashboard.html',
        {'tasks': tasks}
    )

@login_required(login_url='login')
def create_task(request):

    if request.method == 'POST':

        form = TaskForm(request.POST)

        if form.is_valid():

            task = form.save(commit=False)

            task.user = request.user

            task.save()

            return redirect('dashboard')

    else:

        form = TaskForm()

    return render(
        request,
        'testapp/create_task.html',
        {'form': form}
    )

@login_required(login_url='login')
def update_task(request, pk):

    task = get_object_or_404(
        Task,
        id=pk,
        user=request.user
    )

    if request.method == 'POST':

        form = TaskForm(
            request.POST,
            instance=task
        )

        if form.is_valid():

            form.save()

            return redirect('dashboard')

    else:

        form = TaskForm(instance=task)

    return render(
        request,
        'testapp/update_task.html',
        {'form': form}
    )

@login_required(login_url='login')
def delete_task(request, pk):

    task = get_object_or_404(
        Task,
        id=pk,
        user=request.user
    )

    task.delete()

    return redirect('dashboard')