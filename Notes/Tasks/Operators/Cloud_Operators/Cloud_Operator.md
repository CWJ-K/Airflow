<!-- omit in toc -->
# Introduction
Take note of operators for cloud API.

<br />

<!-- omit in toc -->
# Table of Contents
- [AWS](#aws)
  - [SageMaker](#sagemaker)
    - [wait_for_completion](#wait_for_completion)

# AWS
## SageMaker
### wait_for_completion
* True: wait for the given task to complete. 
  > Operators internally poll every X seconds to check whether the job is running
* False: only taking action and not following up on
