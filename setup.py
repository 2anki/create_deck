from setuptools import setup, find_packages

setup(
    name="twoanki",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "aioredis>=2.0.0",
        "genanki==0.13.1",
        "pydantic>=1.8.0,<3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.18.0",
            "pytest-cov>=3.0.0",
            "httpx>=0.23.0",
        ],
    },
) 