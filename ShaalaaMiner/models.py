from django.db import models

# Create your models here.

class Grade(models.Model):
    grade = models.IntegerField(unique=True)
    to_scrape = models.BooleanField(default=False)

    def __str__(self):
        return f'class {self.grade}' 

class Publication(models.Model):
    author = models.CharField(max_length=255, unique=True)
    hyperlink = models.URLField()
    available = models.BooleanField(default=True)
    to_scrape = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.author} {self.to_scrape} {self.available}"
