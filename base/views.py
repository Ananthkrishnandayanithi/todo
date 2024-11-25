from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Task
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect  # Add this import



class CustomLoginView(LoginView):
    template_name= 'base/login.html'
    model =  Task
    fields= '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('task-list')
    

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filter tasks to include only those for the current user
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        # Count the tasks where 'complex' is False
        context['task_count'] = context['tasks'].filter(complex=False).count()
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__icontains=search_input  # Corrected the lookup
            )
        return context


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task-list')  # Redirect to task list after successful registration

    def form_valid(self, form):
        # Save the user and log them in automatically
        user = form.save()
        if user:
            login(self.request, user)  # Log the user in
        return super().form_valid(form)

    def get(self, *args, **kwargs):
        # If the user is already authenticated, redirect them to the task list
        if self.request.user.is_authenticated:
            return redirect('task-list')
        return super().get(*args, **kwargs)

class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('task-list')
    template_name = 'base/task.html'

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete', 'complex']  # Exclude 'user' from fields
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.user = self.request.user  # Associate the task with the logged-in user
        return super().form_valid(form)
    

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model =  Task
    fields= ['title', 'description', 'complete', 'complex']
    success_url = reverse_lazy('task-list')
class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('task-list')  # Redirect to task list after successful deletion
    template_name = 'base/task_confirm_delete.html'  # Ensure the correct template is used