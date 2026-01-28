from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Add any additional fields or methods if needed
    pass

    def __str__(self):
        return self.username
