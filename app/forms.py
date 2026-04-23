from django import forms
from .models import Book, UserModel

class BookForm(forms.ModelForm):
    # Явное объявление полей для гибкой настройки
    title = forms.CharField(
        label="Название книги",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите название книги'
        })
    )
    
    description = forms.CharField(
        label="Описание",
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Краткое содержание...',
            'rows': 4
        })
    )
    
    price = forms.DecimalField(
        label="Цена",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00',
            'step': '0.01'
        })
    )

    class Meta:
        model = Book
        fields = ['title', 'description', 'price', 'cover_image', 'author', 'category']
        
        # Настройка стилей для ForeignKey и файлов
        widgets = {
            'author': forms.Select(attrs={
                'class': 'form-control',
                'style': 'background-color: #0f172a; color: white;'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
                'style': 'background-color: #0f172a; color: white;'
            }),
            'cover_image': forms.FileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*'
            }),
        }

    # Валидация цены
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Цена должна быть больше нуля!")
        return price
    

class UserForm(forms.ModelForm):
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )
    
    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    
    email = forms.EmailField(
        label="Email",
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.com'})
    )
    
    phone_number = forms.CharField(
        label="Телефон",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7...'})
    )

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'phone_number', 'password']

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone and not phone.startswith('+'):
            raise forms.ValidationError("Номер телефона должен начинаться с '+'")
        return phone
    
class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",  # ТУТ ДОЛЖНО БЫТЬ USERNAME
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter your username', # И ТУТ
            'autofocus': True
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': '••••••••'
        })
    )


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'you@example.com',
            'autofocus': True
        })
    )

# Форма для установки нового пароля
class SetNewPasswordForm(forms.Form):
    password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'At least 8 characters',
            'autofocus': True
        })
    )

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '••••••••'
        })
    )
    new_password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'At least 8 characters'
        })
    )
