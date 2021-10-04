from os import environ

SESSION_CONFIGS = [
    dict(
        name='syp_v1',
        display_name='DB Decision-Making Study',
        app_sequence=['syp_v1'],
        num_demo_participants = 10, #should be 20 in actual implementation, must be multiples of 10
        use_browser_bots=False,
        doc="""
        djb187@pitt.edu SYP project
        """
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False
# USE_POINTS = True

# uncomment when ready to go to production
environ['OTREE_ADMIN_PASSWORD'] = 'dbanko_syp'
environ['OTREE_PRODUCTION'] = '1'
environ['OTREE_AUTH_LEVEL']='STUDY'

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '7468549050899'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']


# OTREE_AUTH_LEVEL = DEMO


DEBUG = (environ.get('OTREE_PRODUCTION') in {None, '', '0'})
AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')

ROOMS = [
    dict(
        name='peel_virtual',
        display_name='PEEL (Virtual)',
        participant_label_file='_rooms/participant_labels_syp.txt',
        use_secure_urls=True
    ),
]

