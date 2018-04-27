from django.db import models

# Create your models here.
class GenericPublishMixin(object):
	
	def publish(self, language):
		
		return
		
@receiver(post_save, dispatch_uid='generic_publish_event')
def publish_event(sender, instance, **kwargs):
	# check the settings PUBLISHER_REGISTERED_MODELS for known publishable models
	
	# get the model
		# e.g. model.save()
		pass