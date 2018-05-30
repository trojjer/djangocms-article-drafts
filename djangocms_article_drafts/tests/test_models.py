from django.test import TestCase

from djangocms_article_drafts.exceptions import DraftDoesNotExist, NotPublished
from djangocms_article_drafts.models import Publishable
from djangocms_article_drafts.test_project.models import ArticleTest


class PublishableModelTestCase(TestCase):
    def test_create(self):
        article = ArticleTest(title='Test title', reviewed=True)
        article.save()

        # At the beginning, we don't have any Publishables
        self.assertEqual(0, Publishable.objects.all().count())

        # Lets create our first draft
        Publishable.create(article)
        self.assertEqual(1, Publishable.objects.all().count())
        publishable = Publishable.objects.get()

        # Lets double check that the flags and objects are set correctly
        self.assertIsNone(publishable.published_object)

        self.assertEqual(article.pk, publishable.draft_object_id)
        self.assertEqual(article.pk, publishable.draft_object.pk)

        self.assertTrue(publishable.is_draft)
        self.assertFalse(publishable.is_published)
        self.assertFalse(publishable.is_visible)

    def test_publish(self):
        article = ArticleTest(title='Test title', reviewed=True)
        article.save()
        Publishable.create(article)

        publishable = Publishable.objects.get()

        # After publishing, we still have only 1 Publishable object,
        # but with both draft_object and published_object set
        publishable.publish()

        self.assertEqual(1, Publishable.objects.all().count())
        publishable = Publishable.objects.get()

        self.assertIsNotNone(publishable.published_object)

        self.assertEqual(article.pk, publishable.draft_object_id)
        self.assertEqual(article.pk, publishable.draft_object.pk)

        self.assertFalse(publishable.is_draft)
        self.assertTrue(publishable.is_published)
        self.assertTrue(publishable.is_visible)

    def test_edit(self):
        article = ArticleTest(title='Test title', reviewed=True)
        article.save()

        Publishable.create(article)

        publishable = Publishable.objects.get()

        # Without draft_object set, we can't edit the publishable
        publishable.draft_object = None
        with self.assertRaises(DraftDoesNotExist):
            publishable.edit()

        publishable.draft_object = article

        publishable.publish()
        self.assertTrue(publishable.is_visible)
        self.assertTrue(publishable.is_published)
        self.assertFalse(publishable.is_draft)

        # After we trigger edit, the publishable should be in the draft state
        publishable.edit()
        self.assertTrue(publishable.is_visible)
        self.assertTrue(publishable.is_published)
        self.assertTrue(publishable.is_draft)

    def test_set_visibility(self):
        article = ArticleTest(title='Test title', reviewed=True)
        article.save()

        Publishable.create(article)
        publishable = Publishable.objects.get()

        # We don't have a published version yet, so setting visiblity to True
        # should fail

        with self.assertRaises(NotPublished):
            publishable.set_visibility(visible=True)

        # False should work
        publishable.set_visibility(visible=False)

        publishable.publish()
        # Now the publishable is published, and automatically visible
        self.assertTrue(publishable.is_visible)
        self.assertTrue(publishable.is_published)

        # We can set the visibility to False
        publishable.set_visibility(visible=False)
        self.assertFalse(publishable.is_visible)
        self.assertTrue(publishable.is_published)

        # And to True, as Publishable is published
        publishable.set_visibility(visible=True)
        self.assertTrue(publishable.is_visible)
        self.assertTrue(publishable.is_published)
