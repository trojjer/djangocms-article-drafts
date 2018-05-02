from cms.exceptions import PublicIsUnmodifiable
from django.test import TestCase

from djangocms_article_drafts.models import Article


class GenericPublishingTestCase(TestCase):

    def test_exception_if_page_is_draft(self):
        draft_article = Article.objects.create(publisher_is_draft=False)

        with self.assertRaises(PublicIsUnmodifiable):
            draft_article.publish('en')
