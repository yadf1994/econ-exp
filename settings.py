import os
# import dj_database_url

# Définir la variable DATABASES pour PostgreSQL avec SSL activé
# DATABASES = {
    # 'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'), conn_max_age=600, ssl_require=True)
# }


from os import environ

SESSION_CONFIGS = [
    dict(
        name='random_treatment',
        display_name="EXP EFREI random per group traitement",
        app_sequence=['votes'],
        num_demo_participants=5,
        treatment=-1,
    ),
    dict(
        name='test_t0',
        display_name="EXP EFREI traitement 0",
        app_sequence=['votes'],
        num_demo_participants=5,
        treatment=0,
    ),
    dict(
        name='test_t1',
        display_name="EXP EFREI traitement 1 (WoodSIRV)",
        app_sequence=['votes'],
        num_demo_participants=5,
        treatment=1,
    ),
    dict(
        name='test_t2',
        display_name="EXP EFREI traitement 3 (Borda)",
        app_sequence=['votes'],
        num_demo_participants=5,
        treatment=2,
    ),
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'fr'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = False

ROOMS = [
    dict(
        name='efrei',
        display_name='EFREI EXP',
        participant_label_file='_rooms/efrei.txt',
    )
]

ADMIN_USERNAME = 'admin'

ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '{{ secret_key }}'

INSTALLED_APPS = ['otree']