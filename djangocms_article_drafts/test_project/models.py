from django.db import models


class ArticleTest(models.Model):
	
	publisher_is_draft = models.BooleanField(default=True)
