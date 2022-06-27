<!-- omit in toc -->
# Introduction
Sometimes, it is convenient to apply an operator to transfer data between two different systems. What is the type of this operator? How can we use it?

<br />

<!-- omit in toc -->
# Table of Contents
- [Fundamental Concepts](#fundamental-concepts)
  - [1. A-to-B operators](#1-a-to-b-operators)
  - [2. Customized A-to-B operators](#2-customized-a-to-b-operators)

<br />

# Fundamental Concepts

## 1. A-to-B operators
* to transfer data between two systems
* e.g.
  * Query MySQL database and Store the results on Google Cloud Storage
  * Copy data from SFTP server to AWS S3
  * call an HTTP REST API and store them in other systems

<br />

## 2. Customized A-to-B operators
* Look at the source code of other similar A-to-B operators to develop A-to-B operators 
  > Take reference from: MongoToS3Operator, S3ToSFTPOperator, SFTPToS3Operator, MySqlToGoogleCloudStorageOperator
  * Note: Pay attention to below
    1. Are data stored in memory or the disk?
    2. make sure enough memory on the Airflow machine/disk space in the process of data transfer






