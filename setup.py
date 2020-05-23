import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spotipie-toelapiut",
    version="0.0.1",
    author="Apiut Toel",
    author_email="toelapiut7@gmail.com",
    description="Integrate Spotify with any python project in the shortest way possible, with least efforts possible. "
                "The package provides authorization, search and many more other handy add-ons to simplify your "
                "integration.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/toelapiut/Spotipie",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
