from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        STAFF = "staff", "Staff"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STAFF)
    is_active = models.BooleanField(default=True)

    def is_admin_role(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    def is_staff_role(self):
        return self.role in [self.Role.ADMIN, self.Role.STAFF]