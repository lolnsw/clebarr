from setuptools import setup, find_packages

setup(
    name="clebarr",
    version="0.1.0",
    packages=find_packages(include=["app", "app.*"]),
    python_requires=">=3.11",
    install_requires=[
        line.strip()
        for line in open("requirements.txt")
        if line.strip() and not line.startswith("#")
    ],
) 