from setuptools import setup, find_packages

setup(
    name="Udacity",
    packages=find_packages(),
    include_package_data=True,
    version="2.0.0-beta",
    description="It's pip...",
    python_requires='>=3.7',
    keywords=['pip', 'Udacity'],
    install_requires=open("requirements.txt").readlines(),
    entry_points={
        "console_scripts": [
            "udacity=udacity.cli:main",
        ],
    },
)
