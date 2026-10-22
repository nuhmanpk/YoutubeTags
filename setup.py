import pathlib
import setuptools

file = pathlib.Path(__file__).parent

README = (file / "README.md").read_text(encoding="utf-8")

setuptools.setup(
    name="YoutubeTags",
    version="1.5",
    author="Nuhman Pk",
    author_email="nuhmanpk7@gmail.com",
    long_description = README,
    long_description_content_type = "text/markdown",
    description="YoutubeTags is a python third-party api wrapper to Extract Youtube Video Tags without Youtube API",
    license="MIT",
    url="https://github.com/nuhmanpk/YoutubeTags",
    project_urls={
        "Documentation": "https://youtubetags.readthedocs.io",
        "Source": "https://github.com/nuhmanpk/YoutubeTags",
        "Issues": "https://github.com/nuhmanpk/YoutubeTags/issues",
    },
    keywords="youtube tags seo youtube-tags scraper keywords hashtags",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=setuptools.find_packages(include=['YoutubeTags']),
    install_requires=[
        'beautifulsoup4>=4.6',
        'requests>=2.20'
    ],
    entry_points={
        "console_scripts": ["youtubetags=YoutubeTags.cli:main"],
    },

    python_requires=">=3.6",

)
