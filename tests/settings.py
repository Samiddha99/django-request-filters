from pathlib import Path
from decouple import config, Csv
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env_file = BASE_DIR / '.env'
env = environ.Env()

DEBUG = True

VPNAPI_KEY=config('VPNAPI_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}
SECRET_KEY = 'justfortest'
