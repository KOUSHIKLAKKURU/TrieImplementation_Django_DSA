from django.db import models

# Create your models here.
class Word (models.Model):
    word_text = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.word_text