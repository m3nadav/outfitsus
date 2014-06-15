import sys
sys.path = []
activate_this = '/var/www/html/flask/bin/ativate_this.py'
execfile(activate_this, dict(__file__=activate_this))
from nadav import app as application
