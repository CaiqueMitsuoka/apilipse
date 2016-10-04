import app,os
from app import getApp
port = int(os.environ.get('PORT', 5000))
app = getApp()
app.run(host='0.0.0.0',port=port,debug=True)
