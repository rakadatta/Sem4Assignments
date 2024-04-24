from os import environ


SESSION_CONFIGS = [
    dict(
        name="pub_goods_test",
        display_name="my pub goods",
        num_demo_participants=3,
        app_sequence=["my_pub_goods"],
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=1.00, participation_fee=0.00, doc="")

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = "en"

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = "USD"
USE_POINTS = False

ROOMS = [
    dict(
        name="econ101",
        display_name="Econ 101 class",
        participant_label_file="_rooms/econ101.txt",
    ),
    dict(name="live_demo", display_name="Room for live demo (no participant labels)"),
    dict(
        name="econ9942",
        display_name="Econ 9942 class",
        participant_label_file="_rooms/econ9942.txt",
        use_secure_urls=True,
    ),
]

ADMIN_USERNAME = "admin"
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get("OTREE_ADMIN_PASSWORD")

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = "123"

INSTALLED_APPS = ["otree"]

# use_browser_bots = True
