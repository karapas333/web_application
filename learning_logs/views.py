from django.shortcuts import render, redirect

from .models import Topic, Entry
from .forms import TopicForm, EntryForms
from django.contrib.auth.decorators import login_required
from django.http import Http404


def index(request):
    """Домашняя страница приложения Learning Log"""
    return render(request, "learning_logs/index.html")


@login_required
def topics(request):
    """Выводит список тем."""
    topics = Topic.objects.filter(owner=request.user).order_by("date_added")
    context = {"topics": topics}
    return render(request, "learning_logs/topics.html", context)


@login_required
def topic(request, topic_id):
    """Выводит одну тему и все её записи."""
    topic = Topic.objects.get(id=topic_id)

    # Проверка того, что тема принадлежит текущему пользователю.
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by("-date_added")
    context = {"topic": topic, "entries": entries}
    return render(request, "learning_logs/topic.html", context)


@login_required
def new_topic(request):
    """Добавляет новую тему."""
    if (request.method != 'POST' and request.method == "GET"):
        # Вернуть пустую форму, если нет данных POST
        form = TopicForm()
    else:
        form = TopicForm(data = request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()

            # form.save()
            return redirect('learning_logs:topics')
    # Отображает пустую форму.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Добавляет новую запись для конкретной темы."""
    topic = Topic.objects.get(id=topic_id)
    if (request.method != 'POST' and request.method == 'GET'):
        form = EntryForms()
    else:
        form = EntryForms(data = request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Редактирует существующую запись."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if topic.owner != request.user:
        raise Http404

    if (request.method != 'POST' and request.method == 'GET'):
        form = EntryForms(instance=entry)
    else:
        form = EntryForms(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("learning_logs:topic", topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)