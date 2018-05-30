# djangocms-article-drafts
Working title for a generic publishing app to integrate with `divio/djangocms-moderation`.

The goal is to provide generic publish functionality to `Articles` as well as `Pages`.


# Installation

We need to install the `djangocms` and then add this repository as a dependency:

1. Create and activate new virtual env, e.g.
    
    `mkvirtualenv testenv`

2. Create a project folder, e.g.
 
    `mkdir ~/workspace/testproject/`
    
3. `cd ~/workspace/testproject`

4. Install djangocms 

    `pip install djangocms-installer`

5. Setup djangocms, e.g. 
    
    `djangocms -f -p . testsite`

6. `pip install djangocms_helper`

7. Add the following email settings to settings.py

```
    # This will ensure that emails will be printed to the console instead of real send
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

9. Fork `https://github.com/trojjer/djangocms-article-drafts`

10. Clone yours `djangocms-article-drafts` app from github into separate folder, 
    e.g. `~/workspace/djangocms-article-drafts/`

11. Go to the main project folder  `cd ~/workspace/testproject` and install the 
    package from your local folder

    `pip install -e ~/workspace/djangocms-article-drafts/`

12. Add `djangocms_article_drafts` and `adminsortable2` to the INSTALLED_APPS in settings.py

13. `python manage.py migrate`

14. `python manage.py test djangocms_article_drafts`

Now you can make changes to your local `~/workspace/djangocms-article-drafts/`
repository and changes will be reflected in your `testproject`.
