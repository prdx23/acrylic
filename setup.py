import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="acrylic",
    version="0.2",
    author="Arsh",
    author_email="arsh@pydata.org",
    description="A simple and intuitive library to work with colors in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Arsh23/acrylic",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
    ],
    keywords='color colors scheme palette rgb hsv hsl ryb hex',
    project_urls={
        'Source': 'https://github.com/Arsh23/acrylic',
        'Tracker': 'https://github.com/Arsh23/acrylic/issues',
    },
    python_requires='>=3.6',
)
