from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="obscuraflow",
    version="0.1.0",
    author="Robin Andreeklund",
    description="A workflow orchestration framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/robinandreeklund-collab/Obscuraflow",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[],
)
