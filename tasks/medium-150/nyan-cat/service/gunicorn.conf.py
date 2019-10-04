user      = 'www-data'
group     = 'www-data'
bind      = '0.0.0.0:31337'
workers   = 4
threads   = 4
accesslog = '/var/log/gunicorn/access.log'
errorlog  = '/var/log/gunicorn/error.log'
