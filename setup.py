from setuptools import setup, find_packages

setup(
    name='unreal-project-manager',
    version='0.1.4',
    packages=find_packages(where='.'),
    include_package_data=True,
    install_requires=[
        'python-dotenv'
    ],
    entry_points={
        'console_scripts': [
            'upm=upm.__main__:main'
        ]
    },
    package_data={
        'upm': ['*.upm', '*.txt']
    },
    author='Brandt Frazier',
    author_email='brandt@frazimuth.me',
    description='A lightweight Python module for managing Unreal projects across space, time, and platforms.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/crashtestbrandt/unrealprojectmanager',
    ckassifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.10'
)