import os,sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.environ['PWD']),'gallery')))
sys.path.append(os.path.dirname(os.environ['PWD']))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gallery.settings")

# This application object is used by the development server
# as well as any WSGI server configured to use this file.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
