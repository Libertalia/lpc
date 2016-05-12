from setuptools import setup

setup(name='lpc',
    version='0.0.1',
    description='OpenShift App',
    packages=['lpc'],
    author='James Pic',
    author_email='contact@libertalia.tv',
    url='http://github.com/libertalia/lpc',
    install_requires=[
        'Django>=1.9,<1.10',
        'django-shop>=0.9,<1.0',
        'djangocms_text_ckeditor>=2.9,<2.10',
        'djangocms-cascade>=0.8,<0.9',
        'djangocms-bootstrap3>=0.1,<0.2',
        'django-admin-sortable2>=0.6,<0.7',
        'djangorestframework>=3.1,<3.2',
        'django-rest-auth>=0.5,<0.6',
        'django-fsm>=2.3,<2.4',
        'django-fsm-admin>=1.2,<1.3',
        'django-libsass>=0.4,<0.5',
        'django-filter>=0.13,<0.14',
        'django-parler>=1.6,<1.7',
        'djangoshop-stripe>=0.1,<0.2',
    ],
    extras_require={
        # Full version hardcode for testing dependencies so that
        # tests don't break on master without any obvious reason.
        'testing': [
            'django-responsediff==0.2.0',
            'flake8==2.5.1',
            'pep8==1.5.7',
            'pytest==2.8.5',
            'pytest-django==2.9.1',
            'pytest-cov==2.2.0',
            'codecov',
        ]
    }
)
