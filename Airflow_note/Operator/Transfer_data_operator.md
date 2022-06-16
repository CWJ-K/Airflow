<!-- omit in toc -->
# Introduction
Take notes of A to B operators.

<br />

<!-- omit in toc -->
# Table of Contents
- [Fundamental Concepts](#fundamental-concepts)
  - [A-to-B operators](#a-to-b-operators)
  - [Customized A-to-B operators](#customized-a-to-b-operators)
- [MySqlToGoogleCloudStorageOperator](#mysqltogooglecloudstorageoperator)
- [SFTPToS3Operator](#sftptos3operator)
- [SimpleHttpOperator](#simplehttpoperator)

# Fundamental Concepts
## A-to-B operators
* to transfer data between two systems
* e.g.
  * Query MySQL database and Store the results on Google Cloud Storage
  * Copy data from SFTP server to AWS S3
  * call an HTTP REST API and store them in other systems

## Customized A-to-B operators
* Look at the source code of other similar A-to-B operators to develop A-to-B operators 
  > e.g. MongoToS3Operator, S3ToSFTPOperator
  * Note: Pay attention to 
    1. store data in memory or in disk
    2. make sure enough memory on the Airflow machine/disk space in the process of data transfer

# MySqlToGoogleCloudStorageOperator
# SFTPToS3Operator
# SimpleHttpOperator

