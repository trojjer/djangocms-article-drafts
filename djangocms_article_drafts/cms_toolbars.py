from django.utils.translation import override as force_language, ugettext_lazy as _

import importlib


# from cms.api import get_page_draft  # @todo: publisher needs its own version of this

from cms.utils.urlutils import add_url_parameters, admin_reverse
from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.toolbar.items import (
    Button,
    ButtonList,
    BaseItem,
    Dropdown,
    DropdownToggleButton,
    ModalButton,
)

from cms.utils.urlutils import admin_reverse
# from .utils import get_admin_url

# @todo: refactor as generic rather than Article
from cms.cms_toolbars import PageToolbar

from .models import publishable_pool


class PublisherToolbar(CMSToolbar):
    #
    # watch_models = [Article]
    # supported_apps = ['aldryn_newsblog']

    def populate(self):
        print('populate')
        pass

    def post_template_populate(self):
        print('post_template_populate')
        self.add_publish_button()

    def request_hook(self):
        print('request_hook')
        # @todo: assign self.get_supported_apps() returned as supported apps"
        pass

    def get_supported_apps(self):
        """ Retrieve iterable of content models registered to the pool"""
        pass

    def get_content_object_pk(self):
        return 1

    def get_publish_url(self):
        return ''
        pk = self.get_content_object_pk()
        params = {}
        url = admin_reverse('cms_publisher_publish_object', args=(pk, 'en',))
        return add_url_parameters(url, params)

    def add_publish_button(self, classes=None):

        item = ButtonList(side=self.toolbar.RIGHT)
        item.add_button(
            _('Publisher modla'),
            url=self.get_publish_url(),
            disabled=False,
            extra_classes={},
        )
        self.toolbar.add_item(item)

# should_register = False
# print('yo')
# print(toolbar_pool.toolbars.values())
# for toolbar in toolbar_pool.toolbars.values():
#     print('toolbar')
#     print(toolbar)
#     print('publishable list')
#     print(publishable_pool.model_pool.values())
#     for ContentModel in publishable_pool.model_pool.values():
#         print('ContentModel')
#         print(ContentModel)
#         watch_models = getattr(toolbar, 'watch_models', None)
#         if watch_models and ContentModel.__name__ in watch_models:
#             print('found ContentModel')
#             toolbar_pool.unregister(toolbar)

toolbars = [t for t in toolbar_pool.toolbars.values()]
for toolbar in toolbars:
    # toolbar_pool.unregister(toolbar)
    pass

toolbar_pool.register(PublisherToolbar)
