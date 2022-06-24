<!-- omit in toc -->
# Table of Contents
- [Introduction](#introduction)
- [Structure of this Repository](#structure-of-this-repository)
- [Writing Conventions](#writing-conventions)
  - [1. Copy the Template Structure to Markdown](#1-copy-the-template-structure-to-markdown)
  - [2. Ensure to Keep Capital of Directories in Git](#2-ensure-to-keep-capital-of-directories-in-git)

<br />

# Introduction

I believe note-taking helps me learn more about Airflow. Therefore, I created this repository.

The repository includes Airflow notes and projects, which help understand the features of Airflow and how to apply the features in different cases.

Main Reference: [Data Pipelines With Apache Airflow](https://github.com/BasPH/data-pipelines-with-apache-airflow)

<br />

# Structure of this Repository

* Notes
  * Structure
    * Components
    * Configuration
  * DAGs
  * Tasks
    * Operators
      * Operators
      * Cloud Operators
      * Dynamic References 
      * Big Data Transformations
    * Sensors
    * Dependency
    * Data Transfer
      * Between Systems
      * Between Tasks
    * Custom Operations
    * Hooks
  * Tests
  * Package

-----
* Projects
  * Collect images of Rockets
  * Deploy Machine Learning Model (WIP)
  * Download Wikipedia Page Views
  * Transfer Data Between Systems (WIP)
  * Write CI/CD Tests in Airflow (WIP)
  * Build Custom Components
  * Use Virtualization in Airflow
  * Find the Fastest Way to Get Around NYC (WIP)


<br />

# Writing Conventions

> Naming convention: using questions or long words help fast understand the whole picture instead of short words

* Introduction
  * why I write this note
* Fundamental Concepts (Optional)
  * concepts without commands
  * pictures
* Commands 
  * how to install
* Arguments (Optional)
  * introduction of arguments
  * package name

<br />

## 1. Copy the Template Structure to Markdown

```
<!-- omit in toc -->
# Introduction

<br />

<!-- omit in toc -->
# Table of Contents

<br />

# Fundamental Concepts

<br />

# Commands 

<br />

# Arguments


```

## 2. Ensure to Keep Capital of Directories in Git
```
git config core.ignorecase false
```



