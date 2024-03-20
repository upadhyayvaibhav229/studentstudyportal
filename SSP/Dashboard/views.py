from django.shortcuts import render, redirect, get_object_or_404
from langchain import Wikipedia
import requests
from .forms import *
from .forms import DashboardForm
from .models import *
from django.contrib import messages
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from youtubesearchpython import VideosSearch
from .forms import UserRegistrationForm
from django.core.exceptions import ObjectDoesNotExist
import requests
from django.http import JsonResponse
import wikipedia
from .forms import ConversionForms, ConversionLengthForm, ConversionMassForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required



# Create your views here.


@login_required
def home(request):
    return render(request,'dashboard/home.html')

@login_required
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

@login_required
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

@login_required
def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    homework.is_finished = not homework.is_finished
    homework.save()
    return redirect('homework')

@login_required
def delete_homework(request, pk=None):
    homework = Homework.objects.get(id=pk).delete()
    return redirect('homework')

@login_required
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

@login_required
def todo(request):
    if request.method == 'POST':
        form = Todoform(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False

            todo = Todo(
                user = request.user,
                title = request.POST['title'],
                is_finished = finished
            )
            todo.save()
            messages.success(request, f'submitted sucessfully{request.user.username}!!')

    
    form = Todoform()
    todos = Todo.objects.filter(user=request.user)
    if len(todos) == 0:
        todo_done = True
    else:
        todo_done = False
    context = {
        'todos': todos,
        'form': form,
        'todo_done': todo_done
    }
    return render(request, 'dashboard/todo.html', context)

@login_required
def update_todo(request, pk=None):
    todo = Todo.objects.get(id = pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect('todo')

@login_required
def delete_todo(request, pk = None):
    Todo.objects.get(id = pk).delete()
    return redirect('todo')

@login_required
def books(request):
    form = DashboardForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        text = form.cleaned_data.get('text')
        url = "https://books.google.com/ebooks?id=buc0AAAAMAAJ&dq=holmes&as_brr=4&source=webstore_bookcard--" + text
        r = requests.get(url)
        answer = r.json()

        if 'items' in answer:
            result_list = []
            for item in answer['items'][:10]:
                volume_info = item.get('volumeInfo', {})
                result_dict = {
                    'title': volume_info.get('title', 'No title available'),
                    'subtitle': volume_info.get('subtitle', ''),
                    'description': volume_info.get('description', 'No description available'),
                    'count': volume_info.get('count', 'Not available'),
                    'category': volume_info.get('categories', []),
                    'rating': volume_info.get('averageRating', 'Not available'),
                    'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail', ''),
                    'preview': volume_info.get('previewLink', '')
                }
                result_list.append(result_dict)

            context = {'form': form, 'results': result_list}
            return render(request, 'dashboard/books.html', context)
        else:
            error_message = "No books found for the given search."
            context = {'form': form, 'error_message': error_message}
            return render(request, 'dashboard/books.html', context)

    context = {'form': form}
    return render(request, 'dashboard/books.html', context)
   


@login_required
def dictionary(request):
    if request.method == "POST":
        form = DashboardForm()

        text = request.POST.get('text', '')  # Use get method to avoid KeyError
        url = "http://api.dictionaryapi.dev/api/v2/entries/en_US/"+ text
        r = requests.get(url)
        
        if r.status_code == 200:
            try:
                answer = r.json()
                phonetics = answer[0]['phonetics'][0]['text']
                audio = answer[0]['phonetics'][0]['audio']
                definition = answer[0]['meanings'][0]['definitions'][0]['definition']
                example = answer[0]['meanings'][0]['definitions'][0].get('example', '')
                synonyms = answer[0]['meanings'][0]['definitions'][0].get('synonyms', '')
                
                context = {
                    'form': form,
                    'input': text,
                    'phonetics': phonetics,
                    'audio': audio,
                    'definition': definition,
                    'example': example,
                    'synonyms': synonyms,
                }
            except (KeyError, IndexError) as e:
                context = {
                    'form': form,
                    'input': text,
                    'error_message': 'Invalid response format from the dictionary API.'
                }
        else:
            context = {
                'form': form,
                'input': text,
                'error_message': f'Request failed with status code {r.status_code}.'
            }
            
        return render(request, 'dashboard/dictionary.html', context)
    else:
        form = DashboardForm()
        context = {
            'form': form
        }
        return render(request, 'dashboard/dictionary.html', context)

@login_required
def wiki(request):
    if request.method == 'POST':
        text = request.POST['text']
        form = DashboardForm(request.POST)
        search = wikipedia.page(text)
        context= {
            'form': form,
            'title': search.title,
            'link': search.url,
            'details': search.summary

        }
        return render(request, 'dashboard/wiki.html', context)
    else:    
        form = DashboardForm()
        context = {
            'form': form
        }
    return render(request, 'dashboard/wiki.html', context)



@login_required
def conversion(request):
    if request.method == 'POST':
        forms = ConversionForms(request.POST)
        measurement = request.POST.get('measurement')
        if measurement:
            if measurement == 'length':
                measurement_form = ConversionLengthForm()
                context = {
                    'forms': forms,
                    'm_form': measurement_form,  # Change 'm_forms' to 'm_form'
                    'input': True,
                }
                answer = ''
                if request.POST.get('input') and request.POST.get('measure1') and request.POST.get('measure2'):
                    first = request.POST['measure1']
                    second = request.POST['measure2']
                    input_value = float(request.POST['input'])
                    if input_value >= 0:
                        if first == 'yard' and second == 'foot':
                            answer = f'{input_value} yard = {input_value * 3} foot'
                        elif first == 'foot' and second == 'yard':
                            answer = f'{input_value} foot = {input_value / 3} yard'
                context['answer'] = answer
                
            elif measurement == 'mass':
                measurement_form = ConversionMassForm()
                context = {
                    'forms': forms,
                    'm_form': measurement_form,  # Change 'm_forms' to 'm_form'
                    'input': True,
                }
                answer = ''
                if request.POST.get('input') and request.POST.get('measure1') and request.POST.get('measure2'):
                    first = request.POST['measure1']
                    second = request.POST['measure2']
                    input_value = float(request.POST['input'])
                    if input_value >= 0:
                        if first == 'pound' and second == 'kilogram':
                            answer = f'{input_value} pound = {input_value * 0.453592} kilogram'
                        elif first == 'kilogram' and second == 'pound':
                            answer = f'{input_value} kilogram = {input_value * 2.20462} pound'
                context['answer'] = answer
                
        else:
            # Handle the case where 'measurement' doesn't exist in request.POST
            context = {
                'forms': forms,
                'input': False,
            }
    else:
        forms = ConversionForms()
        context = {
            'forms': forms,
            'input': False,
        }
    return render(request, 'dashboard/conversion.html', context)

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
    homeworks = Homework.objects.filter(user=request.user)
    todos = Todo.objects.filter(user=request.user)

    homework_done = all(homework.is_finished for homework in homeworks)
    todos_done = all(todo.is_finished for todo in todos)

    context = {
        'homeworks': homeworks,
        'todos': todos,
        'homework_done': homework_done,
        'todos_done': todos_done
    }
    return render(request, 'User/profile.html', context)
