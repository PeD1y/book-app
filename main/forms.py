from django import forms
from .models import User,Book,Category
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

class SignUpForm(UserCreationForm):
    last_name = forms.CharField(
        max_length=30,
        label='苗字'
    )
    first_name = forms.CharField(
        max_length=30,
        label='名前'
    )
    email = forms.EmailField(
        max_length=255,
        label='Eメールアドレス'
    )
    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name',  'email', 'password1', 'password2', )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class LendBookForm(forms.Form):
    isbn_code = forms.CharField(
        max_length=13,
        required=True,
        label='ISBNコード',
        help_text='書籍裏に記載の978から始まるコードを入力してください'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['name'] ="keyword"

class PreviewForm(forms.ModelForm):
    book_title = forms.CharField(
            max_length=30,
            label='タイトル',
        )
    category = forms.ModelChoiceField(
        label = 'カテゴリー', 
        required = True,
        help_text = 'カテゴリを選択してください',
        queryset = Category.objects.all())
    author_name = forms.CharField(
            max_length=30,
            label='著者',            
        )
    description = forms.CharField(
        max_length=255,
        label = '説明',
        widget = forms.Textarea(attrs={'class' : 'input'})
    )
    
    class Meta:
        model = Book
        fields = ('book_title','category','author_name','description',)
        exclude = ('lend_user','borrow_user','lend','created_at')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['name'] ="keyword"

class PostSearchForm(forms.Form):
    key_word = forms.CharField(
        label = 'キーワード', required = False,
        widget = forms.TextInput(attrs={'class' : 'input'})
    )
    book = forms.ModelChoiceField(
        label = '投稿者', required = False,
        queryset = Book.objects.all()
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control mr-sm-2'
            field.widget.attrs['type'] ="search"
            field.widget.attrs['placeholder'] ="本を探す..."
            field.widget.attrs['aria-label'] ="本を探す..."

