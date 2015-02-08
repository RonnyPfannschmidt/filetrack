from setuptools import setup, find_packages
setup(
    name='FileTrack',
    get_version_from_scm=True,
    packages=find_packages(),
    setup_requires=[
        'hgdistver',
    ],
)
