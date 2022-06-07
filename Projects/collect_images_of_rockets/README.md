<!-- omit in toc -->
# Introduction
Collect rocket images to fetch next launch

<br />

<!-- omit in toc -->
# Table of Contents
- [Pipelines](#pipelines)
- [Files Storage](#files-storage)
<br />

# Pipelines

```mermaid
graph TD;
    fetch_next_rocket_launch_information--save information into json format-->fetch_pictures_of_rockets_based_on_url;
    fetch_pictures_of_rockets_based_on_url--save images -->notice_the_next_launch;
```

<br />

# Files Storage
files can store in tmp/ of scheduler container
> share information between tasks by persisting data to /tmp location