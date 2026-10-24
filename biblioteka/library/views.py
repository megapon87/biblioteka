from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Book, SavedBook
from .forms import RegisterForm, LoginForm


def home(request):
    query = request.GET.get('q', '').strip()

    if query:
        books = list(Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        ))
        shelves = None
    else:
        books = list(Book.objects.all())
        shelf_size = 5
        shelves = [books[i:i + shelf_size] for i in range(0, len(books), shelf_size)]

    saved_ids = set()
    if request.user.is_authenticated:
        saved_ids = set(
            SavedBook.objects.filter(user=request.user).values_list('book_id', flat=True)
        )

    return render(request, 'home.html', {
        'shelves': shelves,
        'search_results': books if query else None,
        'query': query,
        'total': Book.objects.count(),
        'saved_ids': saved_ids,
    })


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    is_saved = False
    if request.user.is_authenticated:
        is_saved = SavedBook.objects.filter(user=request.user, book=book).exists()
    return render(request, 'book_detail.html', {'book': book, 'is_saved': is_saved})


@login_required
def toggle_save(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    saved, created = SavedBook.objects.get_or_create(user=request.user, book=book)
    if not created:
        saved.delete()
    next_url = request.POST.get('next')
    if next_url == 'home':
        return redirect('home')
    return redirect('book_detail', book_id=book.id)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data.get('email', ''),
                password=form.cleaned_data['password1'],
            )
            login(request, user)
            return redirect('profile')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('profile')
            form.add_error(None, 'Невірний логін або пароль')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def profile(request):
    saved_books = Book.objects.filter(saved_by__user=request.user).order_by('-saved_by__saved_at')
    return render(request, 'profile.html', {'saved_books': saved_books})
