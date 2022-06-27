<!-- omit in toc -->
# Introduction
How to package custom components in a sub-package within the DAGs directory?


<br />

<!-- omit in toc -->
# Table of Contents
- [why to package custom components?](#why-to-package-custom-components)
- [How to package](#how-to-package)
  - [1. Python package](#1-python-package)
- [How to deploy the package](#how-to-deploy-the-package)
  - [1. distribute to GitHub repository and install directly from it](#1-distribute-to-github-repository-and-install-directly-from-it)
  - [2. use a pip package feed such as PyPI](#2-use-a-pip-package-feed-such-as-pypi)
  - [3. install from a file-based location](#3-install-from-a-file-based-location)

<br />

# why to package custom components?
  * share the components in other projects
  * perform more rigorous testing (CICD) on custom components by keeping the code separate from DAGs

<br />

# How to package

## 1. Python package
* setuptools

<br />

# How to deploy the package

## 1. distribute to GitHub repository and install directly from it
```linux
    python -m pip install git+https://
```

## 2. use a pip package feed such as PyPI
```linux
    python -m pip install airflow_movielens
```

## 3. install from a file-based location
* make sure the Airflow environment can access the directory