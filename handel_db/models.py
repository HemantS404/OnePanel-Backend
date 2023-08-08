from django.db import models
from accounts.models import User

# Create your models here.
class Database(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)

    def __str__(self) :
        return f'{self.user.email}\'s  {self.name}'

class Artifact(models.Model):
    database = models.ForeignKey(Database, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)

    def __str__(self) :
        return f'{self.database.name} - {self.name}'

class Collection(models.Model):
    artifact = models.ForeignKey(Artifact, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    schema = models.JSONField()

    def __str__(self) :
        return f'{self.artifact.name}\'s  {self.name}'