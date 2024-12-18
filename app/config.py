# 服务器公网 IP
SERVER_ADDRESS = '103.229.54.221'
SERVER_PORT = 8000

mysql_config = {
        'connections': {
            'default': {
                # 'engine': tortoise.backends.asyncpg, # PostgreSQL
                'engine': 'tortoise.backends.mysql', # MySQL or Mariadb
                'credentials': {
                    'host': SERVER_ADDRESS,
                    'port': '33060',
                    'user': 'root',
                    'password': '932384',
                    'database': 'fyzt',
                }
            },
        },
        'apps': {
            'models': {
                'models': ['app.models.user', 'app.models.video', 'app.models.user_form', "aerich.models"],
                'default_connection': 'default',
            }
        },
        'use_tz': False,
        'time_zone': 'Asia/Shanghai'
    }


url = "https://meta.guiji.ai"
AccessKey = "69wCg6iKHMGlcULLGahXIQT3"
Secretkey = "XfYmmoZTbBOR3PPThzdpk6XKMgz8hSUMvnMBM2UtEKI9lVRfw8KLynloXo72Amjo"



REDIS_PASSWORD = '932384'


REDIS_USER_REGISTER_CODE = 'user:register:code:'
REDIS_USER_LOGIN_CODE = 'user:login:code:'
REDIS_USER_RESET_CODE = 'user:reset:code:'