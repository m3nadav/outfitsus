import sys
activate_this = '/var/www/html/flask/bin/ativate_this.py'
execfile(activate_this, dict(__file__=activate_this))
sys.path.append('/var/www/html/flask')
sys.path.append('/var/www/html/flask/env/lib/python2.7/site-packages')
from nadav import app as application
