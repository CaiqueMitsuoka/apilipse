import os
from app import getApp
from config import PORT, DEBUG

port = int(os.environ.get('PORT', PORT))
app = getApp()
app.run(host='0.0.0.0', port=port, debug=DEBUG)
