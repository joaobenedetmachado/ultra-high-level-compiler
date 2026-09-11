"""Setup script for the ultra high-level language compiler."""

from pathlib import Path

from setuptools import find_packages, setup

readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="ultra-high-level-compiler",
    version="1.0.0",
    description="Compilador de linguagem natural em portugues que gera codigo Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jean Reinhold",
    author_email="jeanpaulreinhold@gmail.com",
    url="https://github.com/joaobenedetmachado/ultra-high-level-compiler",
    packages=find_packages(),
    py_modules=["cli"],
    python_requires=">=3.7",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "uhl-compile=cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Compilers",
        "Topic :: Software Development :: Code Generators",
    ],
    keywords="compilador linguagem-natural portugues python geracao-de-codigo",
)
