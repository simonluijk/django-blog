"""
Based entirely on Django's own ``setup.py``.
"""
from distutils.core import setup

# Dynamically calculate the version
version_tuple = __import__('blog').VERSION
if version_tuple[2] is not None:
    version = "%d.%d_%s" % version_tuple
else:
    version = "%d.%d" % version_tuple[:2]

setup(
    name='django-blog',
    description='Yet another django blog',
    version=version,
    author='Simon Luijk',
    author_email='simon@simonluijk.com',
    url='http://www.apricotwebsolutions.com/blog/',
    packages=[
        'blog',
        'blog.templatetags'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ],
)
