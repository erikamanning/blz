API_SECRET_KEY = os.environ.get('SECRET_API_KEY', '##NOT A KEY##')
FLASK_SECRET_KEY = os.environ.get('SECRET_KEY', '##NOT A KEY##')
DATA_BASE_URI = os.environ.get('DATABASE_URL','postgresql:///blz')