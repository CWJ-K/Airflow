<!-- omit in toc -->
# Introduction
Collect rocket images to fetch next launch

<br />

<!-- omit in toc -->
# Table of Contents
- [Pipelines](#pipelines)
<br />

# Pipelines

```mermaid
graph TD;
    fetch_pageviews_data_of_wiki--save data into gz files-->extract_gz_files;
    extract_gz_files-->fetch_specifc_pageviews_data;
    fetch_specifc_pageviews_data--store in sql file-->wrtie_data_to_postgres
```