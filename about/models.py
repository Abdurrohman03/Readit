from django.db import models


class Feedback(models.Model):
    fullname = models.CharField(max_length=225)
    position = models.CharField(max_length=225)
    avatar = models.ImageField(upload_to='feedbacks/')
    message = models.TextField()

    def __str__(self):
        return self.fullname

