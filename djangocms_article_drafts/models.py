from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.fields import GenericForeignKey

from cms.exceptions import PublicIsUnmodifiable, PublicVersionNeeded
from cms.signals import post_publish
import importlib

from djangocms_article_drafts.exceptions import DraftDoesNotExist, NotPublished


class Publishable(models.Model):
    """Abstract model to represent a publishable CMS node e.g. Page, Article.
    """

    content_type = models.ForeignKey(ContentType)
    draft_object_id = models.PositiveIntegerField()
    published_object_id = models.PositiveIntegerField(null=True)

    draft_object = GenericForeignKey('content_type', 'draft_object_id')
    published_object = GenericForeignKey('content_type', 'published_object_id')

    is_draft = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    # Publishable can be hidden on the frontend, but still published,
    # `is_visible` is the flag used for this scenario
    is_visible = models.BooleanField(default=False)

    """ draft_object_id @todo: track the draft
    to which a published record relates """
    class Meta:
        unique_together = ('content_type', 'draft_object_id')

    @classmethod
    def create(cls, draft_object):
        """
        When publishable is first created

        :return: <obj> Publishable
        """
        return Publishable.objects.create(draft_object=draft_object)

    def publish(self):
        # TODO We need to copy the draft object to a new PublishedObject and
        # save this on our Publishable model
        published_object = self._copy_object_stub()
        self.published_object = published_object
        self.is_draft = False
        self.is_published = True
        self.is_visible = True
        self.save()

    def edit(self):
        """
        Some changes has been made on this Publishable, so lets mark it as
        a draft. The draft_object must be present for edit to be possible
        """
        if self.draft_object is None:
            # We can't edit this publishable if there is no draft version yet
            raise DraftDoesNotExist(
                "You need a draft to be able to edit this Publishable"
            )

        self.is_draft = True
        self.save()

    def set_visibility(self, visible=True):
        """
        This method updates the visibility of this Publishable. We can't set
        publishable to visible if it is not published.
        :param visible: <bool> Should this Publishable be visible?
        """
        if visible and not self.is_published:
            raise NotPublished(
                "You can't set visibility to True for non-published Publishable"
            )
        self.is_visible = visible
        self.save()

    def _copy_object_stub(self):
        """
        Stub method which will handle copying the data to the new published object.
        `self.published_object` might be set or None. If it is None lets create
        it and save it, otherwise re-use the id
        TODO Implement this method properly (FIL-118)
        """
        if self.published_object is None:
            new_object = self.draft_object
            new_object.pk = None
            new_object.save()
        else:
            new_object = self.published_object

        return new_object


# @todo: db keeping track of registered classes / models
# class StoredPublishables(models.Model):


class PublishPool(object):
    def __init__(self):
        self.clear()

    def __contains__(self, model_class):
        return model_class in publishable_pool.model_pool.values()

    def create_publishable(self, sender, instance, created):
        if created:
            Publishable.create(draft_object=instance)
        else:
            # Mark the existing one as a draft
            publishable = Publishable.objects.get(draft_object=instance)
            publishable.edit()

    def clear(self):
        self.model_pool = {}

    def register(self, model_module, model_name):
        """
        TODO: check that the model has certain
        required attributes e.g. publisher_is_draft
        """
        model_module = importlib.import_module(model_module, model_name)
        ContentModel = getattr(model_module, model_name)
        assert ContentModel.__name__ == model_name, (
            'ContentModel not imported correctly. Expected {} class, found {}.'.format(
                model_name, ContentModel))
        self.model_pool[model_name] = ContentModel

    def get_published_record(self):
        pass

    def get_draft_record(self):
        pass

    def publish(self, model_instance):
        # Publish can only be called on draft pages
        publishable = Publishable.objects.get(
            draft_object_id=model_instance.id
        )
        if not publishable.is_draft:
            raise PublicIsUnmodifiable(
                'The public instance cannot be published. Use draft.' 
            )

        # validate... Content Object.publisher_can_publish() calls this if available on foreign object
        try:
            publishable.publisher_can_publish()
        except AttributeError as e:
            pass

        # Do we need to look for a matching published record?
        # If there is no published version yet. Create one.
            # NB: the existing publisher app has two attributes: is_draft_version and is_published_version, which seems like a redundancy

        # set is_draft = false

        # save publishable.draft_id foreign key

        # NB: these would be our default behaviours but would be overridden by callbacks defined on the foreign object
        # publisher.copy_object: Copy the Content record first via copy_object default, or via callback override (i.e. copy_object, copy_placeholder, get_fields_to_copy)
            # question: relationship between page & title: why do we need is_draft & public_id on both models?
        # publisher.update_relations
            # update_one_to_many_relation
            # update_one_to_one_relation
            # update_many_to_many_relation

        # save the publishable.published_id

        # delete draft? We don't need this – Paulo says it causes relationship problems.


        # @todo: Parler? Do we need it? Why is it not part of the CMS already?

        publishable.publish()
        return True


@receiver(post_publish, dispatch_uid='publishable_post_publish')
def publish_receiver(sender, **kwargs):
    # check for known publishable models
    if sender in publishable_pool:
        publishable_pool.publish(kwargs['instance'])
    # e.g. model.save()


@receiver(post_save, dispatch_uid="publishable_post_save")
def save_receiver(sender, **kwargs):
    # import pdb; pdb.set_trace()
    if sender in publishable_pool:
        publishable_pool.create_publishable(sender, kwargs['instance'], kwargs['created'])


publishable_pool = PublishPool()    
