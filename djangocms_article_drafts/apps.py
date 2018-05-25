from django.apps import AppConfig
# from django.apps import apps as django_apps
from django.conf import settings


class DjangocmsArticleDraftsConfig(AppConfig):
    name = 'djangocms_article_drafts'
    verbose_name = 'Publishable Article Drafts'

    def ready(self):
        from .models import publishable_pool
        # @todo: register publishable models from settings.py
        publishable_models = getattr(settings, 'CMS_PUBLISHABLE_REGISTERED_MODELS', ())
        for i in publishable_models:
            publishable_pool.register(i)
