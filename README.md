# hydra-presentation
Presentation layer for Hydra framework


## Setup project ...

```bash
# Install bower packages from your project settings.py
python manage.py bower install
# Build hydra-frontend
python manage.py polymer build
# Finally merge in static folder
python manage.py collectstatic -i
```