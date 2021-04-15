import os
from distutils.core import setup

def get_version():
    """
    Gets the latest version number out of the package,
    saving us from maintaining it in multiple places.
    """
    local_results = {}
    execfile('script_runner/version.py', {}, local_results)
    return local_results['__version__']

setup(
    name="script-runner-api",
    packages=[
        "script_runner",
        "script_runner.api",
    ],
    scripts=["script_runner/main.py"],
    version=get_version(),
    license="MIT",
    description="Provides an API server + celery worker module for running arbitrary scripts.",
    author="Robert Chu",
    author_email="robert.chu@labgrid.com",
    url="https://github.com/lab-grid/script-runner",
    download_url="https://github.com/lab-grid/script-runner/archive/0.1.0.tar.gz",
    keywords=["script", "api", "labflow", "labgrid", "lab-grid"],
    install_requires=[
        "amqp==5.0.6; python_version >= '3.6'",
        "aniso8601==9.0.1; python_version >= '3.5'",
        "attrs==20.3.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "billiard==3.6.4.0",
        "celery==5.0.5",
        "click==7.1.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "click-didyoumean==0.0.3",
        "click-plugins==1.1.1",
        "click-repl==0.1.6",
        "decorator==5.0.5; python_version >= '3.5'",
        "ecdsa==0.14.1; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "flask==1.1.2",
        "flask-cors==3.0.10",
        "flask-restx==0.3.0",
        "gunicorn==20.1.0",
        "itsdangerous==1.1.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "jinja2==2.11.3; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "jsonpath-ng==1.5.2",
        "jsonschema==3.2.0",
        "kombu==5.0.2; python_version >= '3.6'",
        "markupsafe==1.1.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "ply==3.11",
        "prompt-toolkit==3.0.18; python_full_version >= '3.6.1'",
        "pyasn1==0.4.8",
        "pydantic==1.8.1",
        "pyrsistent==0.17.3; python_version >= '3.5'",
        "python-jose==3.2.0",
        "pytz==2021.1",
        "redis==3.5.3",
        "rsa==4.7.2; python_version >= '3.5' and python_version < '4'",
        "six==1.15.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "typing-extensions==3.7.4.3",
        "vine==5.0.0; python_version >= '3.6'",
        "wcwidth==0.2.5",
        "werkzeug==1.0.1",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
