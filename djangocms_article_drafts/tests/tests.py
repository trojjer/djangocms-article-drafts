from cms.exceptions import PublicIsUnmodifiable
from django.test import TestCase

from djangocms_article_drafts.models import Article


class GenericPublishingTestCase(TestCase):

    def test_exception_if_article_is_draft(self):
        public_article = Article.objects.create(publisher_is_draft=False)

        with self.assertRaises(PublicIsUnmodifiable):
            public_article.publish('en')

    def test_article_publish(self):
        draft_article = Article.objects.create(publisher_is_draft=True)

        is_published = draft_article.publish('en')

        self.assertTrue(is_published)
