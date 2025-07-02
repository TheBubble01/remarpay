from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    """
    Custom user manager for handling user creation and superuser logic.
    """

    def create_user(self, email, name, password=None, role='cashier', phone=None):
        if not email:
            raise ValueError("Users must have an email address")
        
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            role=role,
            phone=phone
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.role = 'tech-admin'
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model with role-based access, profile info, timezone,
    and frontend preference support.
    """

    ROLE_CHOICES = [
        ('cashier', 'Cashier'),
        ('agent', 'Payment Agent'),
        ('manager', 'Chief Manager'),
        ('tech-admin', 'Tech Admin'),
    ]

    COUNTRY_CHOICES = [
        ('nigeria', 'Nigeria'),
        ('niger', 'Niger'),
        ('cameroon', 'Cameroon')
    ]

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='cashier')
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)

    # For agent assignment
    assigned_country = models.CharField(
        max_length=20,
        choices=COUNTRY_CHOICES,
        blank=True,
        null=True
    )

    # User preferences
    current_country = models.CharField(max_length=50, blank=True, null=True)
    timezone = models.CharField(max_length=100, blank=True, null=True)
    dark_mode = models.BooleanField(default=False)

    # Django system fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.name
