import random
from django.db import models
from django.conf import settings
# Create your models here.

User = settings.AUTH_USER_MODEL


class Humm(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    #like = models.IntegerField()
    # id = models.AutoField(primry_key = True)
    # many Users can many tweets, one tweet can only be by one user.
    # user models.ForeignKey(User, null=True, on_delete=models.SET_NULL) # when we want to keep history even if user deleted.

    # many Users can many tweets, one tweet can only be by one user.

    class Meta:
        ordering = ['-id']

    def serialize(self):
        return{
            "id": self.id,
            "content": self.content,
            "like": random.randint(0, 2000)
        }
