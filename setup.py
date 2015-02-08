from setuptools import setup, find_packages
setup(
    name='FileTrack',
    get_version_from_scm=True,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'filetrack = filetrack.cli:main',
        ],
    },
    setup_requires=[
        'hgdistver',
    ],
    install_reqires=[
        'micromigrate',
        'click',
    ]
)
