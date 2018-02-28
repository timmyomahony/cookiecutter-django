# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

This repository was generated using a [modified version](https://github.com/timmyomahony/cookiecutter-django) of [django-cookie-cutter](https://github.com/pydanny/cookiecutter-django). 

Many of the options available when creating a new `django-cookie-cutter` have been either removed or enforced for our needs:

- Enforced Sentry logging
- Enforced Docker for both local development and for deployment
- Removed any Windows-specific options
- Removed opbeat, Mailhog, Celery and Bootstrap configurations
- Removed allauth and the default user account
- Removed the default views, styles and JavaScript
- Replaced the documentation with MkDocs (as opposed to Sphinx)
- Simplified the `base.html`
- Added a single core app with an `index.html`
- Replaced the media file storage on production with a manifest storage get cache busting
- Included a `robots.txt` and `humans.txt` view as well as a `sitemap.xml`
- Included `easy_thumbnails`