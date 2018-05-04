from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.fields import GenericForeignKey

from cms.exceptions import PublicIsUnmodifiable
from cms.signals import post_publish


class Publishable(models.Model):
    """Abstract model to represent a publishable CMS node e.g. Page, Article.
    """
    
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    is_draft = models.BooleanField(default=True)

    class Meta: 
        unique_together = ('content_type', 'object_id')

# @todo: db keeping track of registered classes / models
# class StoredPublishables(models.Model):
    
    
class PublishPool(object):
    def __init__(self):
        self.model_pool = {}
    
    def register(self, model_class):
        # todo: check that the model has certain required attributes e.g. publisher_is_draft
        self.model_pool[model_class.__name__] = model_class

    def publish(self, model_instance):
        # Publish can only be called on draft pages
        if not model_instance.is_draft:
            raise PublicIsUnmodifiable('The public instance cannot be published. Use draft.')
        return True
        
    def __contains__(self, model_class):
        return model_class in publishable_pool.model_pool.values()
    
    
@receiver(post_publish, dispatch_uid='publishable_post_publish')
def publish_receiver(sender, **kwargs):
    # check for known publishable models
    if sender in publishable_pool:
        publishable_pool.publish(sender)
    # e.g. model.save()
    
@receiver(post_save, dispatch_uid="publishable_post_save")
def save_receiver(sender, **kwargs):
    if sender in publishable_pool:
        if kwargs['created']: 
            # import pdb; pdb.set_trace()
            Publishable.objects.create(content_object=kwargs['instance'])
        else:
            # @todo: check for existence of records
            pass

publishable_pool = PublishPool()    
