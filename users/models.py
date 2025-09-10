from django.db import models
from django.contrib.auth.models import User
import uuid

class Invitation(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    email = models.EmailField(unique=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
