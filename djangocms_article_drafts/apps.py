from django.apps import AppConfig
# from django.apps import apps as django_apps
from django.conf import settings


class DjangocmsArticleDraftsConfig(AppConfig):
    name = 'djangocms_article_drafts'
    verbose_name = 'Publishable Article Drafts'

    def ready(self):
        # @todo: register publishable models from settings.py
        print('ready')
        # print(settings)

