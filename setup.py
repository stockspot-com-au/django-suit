from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name='django-suit',
    version=__import__('suit').VERSION,
    description='Modern theme for Django admin interface.',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author='Kaspars Sprogis (darklow), forked by @mhindery',
    author_email='info@djangosuit.com',
    url='http://djangosuit.com',
    packages=['suit', 'suit.templatetags'],
    python_requires='>=3.10',
    install_requires=[
        'Django>=5.2,<6.2',
    ],
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Framework :: Django :: 5.2',
        'Framework :: Django :: 6.0',
        'Framework :: Django :: 6.1',
        'License :: Free for non-commercial use',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Environment :: Web Environment',
        'Topic :: Software Development',
        'Topic :: Software Development :: User Interfaces',
    ]
)
