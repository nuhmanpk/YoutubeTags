import pathlib
import setuptools

file = pathlib.Path(__file__).parent

README = (file / "README.md").read_text()

setuptools.setup(
    name="YoutubeTags",
    version="1.0",
    author="Nuhman",
    author_email="nuhmanpk7@gmail.com",
    long_description = README,
    long_description_content_type = "text/markdown",
    description="Simple Python Library to Extract YouTube Video Tags",
    license="MIT",
    url="https://github.com/bughunter0/YoutubeTags",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    install_requires = [],
    python_requires=">=3.6",
    
)
