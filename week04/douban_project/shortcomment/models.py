from django.db import models

# Create your models here.

class Short(models.Model):
    subject_id = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    rating = models.CharField(max_length=10)
    posttime = models.DateTimeField()
    shorttext = models.TextField()
    
    class Meta:
        verbose_name = "短评"
        verbose_name_plural = "短评"
        ordering = ["-posttime"]
    
    def __str__(self):
        return self.shorttext
