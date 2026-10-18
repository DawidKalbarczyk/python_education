from django.urls import path
from .views import HelloHTMLView, HelloPath, HelloQuery, HelloWorldView, HelloPythonView, PostExample, SpecialView, SubmitDjangoForm, SubmitExample, TemplateView, TodosView

urlpatterns = [
    path('hello', HelloWorldView.as_view(), name='hello-world'),
    path('', HelloPythonView.as_view(), name='hello-python'),
    path('html', HelloHTMLView.as_view(), name='hello-html'),
    path('add/<int:num1>/<int:num2>', HelloPath.as_view(), name='hello-path'),
    path('query', HelloQuery.as_view(), name='hello-query'),
    path('special', SpecialView.as_view(), name='special-view'),
    path('post-example', PostExample.as_view(), name='post-example'),
    path('submit-example', SubmitExample.as_view(), name='submit-example'),
    path('submit-django-form', SubmitDjangoForm.as_view(), name='submit-django-form'),
    path('template-demo', TemplateView.as_view(), name='template-demo'),
    path('todos', TodosView.as_view(), name='todos'),
]