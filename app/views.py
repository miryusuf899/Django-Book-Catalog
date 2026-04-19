from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from django.core.mail import send_mail
from .models import Category, Author, Book, Review, UserModel
import uuid


def book_list(request):
    # Оптимизация по ТЗ (пункт 10)
    books = Book.objects.all().select_related('author', 'category')
    
    # Поиск по названию (пункт 8: icontains)
    title = request.GET.get('title')
    if title:
        books = books.filter(title__icontains=title)
        
    # Фильтры (пункт 8: категория и автор)
    cat_id = request.GET.get('category')
    if cat_id:
        books = books.filter(category_id=cat_id)
        
    auth_id = request.GET.get('author')
    if auth_id:
        books = books.filter(author_id=auth_id)
        
    # Lookup fields (пункт 8: gte, lte)
    min_p = request.GET.get('min_price')
    if min_p:
        books = books.filter(price__gte=min_p)
    
    max_p = request.GET.get('max_price')
    if max_p:
        books = books.filter(price__lte=max_p)

    # Исключение данных (пункт 8: exclude)
    books = books.exclude(price__lte=0)

    context = {
        'books': books,
        'categories': Category.objects.all(),
        'authors': Author.objects.all(),
    }
    return render(request, 'book/book_list.html', context)

# --- 9, 10. Детали книги (ORM: prefetch_related, get_object_or_404) ---
def book_detail(request, pk):
    # prefetch_related для отзывов (пункт 10)
    # Через book.review_set.all в шаблоне покажем Reverse Relation (пункт 9)
    book = get_object_or_404(Book.objects.prefetch_related('review_set'), pk=pk)
    return render(request, 'book/book_detail.html', {'book': book})

# --- 7, 12. CRUD: Создание (Только для авторизованных) ---
def create_book(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        cover = request.FILES.get('cover_image')
        author = get_object_or_404(Author, pk=request.POST.get('author'))
        category = get_object_or_404(Category, pk=request.POST.get('category'))
        
        Book.objects.create(
            title=title,
            description=description,
            price=price,
            cover_image=cover,
            author=author,
            category=category,
            created_by_id=user_id
        )
        return redirect('book_list')

    authors = Author.objects.all()  # Получаем всех авторов
    categories = Category.objects.all() # Получаем все категории
    
    context = {
        'authors': authors,
        'categories': categories,
    }
    return render(request, 'book/book_create.html', context)

# --- 7, 12. CRUD: Обновление (Только автор или админ) ---
def book_update(request, pk):
    user_id = request.session.get('user_id')
    book = get_object_or_404(Book, pk=pk)

    if not user_id or (book.created_by_id != user_id):
        return redirect('book_list')

    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.description = request.POST.get('description')
        book.price = request.POST.get('price')
        if request.FILES.get('cover_image'):
            book.cover_image = request.FILES.get('cover_image')
        book.author_id = request.POST.get('author')
        book.category_id = request.POST.get('category')
        book.save()
        return redirect('book_detail', pk=book.pk)
    
    context = {
        'book': book,
        'authors': Author.objects.all(),
        'categories': Category.objects.all()
    }
    return render(request, 'book/book_update.html', context)

# --- 7, 12. CRUD: Удаление ---
def book_delete(request, pk):
    user_id = request.session.get('user_id')
    book = get_object_or_404(Book, pk=pk)

    if not user_id or (book.created_by_id != user_id):
        return redirect('book_list')

    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'book/book_delete.html', {'book': book})

# --- 11. Статистика (ORM: aggregate, annotate) ---
def aggregate_view(request):
    book_stats = Book.objects.aggregate(
        total_books=models.Count('id'),
        average_price=models.Avg('price'),
        max_price=models.Max('price'),
        min_price=models.Min('price'),
    )
    # Количество книг у каждого автора (annotate)
    authors = Author.objects.annotate(
        num_books=models.Count('book')
    )
    return render(request, 'stats.html', {'stats': book_stats, 'authors': authors})

# --- 12, 13. Регистрация и подтверждение Email ---
def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = UserModel(email=email, username=username)
        user.set_password(password)
        user.save()

        link = f"http://127.0.0.1:8000/verify/{user.email_token}/"
        send_mail(
            'Verify your email',
            f'Click the link to verify your email: {link}',
            None,
            [email]
        )
        return render(request, 'Registrations/login.html')

    return render(request, 'Registrations/register.html')

def verify_email(request, token):
    user = get_object_or_404(UserModel, email_token=token)
    user.is_active = True
    user.save()
    return redirect('login')

# --- 12. Логин и Логаут ---
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = UserModel.objects.filter(email=email).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                return render(request, 'Registrations/login.html', {'error': 'Verify email!'})
            request.session['user_id'] = user.id
            return redirect('book_list')
            
    return render(request, 'Registrations/login.html')

def logout_view(request):
    request.session.flush()
    return redirect('login')

# --- 14. Смена и сброс пароля ---
def change_password(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    
    user = UserModel.objects.get(id=user_id)
    if request.method == 'POST':
        old = request.POST.get('old_password')
        new = request.POST.get('new_password')
        if user.check_password(old):
            user.set_password(new)
            user.save()
            return redirect('book_list')
            
    return render(request, 'Registrations/change_password.html')

def reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = UserModel.objects.filter(email=email).first()
        if user:
            user.reset_token == uuid.uuid4()
            user.save()
            link = f"http://127.0.0.1:8000/reset-confirm/{user.reset_token}/"
            send_mail('Reset Password', f'Link: {link}',None, [email])
        return render(request, 'Registrations/email_sent.html')
    return render(request, 'Registrations/reset_request.html')

def reset_confirm(request, token):
    user = get_object_or_404(UserModel, reset_token=token)

    if not user:
        return redirect('login')
    
    if request.method == 'POST':
        new_password = request.POST['password']
        user.set_password(new_password)
        user.reset_token = None
        user.save()
        return redirect('login')
    return render(request, 'Registrations/reset_confirm.html')

def home(request):
    user = request.session.get('user_id')
    if not user:
        return redirect('login')
    data = {'data': get_object_or_404(UserModel, id=user)}
    return render(request, 'home.html', data)