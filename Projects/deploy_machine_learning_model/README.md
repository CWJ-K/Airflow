<!-- omit in toc -->
# Table of Contents
- [Introduction](#introduction)
- [Structure](#structure)
  - [Logic Steps of an Offline Part](#logic-steps-of-an-offline-part)

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

## Logic Steps of an Offline Part

```mermaid
flowchart LR
    raw_data --copy data to own account -->
    raw_data_in_own_account;
    raw_data_in_own_account --transform_data_to_useful_format-->processed_data_in_own_account;
    processed_data_in_own_account -- train_model-->SageMaker_model;
    SageMaker_model--deploy model-->SageMaker_endpoint; 

```