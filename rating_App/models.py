from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class CustomUserTable(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email  # Use a more descriptive field for string representation
    
    class Meta:  
        db_table = 'CustomUserTable'


# class CustomUserAdmin(UserAdmin):
#     # Customize the display and behavior of the CustomUser model in the admin
#     list_display = ('username', 'email')
#     list_filter = ('is_superuser', 'groups')
#     search_fields = ('username', 'email')

class Music(models.Model):
    title = models.CharField(max_length=100)
    urls_file = models.FileField(upload_to='music_urls/')  # Removed default value
    created_at = models.DateTimeField(auto_now_add=True)
    is_automatic = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Rating(models.Model):
    RATING_CHOICES = (
        ('Terrible', 'Terrible'),
        ('Somehow Good', 'Somehow Good'),
        ('Good', 'Good'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ratings')
    music = models.ForeignKey(Music, on_delete=models.CASCADE, related_name='ratings')
    rating = models.CharField(max_length=15, choices=RATING_CHOICES)

    def __str__(self):
        return f"{self.user} - {self.music}: {self.rating}"
