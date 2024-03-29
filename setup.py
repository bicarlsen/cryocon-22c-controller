import setuptools

# get __version__
exec( open( 'cryocon_22c_controller/_version.py' ).read() )

with open("README.md", "r") as fh:
    long_description = fh.read()

project_urls = {
    'Source Code': 'https://github.com/bicarlsen/cryocon-22c-controller',
    'Bug Tracker': 'https://github.com/bicarlsen/cryocon-22c-controller/issues'
}

setuptools.setup(
    name="cryocon-22c-controller",
    version=__version__,
    author="Brian Carlsen",
    author_email="carlsen.bri@gmail.com",
    description="A package for controlling CryoCon 22C Temperature Controllers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['cryocon', 'cryocon 22c', 'temperature controller', 'cryostat', 'cryo'],
    url="https://github.com/bicarlsen/cryocon-22c-controller",
    project_urls = project_urls,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha"
    ],
    install_requires=[
        'easy-scpi',
        'pyvisa-py'
    ]
)