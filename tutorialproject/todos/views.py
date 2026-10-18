from django.shortcuts import redirect, render
from django.views import View
from django.http import HttpResponse, HttpResponseNotAllowed
from .forms import PersonForm, TodoForm
from .models import Todo

import requests
# Create your views here.
class HelloWorldView(View):
    def get(self, request):
        return HttpResponse("Hello, World!")

class HelloPythonView(View):
    def get(self, request):
        return HttpResponse("Hello, Python!")


class HelloHTMLView(View):
    def get(self, request):
        return render(request, 'todos/hello.html', {'message': 'Hello, HTML! From the .py'})


class HelloPath(View):
    def get(self, request, num1, num2):
        return HttpResponse(f"Hello, {num1} and {num2} = {num1 + num2}!")

class HelloQuery(View):
    def get(self, request):
        return HttpResponse(f"Your query was {request.GET.get('query', 'No query provided')}")


class SpecialView(View):
    def get(self, request):
        return redirect('hello-html')


class PostExample(View):
    def post(self, request):
        if request.method == 'POST':
            form = PersonForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                age = form.cleaned_data['age']
                job = form.cleaned_data['job']
                return HttpResponse(f"Name: {name}, Age: {age}, Job: {job}")
            else:
                return HttpResponse("Invalid form data")
        else:
            return HttpResponseNotAllowed(['POST'])


class SubmitExample(View):
    def get(self, request):
        return render(request, 'todos/submit.html')

class SubmitDjangoForm(View):
    def get(self, request):
        form = PersonForm()
        return render(request, 'todos/submit-django-form.html', {'form': form})


class TemplateView(View):
    def get(self, request):
        context = {
            "name": "Mike",
            "age": 30,
            "skills": ["Python", "JavaScript"],
        }
        return render(request, 'todos/template-demo.html', context)


class TodosView(View):
    def get(self, request):
        form = TodoForm()
        todos = Todo.objects.all()
        return render(request, 'todos/todos.html', {'todos': todos, 'form': form})

    def post(self, request):
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save()
            return HttpResponse(f"Todo created: {todo.title}")
