<!-- omit in toc -->
# (WIP)

<!-- omit in toc -->
# Table of Contents
- [Introduction](#introduction)
- [Structure](#structure)
  - [Logic Steps of the Offline Part](#logic-steps-of-the-offline-part)
  - [Steps of the Online Part](#steps-of-the-online-part)
    - [AWS Chalice](#aws-chalice)

<br />

# Introduction 
The project is to develop a machine learning model, working with AWS S3 buckets and AWS SageMaker.

* Dataset: [MNIST](http://yann.lecun.com/exdb/mnist/) - a database of handwritten digits

* Goal: identify handwritten digits

* Tools: 

<br />


# Structure

```mermaid
flowchart TD
    subgraph Offline 
        direction LR
    collect_handwritten_digits_image_data -- train_model --> prediction_modelling;

    end

    subgraph Online
    give_unseen_handwritten_digit_image --REST API--> prediction_modelling;
    prediction_modelling --> classify_unseen_handwritten_digit_image 
    end

```

## Logic Steps of the Offline Part

```mermaid
flowchart TD
    raw_data --copy data from a public bucket to our own bucket -->
    raw_data_in_own_account;
    raw_data_in_own_account --transform_data_to_useful_format-->processed_data_in_own_account;
    processed_data_in_own_account -- train_model-->SageMaker_model;
    SageMaker_model--deploy model-->SageMaker_endpoint; 

```


## Steps of the Online Part
* AWS SageMaker endpoint **only** can be accessible via AWS APIS
  * If want HTTP endpoint to SageMaker, **AWS lambda** is required to as a bridge between SageMaker and HTTP endpoint
* API is implemented with AWS Chalice
  > only deploy as one-offs, so not deploy infrastructure

### AWS Chalice
* a Python framework similar to Flask
* automatically generates the API gateway and lambda resources in AWS



```mermaid
flowchart RL
    subgraph Offline 
        direction RL
    SageMaker_endpoint
    end

    subgraph Online
        direction RL
    AWS_Lambda --> SageMaker_endpoint ; 
    AWS_API_Gateway --> AWS_Lambda;
    end

    subgraph User
        direction RL
    Users --> AWS_API_Gateway 
    end

```
