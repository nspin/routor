from distutils.core import setup

setup(
    name = 'routor',
    version='0.0.1',
    description="Tor controller that allows paths to be chosen on a stream-by-stream basis.",
    author='Nick Spinale',
    license='MIT',
    packages=['routor'],
    install_requires=[
        'bidict',
        'stem',
    ],
)