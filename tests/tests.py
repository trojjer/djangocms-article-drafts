from unittest.mock import MagicMock, patch

from django.db import models
from django.db.models.signals import post_save
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType

from cms.exceptions import PublicIsUnmodifiable
from cms.signals import post_publish

from djangocms_article_drafts.models import Publishable, publishable_pool
from djangocms_article_drafts.test_project.models import ArticleTest

class GenericPublishingTestCase(TestCase):

    def test_pool_attribute(self):
        self.assertEquals(publishable_pool.model_pool, {})
    
    def test_register(self):
        self.assertEquals(publishable_pool.model_pool, {})
        publishable_pool.register(ArticleTest)
        self.assertEquals(publishable_pool.model_pool, {ArticleTest.__name__: ArticleTest})

    # def test_publish_signal(self):
    #     post_publish.send(ArticleTest.objects.create())

    # def test_publish_signal_unregistered_model(self):
    #     post_publish.send(object())
    
    def test_save_signal_creates_new_publishable(self):
        # article = ArticleTest.objects.create()
        # import pdb; pdb.set_trace()
        # publishable_type = ContentType.objects.get(app_label="djangocms_article_drafts", model="publishable")
        article = ArticleTest()
        article.save()
        # post_save.send(ArticleTest, instance=article, created=True)
        self.assertEquals(Publishable.objects.count(), 1)
        
        publishable = Publishable.objects.first()
        self.assertEquals(publishable.object_id, article.id)

    #todo: refactor for pool
    # def test_exception_if_article_is_draft(self):
    #     public_article = Article.objects.create(publisher_is_draft=False)

    #     with self.assertRaises(PublicIsUnmodifiable):
    #         public_article.publish('en')

    # def test_article_publish(self):
    #     draft_article = Article.objects.create(publisher_is_draft=True)

    #     is_published = draft_article.publish('en')

    #     self.assertTrue(is_published)
