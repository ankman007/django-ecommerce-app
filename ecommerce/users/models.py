from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True, null=False)
    password_hash = models.TextField(null=False)
    
    def __str__(self):
        return f"User ID: {self.id}\nUser email: {self.email}"