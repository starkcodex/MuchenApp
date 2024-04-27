

from .models import Todo
from .forms import TodoForm
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


def get_showing_todos(request, todos): 
    if request.GET and request.GET.get('filter'):
        if request.GET.get('filter') == 'complete':
            return todos.filter(is_completed=True)
        if request.GET.get('filter') == 'incomplete':
            return todos.filter(is_completed=False)      
    return todos


@login_required
def index(request):
    todos=Todo.objects.filter(owner=request.user)
    completed_count = todos.filter(is_completed=True).count()
    incomplete_count = todos.filter(is_completed=False).count()
    all_count = todos.count()
    
    incomplete_count = todos.filter(is_completed=False).count()
    context = {'todos': get_showing_todos(request, todos), 'all_count': all_count,
                        'completed_count': completed_count, 'incomplete_count': incomplete_count}
    return render(request, 'ganz/index.html', context)


@login_required
def create_machen(request):
    form = TodoForm()
    context = {'form': form}
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        task_started = request.POST.get('task_started')
        task_ended = request.POST.get('task_ended')
        is_completed = request.POST.get('is_completed', False)
        
        todo = Todo()
        todo.title = title
        todo.description = description
        todo.task_started = task_started
        todo.task_ended = task_ended
        todo.is_completed = True if is_completed=='on' else False
        todo.owner =  request.user
        todo.save()
        
        messages.add_message(request, messages.SUCCESS, 'Muchen Created Succesfully !')
        
        return HttpResponseRedirect(reverse("todo", kwargs={'id': todo.pk}))
    return render(request, 'ganz/create-todo.html', context)


@login_required
def todo_detail(request, id):
    todo = get_object_or_404(Todo, pk=id)
    context = {'todo': todo}
    return render(request, 'ganz/todo-detail.html', context)


@login_required
def todo_delete(request, id):
    todo = get_object_or_404(Todo, pk=id)
    context = {'todo': todo}
    
    
    if request.method == 'POST':
        if todo.owner == request.user:
            todo.delete()
            messages.add_message(request, messages.WARNING, 
                                    'Muchen Deleted Succesfully !')
            return HttpResponseRedirect(reverse('home'))
        return render(request, 'ganz/todo-delete.html', context)
    return render(request, 'ganz/todo-delete.html', context)


@login_required
def todo_edit(request, id):
    todo = get_object_or_404(Todo, pk=id)
    form = TodoForm(instance=todo)
    context = {'todo':todo, 'form':form}
    
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        task_started = request.POST.get('task_started')
        task_ended = request.POST.get('task_ended')
        is_completed = request.POST.get('is_completed', False)
        
        todo.title = title
        todo.description = description
        todo.task_started = task_started
        todo.task_ended = task_ended
        todo.is_completed = True if is_completed=='on' else False
        
        if todo.owner == request.user:
            todo.save()
        
        messages.add_message(request, messages.SUCCESS, 'Muchen Updated Succesfully !')
    
        return HttpResponseRedirect(reverse("todo", kwargs={'id': todo.pk}))
    return render(request, 'ganz/todo-edit.html', context)