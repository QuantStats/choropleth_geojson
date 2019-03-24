import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="choropleth_geojson",
    version="0.0.3",
    author="Wei Ruen Leong",
    author_email="wei.leong2@uqconnect.edu.au",
    description="Plot a choropleth map with a geojson file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/QuantStats/choropleth_geojson",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
