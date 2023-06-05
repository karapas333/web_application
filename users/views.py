from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


def register(request):
    """ Регистрирует нового пользователя, если запрос GET """
    if request.method != 'POST':
        # представление пользователя без данных
        form = UserCreationForm()
    else:
        # обработка заполненной формы с данными POST
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # Выполнение входа и перенаправление на домашнюю страницу.

            login(request, new_user)
            return redirect('learning_logs:index')

    # Отображать пустую или недействительную форму
    context = {'form': form}
    return render(request, 'registration/register.html', context)
