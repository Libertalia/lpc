from setuptools import setup, find_packages

setup(name='lpc',
    version='0.0.1',
    description='OpenShift App',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    author='James Pic',
    author_email='contact@libertalia.tv',
    url='http://github.com/libertalia/lpc',
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
