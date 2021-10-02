""" Package script to create a python dist
"""
from setuptools import setup
from ffmpeg_gui import __version__ as version
from ffmpeg_gui import __name__ as name

requirements = []
extra_requirements = {"dev": ["pylint>=2.0.0",
                              "wheel>=0.37.0",
                              "twine>=3.4.0"]}

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name=name,
    version=version,
    url='https://github.com/ThorpeJosh/ffmpeg-gui',
    license='MIT',
    author='Joshua Thorpe',
    author_email='josh@thorpe.engineering',
    description='FFMPEG GUI for some common and simple AV operations',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['ffmpeg', 'gui', 'audio', 'video', 'convert', 'stitch'],
    packages=['ffmpeg_gui'],
    include_package_data=True,
    install_requires=requirements,
    extras_require=extra_requirements,
    python_requires='>=3.7',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS'
    ],
    entry_points={
        'gui_scripts': [
            'ffmpeg-gui=ffmpeg_gui.__main__:run'
        ],
    },
)
