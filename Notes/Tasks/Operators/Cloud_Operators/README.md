<!-- omit in toc -->
# Introduction
Take note of operators for cloud API.

<br />

<!-- omit in toc -->
# Table of Contents
- [AWS](#aws)
  - [1. Arguments of SageMaker](#1-arguments-of-sagemaker)
    - [1.1. wait_for_completion](#11-wait_for_completion)

<br />

# AWS

## 1. Arguments of SageMaker

### 1.1. wait_for_completion
* True: wait for the given task to complete. 
  > Operators internally poll every X seconds to check whether the job is running
* False: only taking action and not following up on
