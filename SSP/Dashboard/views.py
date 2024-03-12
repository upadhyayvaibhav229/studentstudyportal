from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .forms import DashboardForm
from .models import *
from django.contrib import messages
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from youtubesearchpython import VideosSearch
from .forms import UserRegistrationForm




# Create your views here.



def home(request):
    return render(request,'dashboard/home.html')

def notes(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user = request.user, title = request.POST['title'], desc = request.POST['desc'])
            notes.save()
        messages.success(request,f"Notes added from {request.user.username} successfuly")

    else:
        form = NotesForm()

    #--> login user , when user login user name passed then user able to retireve the data from the notes
    
    notes = Notes.objects.filter(user = request.user) 
    context = {
    'notes': notes,
    'form':form
}
    return render(request, 'dashboard/notes.html',context)

def delete_notes(request, pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect('notes')

class NotesDetailView(generic.DetailView):
    model = Notes


def homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            finished = request.POST.get('is_finished', False) == 'on'
            homeworks = Homework(
                user=request.user,
                Subject=request.POST['Subject'],
                Title=request.POST['Title'],
                Description=request.POST['Description'],
                Due=request.POST['Due'],
                is_finished=finished
            )
            homeworks.save()
            messages.success(request, f'Homework Added from {request.user.username}!!')
            return redirect('homework')
    else:
        form = HomeworkForm()
    homeworks = Homework.objects.filter(user=request.user)
    homework_done = not homeworks.exists()
    context = {
        'homeworks': homeworks,
        'homeworks_done': homework_done,
        'form': form,
    }
    return render(request, 'dashboard/homework.html', context)

def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    homework.is_finished = not homework.is_finished
    homework.save()
    return redirect('homework')

def delete_homework(request, pk=None):
    homework = Homework.objects.get(id=pk).delete()
    return redirect('homework')


def youtube(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST.get('text', '')
        video = VideosSearch(text, limit = 10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input': text,
                    'title': i.get('title', 'N/A'),
                    'duration': i.get('duration', 'N/A'),
                    'thumbnails': i.get('thumbnails', [{'url': 'N/A'}])[0]['url'],
                    'Channel': i.get('Channel', {}).get('Name', 'N/A'),
                    'Link': i.get('Link', 'N/A'),
                    'viewcount': i.get('viewcount', {}).get('short', 'N/A'),
                    'publishedTime': i.get('publishedTime', 'N/A'),
                
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
            context = {

                'form': form,
                'results': result_list
            }
            
        return render(request, 'dashboard/youtube.html', context)

    

    else:
        form = DashboardForm()
    context= {
        'form': form
    }

    return render(request, 'dashboard/youtube.html', context)




def todo(request):
    if request.method == 'POST':
        todo_id = request.POST.get('todo_id')
        todo = Todo.objects.get(pk=todo_id)
        todo.is_finished = not todo.is_finished  # Toggle the status
        todo.save()
        return redirect('todo')  # Redirect back to the todo page
    
    form = Todoform()
    todos = Todo.objects.filter(user=request.user)
    
    context = {
        'todos': todos,
        'form': form,
    }
    return render(request, 'dashboard/todo.html', context)


# login and registration


def register(request):
    # bhakti
    # bha@12345
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}!!")
            return redirect("login")
            
      
    else:
        form = UserRegistrationForm()
    context = {
        'form':form
    }
    return render(request, 'User/register.html', context)

def profile(request):
    homeworks = Homework.objects.filter(is_finished=False, user=request.user)
    todos = Todo.objects.filter(is_finished=False, user=request.user)


    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False
    

    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False

    context = {
        'homeworks' : homeworks,
        'todos': todos,
        'homework_done' : homework_done,
        'todos_done' : todos_done
    }
    return render(request, 'User/profile.html', context)