from unittest.mock import MagicMock, patch

from django.db import models
from django.test import TestCase
from cms.exceptions import PublicIsUnmodifiable


from djangocms_article_drafts.models import BasePublishable, publishable_pool
from djangocms_article_drafts.test_project.models import ArticleTest


class GenericPublishingTestCase(TestCase):

	def test_pool_attribute(self):
		self.assertEquals(publishable_pool.model_pool, {})
	
	def test_register(self):
		publishable_pool.register(ArticleTest)


	#todo: refactor for pool
    # def test_exception_if_article_is_draft(self):
    #     public_article = Article.objects.create(publisher_is_draft=False)

    #     with self.assertRaises(PublicIsUnmodifiable):
    #         public_article.publish('en')

    # def test_article_publish(self):
    #     draft_article = Article.objects.create(publisher_is_draft=True)

    #     is_published = draft_article.publish('en')

    #     self.assertTrue(is_published)
