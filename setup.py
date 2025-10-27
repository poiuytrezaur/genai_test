"""Setup configuration for Weather App."""

from pathlib import Path

from setuptools import find_packages, setup

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="weather-app",
    version="1.0.0",
    author="Weather App Team",
    author_email="info@weatherapp.com",
    description="A modular weather application with user management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/poiuytrezaur/genai_test",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=[
        "Flask>=3.0.0",
        "Flask-SQLAlchemy>=3.1.1",
        "Werkzeug>=3.0.1",
        "requests>=2.31.0",
        "SQLAlchemy>=2.0.23",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "ruff>=0.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "weather-app=backend.app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["frontend/templates/*.html", "frontend/static/**/*"],
    },
)
