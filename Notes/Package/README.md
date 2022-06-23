<!-- omit in toc -->
# Introduction
How to package custom components in a sub-package within the DAGs directory?


<br />

<!-- omit in toc -->
# Table of Contents
- [why to package custom components?](#why-to-package-custom-components)
- [How to package](#how-to-package)
  - [Python package](#python-package)
- [How to deploy](#how-to-deploy)
  - [distribute to GitHub repository and install directly from it](#distribute-to-github-repository-and-install-directly-from-it)
  - [use a pip package feed such as PyPI](#use-a-pip-package-feed-such-as-pypi)
  - [install from a file-based location](#install-from-a-file-based-location)

<br />

# why to package custom components?
  * share the components in other projects
  * perform more rigorous testing (CICD) on custom components by keeping the code separate from DAGs

<br />

# How to package
## Python package
* setuptools

<br />

# How to deploy
## distribute to GitHub repository and install directly from it
```linux
    python -m pip install git+https://
```

## use a pip package feed such as PyPI
```linux
    python -m pip install airflow_movielens
```

## install from a file-based location
* make sure the Airflow environment can access the directory