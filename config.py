db_config = {
        'connections': {
            'default': {
                # 'engine': tortoise.backends.asyncpg, # PostgreSQL
                'engine': 'tortoise.backends.mysql', # MySQL or Mariadb
                'credentials': {
                    'host': '115.25.46.212',
                    'port': '3306',
                    'user': 'head',
                    'password': 'headhead',
                    'database': 'manage_system',
                }
            },
        },
        'apps': {
            'models': {
                'models': ['models.user',"aerich.models"],
                'default_connection': 'default',
            }
        },
        'use_tz': False,
        'time_zone': 'Asia/Shanghai'
    }