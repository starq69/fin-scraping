import setuptools

setuptools.setup(
    name="fin-scraping",
    version="0.1.0",
    url="https://github.com/starq69/cookiecutter-pypackage-minimal",

    author="Sergio Tarquini",
    author_email="starq69@mail.com",

    description="financial scraper",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
