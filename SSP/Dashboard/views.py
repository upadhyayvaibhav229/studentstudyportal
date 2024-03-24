from datetime import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from langchain import Wikipedia
import requests
from youtubesearchpython import VideosSearch
from .forms import NotesForm, HomeworkForm, DashboardForm, UserRegistrationForm, Todoform
from .models import Notes, Homework, Todo
from .forms import ConversionForms, ConversionLengthForm, ConversionMassForm
from .forms import ConversionMassForm

@login_required
def home(request):
    return render(request, 'dashboard/home.html')


# notes
@login_required
def notes(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            Notes.objects.create(user=request.user, title=form.cleaned_data['title'], desc=form.cleaned_data['desc'])
            messages.success(request, f"Notes added from {request.user.username} successfully")
            return redirect('notes')
    else:
        form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
    context = {'notes': notes, 'form': form}
    return render(request, 'dashboard/notes.html', context)

@login_required
def delete_notes(request, pk=None):
    note = get_object_or_404(Notes, id=pk)
    note.delete()
    return redirect('notes')

class NotesDetailView(generic.DetailView):
    model = Notes


# homework section
@login_required
def homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            Homework.objects.create(
                user=request.user,
                Subject=form.cleaned_data['Subject'],
                Title=form.cleaned_data['Title'],
                Description=form.cleaned_data['Description'],
                Due=form.cleaned_data['Due'],
                is_finished=form.cleaned_data.get('is_finished', False)
            )
            messages.success(request, f'Homework Added from {request.user.username}!!')
            return redirect('homework')
    else:
        form = HomeworkForm()
    homeworks = Homework.objects.filter(user=request.user)
    homework_done = not homeworks.exists()
    context = {'homeworks': homeworks, 'homeworks_done': homework_done, 'form': form}
    return render(request, 'dashboard/homework.html', context)

@login_required
def update_homework(request, pk=None):
    homework = get_object_or_404(Homework, id=pk)
    homework.is_finished = not homework.is_finished
    homework.save()
    return redirect('homework')

@login_required
def delete_homework(request, pk=None):
    homework = get_object_or_404(Homework, id=pk)
    homework.delete()
    return redirect('homework')


# youtube section
@login_required
def youtube(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            video = VideosSearch(text, limit=10)
            result_list = []
            for i in video.result()['result']:
                result_dict = {
                    'input': text,
                    'title': i.get('title', 'N/A'),
                    'duration': i.get('duration', 'N/A'),
                    'thumbnails': i.get('thumbnails', [{'url': 'N/A'}])[0]['url'],
                    'Channel': i.get('channel', {}).get('name', 'N/A'),
                    'Link': i.get('link', 'N/A'),
                    'viewcount': i.get('viewCount', {}).get('short', 'N/A'),
                    'publishedTime': i.get('publishedTime', 'N/A'),
                    'description': i.get('descriptionSnippet', '')
                }
                result_list.append(result_dict)
            context = {'form': form, 'results': result_list}
            return render(request, 'dashboard/youtube.html', context)
    else:
        form = DashboardForm()
    context = {'form': form}
    return render(request, 'dashboard/youtube.html', context)


# todo section

from django.contrib.auth.decorators import login_required
@login_required

@login_required
def todo(request):
    if request.method == 'POST':
        form = Todoform(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)  # Don't save immediately
            todo.user = request.user  # Assign the user to the todo
            todo.save()  # Save with the user assigned
            messages.success(request, f'Submitted successfully {request.user.username}!!')
            return redirect('todo')
    else:
        form = Todoform()
    todos = Todo.objects.filter(user=request.user)
    context = {'todos': todos, 'form': form}
    return render(request, 'dashboard/todo.html', context)
@login_required
def update_todo(request, pk=None):
    todo = get_object_or_404(Todo, id=pk)
    todo.is_finished = not todo.is_finished
    todo.save()
    return redirect('todo')

@login_required
def delete_todo(request, pk=None):
    todo = get_object_or_404(Todo, id=pk)
    todo.delete()
    return redirect('todo')


# dictionary section
def dictionary(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/" + text
        r = requests.get(url)
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0].get('example', '')

            # Extract synonyms properly
            synonyms = []
            meanings = answer[0].get('meanings', [])
            for meaning in meanings:
                for definition in meaning.get('definitions', []):
                    synonyms.extend(definition.get('synonyms', []))
                    
            context = {
                'form': form,
                'input': text,
                'phonetics': phonetics,
                'audio': audio,
                'definition': definition,
                'example': example,
                'synonyms': ', '.join(synonyms)  # Join synonyms into a single string
            }
        except:
            context = {
                'form': form,
                'input': '',
            }
        return render(request, 'dashboard/dictionary.html', context)
    else:
        form = DashboardForm()
        context = {
            'form': form
        }
        return render(request, 'dashboard/dictionary.html', context)


# books section
def books(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q=" + text  # Fix the URL
        r = requests.get(url)
        answer = r.json()
        result_list = []

        # Check if 'items' key exists in the JSON response
        if 'items' in answer:
            for item in answer['items']:
                result_dict = {
                    'title': item['volumeInfo'].get('title', ''),
                    'subtitle': item['volumeInfo'].get('subtitle', ''),
                    'description': item['volumeInfo'].get('description', ''),
                    'count': item['volumeInfo'].get('count', ''),
                    'categories': item['volumeInfo'].get('categories', ''),
                    'rating': item['volumeInfo'].get('pageRating', ''),  # Fix this key
                    'thumbnail': item['volumeInfo'].get('imageLinks', {}).get('thumbnail', ''),  # Fix this key
                    'preview': item['volumeInfo'].get('previewLink', ''),  # Fix this key
                }
                result_list.append(result_dict)

            context = {
                'form': form,
                'results': result_list
            }
            return render(request, 'dashboard/books.html', context)
        else:
            error_message = "No results found"
            context = {
                'form': form,
                'error_message': error_message
            }
            return render(request, 'dashboard/books.html', context)
    else:
        form = DashboardForm()
        context = {'form': form}
        return render(request, 'dashboard/books.html', context)


# wiki section
import wikipedia

def wiki(request):
    if request.method == 'POST':
        text = request.POST['text']
        form = DashboardForm(request.POST)
        search = wikipedia.page(text)
        context = {
            'form': form,
            'title': search.title,
            'link': search.url,
            'details': search.summary
        }
        return render(request, 'dashboard/wiki.html', context)

    form = DashboardForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/wiki.html', context)


# conversion
def conversion(request):
    context = {}  # Initialize context here
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

# register and sigin section
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}!!")
            return redirect("login")
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'User/register.html', context)

# profile
@login_required
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


