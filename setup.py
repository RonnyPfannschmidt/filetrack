from setuptools import setup, find_packages
setup(
    name='FileTrack',
    version_from_scm=True,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'filetrack = filetrack.cli:main',
        ],
    },
    setup_requires=[
        'setuptools_scm',
    ],
    install_requires=[
        'micromigrate',
        'click',
        'scandir',
    ]
)
