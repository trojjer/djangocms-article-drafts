from cms.exceptions import PublicIsUnmodifiable
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class BasePublishable(models.Model):
    """Abstract model to represent a publishable CMS node e.g. Page, Article.
    """
    publisher_is_draft = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def publish(self, language):
        # Publish can only be called on draft pages
        if not self.publisher_is_draft:
            raise PublicIsUnmodifiable('The public instance cannot be published. Use draft.')

        return None


class Article(BasePublishable):
    """Publishable Article as distinct from Page.
    """
    pass


@receiver(post_save, dispatch_uid='generic_publish_event')
def publish_event(sender, instance, **kwargs):
    # check the settings PUBLISHER_REGISTERED_MODELS for known publishable models

    # get the model
    # e.g. model.save()
    pass
