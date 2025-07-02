from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, role='cashier', phone=None):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email), name=name, role=role, phone=phone)
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
    ROLE_CHOICES = [
        ('cashier', 'Cashier'),
        ('agent', 'Payment Agent'),
        ('manager', 'Chief Manager'),
        ('tech-admin', 'Tech Admin'),
    ]


    # Country assignment for agents
    assigned_country = models.CharField(
        max_length=20,
        choices=[
            ('nigeria', 'Nigeria'),
            ('niger', 'Niger'),
            ('cameroon', 'Cameroon')
        ],
        blank=True,
        null=True
    )

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='cashier')
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # User's current operating country
    current_country = models.CharField(max_length=50, blank=True, null=True)

    # Timezone string, e.g. 'Africa/Lagos'
    timezone = models.CharField(max_length=100, blank=True, null=True)

    # User dark mode preference
    dark_mode = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.name
