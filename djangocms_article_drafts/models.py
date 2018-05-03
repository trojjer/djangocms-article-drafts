from cms.exceptions import PublicIsUnmodifiable
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class BasePublishable(models.Model):
    """Abstract model to represent a publishable CMS node e.g. Page, Article.
    """
    
    def __init__(self):
        self.model_pool = {}
    
    def register(self, model_class_name):
        # todo: model_pool[model_class_name] = model_class_name()
        # todo: check that the model has certain required attributes e.g. publisher_is_draft
        pass

    def publish(self, language):
        # Publish can only be called on draft pages
        if not self.publisher_is_draft:
            raise PublicIsUnmodifiable('The public instance cannot be published. Use draft.')

        return True
        

publishable_pool = BasePublishable()    


# @todo
# @receiver(pre_publish, dispatch_uid='generic_publish_event')
# def publish_event(sender, instance, **kwargs):
#     # check the settings PUBLISHER_REGISTERED_MODELS for known publishable models

#     # get the model
#     # e.g. model.save()
#     pass

# @receiver(post_publish, dispatch_uid='generic_publish_event')
# def publish_event(sender, instance, **kwargs):
#     # check the settings PUBLISHER_REGISTERED_MODELS for known publishable models

#     # get the model
#     # e.g. model.save()
#     pass
