import os
import sys

sys.path.insert(0, os.getcwd())

from detectweb import create_app

# Create an application instance that web servers can use. We store it as
# "application" (the wsgi default) and also the much shorter and convenient
# "app".
application = create_app()
