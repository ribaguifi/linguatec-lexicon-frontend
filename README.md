# linguatec lexicon frontend
Frontend website based on vue.js

## Development
``TODO``

node.js and npm
```
sudo apt-get install --no-install-recommends nodejs npm
```

## Deployment

```
django-admin startproject frontend

```

Update settings:
```
# settings.py
INSTALLED_APPS = [
    ...
    'linguatec_lexicon_frontend',
]

STATIC_ROOT = '/home/linguatec/frontend/static/'
```

Update `urls.py`
```
# urls.py
urlpatterns = [
    ...
    path('', include('linguatec_lexicon_frontend.urls')),
]
```
