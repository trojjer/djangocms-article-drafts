from django.db import models


class ArticleTest(models.Model):
    """
    Test model used for unit tests
    """
    title = models.CharField(max_length=128)
    reviewed = models.BooleanField(default=False)


class UnregisteredModel(models.Model):
    """
    Test model used for unit tests
    """
    pass
