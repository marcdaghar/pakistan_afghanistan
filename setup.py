from setuptools import setup, find_packages

setup(
    name="yusuf-counter-cycle",
    version="1.0.0",
    author="Marc Daghar",
    description="Modèle formel du contre-cycle de Yusuf pour le Pakistan et l'Afghanistan",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="CC BY-SA 4.0",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "streamlit>=1.28.0",
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "plotly>=5.17.0",
        "scipy>=1.11.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
