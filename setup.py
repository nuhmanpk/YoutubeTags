import pathlib
import setuptools


file = pathlib.Path(__file__).parent

README = (file / "README.md").read_text()

setuptools.setup(
    name="YoutubeTags",
    version="1.2.6",
    author="Nuhman Pk",
    author_email="nuhmanpk7@gmail.com",
    long_description = README,
    long_description_content_type = "text/markdown",
    description="YoutubeTags is a python third-party api wrapper to Extract Youtube Video Tags without Youtube API",
    license="MIT",
    url="https://github.com/bughunter0/YoutubeTags",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(include=['YoutubeTags']),
    install_requires=[
        'bs4',
        'requests',
        'html5lib',
    ],
    python_requires=">=3.6",
)
