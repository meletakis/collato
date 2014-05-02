from Todo.models import *
from django.forms import ModelForm


class TodoListForm(ModelForm):
  class Meta:
    model = TodoList
    fields = ['name','description','source_code_host',]


class TodoItemForm(ModelForm):
  class Meta:
    model = TodoItem
    fields = ['data_type','name','description']		
    exclude = ('app',)
