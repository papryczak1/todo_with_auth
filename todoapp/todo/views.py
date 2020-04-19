from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def signupuser(request):
    form = UserCreationForm()
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signup.html', {'form': form, 'error': 'That username has already exists'})
        else:
            error = 'Password did not match.'
            return render(request, 'todo/signup.html', {'form': form, 'error':error})
    else:
        return render(request, 'todo/signup.html', {'form': form})

@login_required(login_url='loginuser')
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, dateCompleted__isnull=True)
    completeTodos = Todo.objects.filter(user=request.user, dateCompleted__isnull=False).order_by('-dateCompleted')
    context = {'todos': todos, 'completeTodos': completeTodos}
    return render(request, 'todo/todos.html', context)

@login_required(login_url='loginuser')
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('homepage')

def loginuser(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/login.html', {'form': form, 'error':'Username or password did not match.'})
        else:
            login(request, user)
            return redirect('currenttodos')
    else:
        return render(request, 'todo/login.html', {'form':form})


def homepage(request):
        if request.user.is_authenticated:
            return redirect('currenttodos')
        return render(request, 'todo/home.html')

@login_required(login_url='loginuser')
def createtodo(request):
    form = TodoForm()
    context = {'form': form}
    if request.method == 'POST':
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/create.html', {'form':form, 'error':'Bad data passed in'})
    else:
        return render(request, 'todo/create.html', context)

@login_required(login_url='loginuser')
def viewtodo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id, user=request.user)
    form = TodoForm(instance=todo)
    if request.method == 'POST':
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/view.html', {'todo': todo, 'form': form, 'error':'Bad info...'})
    else:
        return render(request, 'todo/view.html', {'todo': todo, 'form': form})

@login_required(login_url='loginuser')
def completetodo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id, user=request.user)
    if request.method == 'POST':
        todo.dateCompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required(login_url='loginuser')
def deletetodo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')
