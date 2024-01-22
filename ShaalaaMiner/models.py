from django.db import models

# Create your models here.

class Publication(models.Model):
    author = models.CharField(max_length=255,)
    hyperlink = models.URLField()
    available = models.BooleanField(default=True)
    to_scrape = models.BooleanField(default=False)

