import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cryocon-22c-controller",
    version="0.0.3.post1",
    author="Brian Carlsen",
    author_email="carlsen.bri@gmail.com",
    description="A package for controlling CryoCon 22C Temperature Controllers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['cryocon', 'cryocon 22c', 'temperature controller', 'cryostat', 'cryo'],
    url="https://github.com/bicarlsen/cryocon-22c-controller",
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