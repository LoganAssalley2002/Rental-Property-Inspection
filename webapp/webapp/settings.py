import os
from dotenv import load_dotenv

load_dotenv('.env')

if os.environ.get('ENVIRONMENT') == 'PRODUCTION':
    from core.settings.production import *
else:
    from core.settings.development import *
