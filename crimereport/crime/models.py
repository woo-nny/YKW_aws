from django.db import models




class Congressperson(models.Model):
    name = models.CharField(max_length=50)
    district = models.CharField(max_length=1000)
    crimes = models.TextField()
    penalty = models.CharField(max_length=100)
    photo = models.CharField(max_length=100)
    elected_num = models.IntegerField()
    party = models.CharField(max_length=50)

    def __str__(self):
        return self.district


class Saying(models.Model):
    speaker = models.CharField(max_length=50)
    saying = models.TextField()

