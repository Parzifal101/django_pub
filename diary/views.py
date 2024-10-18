from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Task, Profile
from django.contrib.auth.decorators import login_required
from .forms import TaskForm, ProfileForm

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'diary/category_list.html', {'categories': categories})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    tasks = Task.objects.filter(category=category)
    return render(request, 'diary/category_detail.html', {'category': category, 'tasks': tasks})

@login_required
def task_create(request):
    category_id = request.GET.get('category')
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            return redirect('category_detail', slug=task.category.slug)
    else:
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            form = TaskForm(initial={'category': category})
        else:
            form = TaskForm()
    return render(request, 'diary/task_form.html', {'form': form})

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            return redirect('category_detail', slug=task.category.slug)
    else:
        form = TaskForm(instance=task)
    return render(request, 'diary/task_form.html', {'form': form, 'task': task})

@login_required
def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.is_completed = True
    task.save()
    return redirect('category_detail', slug=task.category.slug)

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'diary/profile.html', {'form': form})