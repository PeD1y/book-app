from django.db import models

#import
import uuid 
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
    Username and password are required. Other fields are optional.
    """
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=False)
    last_name = models.CharField(_('last name'), max_length=150, blank=False)
    email = models.EmailField(_('email address'), blank=False)
    borrow = models.BooleanField(default=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        #abstract = True #削除していないといけない

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)                                                      

class Category(models.Model):
    name = models.CharField('カテゴリ名',max_length=255, unique=True)

    def __str__(self):
        return self.name

#class BorrowNotification(models.Model):

class Book(models.Model):
    # 識別ID
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    
    # User情報
    lend_user = models.ForeignKey(User,on_delete=models.CASCADE) #貸出user 
    #borrow_user = models.OneToOneField(Borrow,on_delete=models.PROTECT,related_name='borrow_user',null=True,blank=True) #借出user
    #削除したアカウントの復元機能を実装する場合は、models.PROTECTがいいと思う   
    
    #書籍情報
    book_title = models.CharField(max_length=255) #題名
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='カテゴリ',blank=False)  #カテゴリ
    author_name = models.CharField(max_length=255,blank=True) #著者
    description = models.TextField(max_length=255,blank=True) #フレーズ
    created_at = models.DateTimeField('更新日',auto_now_add=True) #作成日
    #publishedDate = models.DateTimeField(max_length=12,blank=True) #出版日
    
    #貸出情報
    lend = models.BooleanField(default=True) #貸出判定
    user_name = models.CharField(max_length=255,blank=True) #借出希望user
    user_email= models.CharField(max_length=255,blank=True) #userメール
    
    def __str__(self):
        return self.book_title

