import setuptools
import pymtts

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
requires_list = open('./requirements.txt', 'r', encoding='utf8').readlines()
requires_list = [i.strip() for i in requires_list]
print(requires_list)
setuptools.setup(
    name=pymtts.name,
    version=pymtts.VERSION,
    author="p1ay8y3ar",
    author_email="p1ay8y3ar@gmail.com",
    description="A python package for using Azure smart AI speech",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/p1ay8y3ar/pymtts",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requires_list
)
