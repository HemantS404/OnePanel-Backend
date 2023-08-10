from django.db import models
from accounts.models import User
import uuid

# Create your models here.
class Database(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)

    def __str__(self) :
        return f'{self.user.email}\'s  {self.name}'

class Artifact(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    database = models.ForeignKey(Database, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)

    def __str__(self) :
        return f'{self.database.name} - {self.name}'

class Collection(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    artifact = models.ForeignKey(Artifact, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    schema = models.JSONField()

    def __str__(self) :
        return f'{self.artifact.name}\'s  {self.name}'