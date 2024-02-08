# Openai_asynchronous_use
Openai API Asynchronously Using Script

- In my case, Implemented an automatic labelling system.
- For training dataset, I processed a huge dataset that approximately 130k.

# Pipeline

![](./assets/asynchronous-automatic-labeling-pipeline.png)

# Asynchronous batching test

- In my case, Used a total of 201 data and checked duration by batch size
- There is no guarantee that increasing the batch size further than this will reduce time.

||sequential parse|Asynchronous parse1|Asynchronous parse2|
|---|---|---|---|
|Volume|201|201|201|
|Batch size|-|100|50|
|Duration (sec)|733|**164.9**|478.82|

# Actual processing duration

- To address TPM or RPM errors, data slicing was performed in batches of 50,000 using an asynchronous mechanism for automatic labeling.
- It is recommended to proceed with caution when labeling using APIs, as resource consumption upon encountering errors can be burdensome.
- I set the batch size to `200`.
- For reference, my openai api tier is 4.

||0 ~ 49999|50000 ~ 99999|100000 ~|
|---|---|---|---|
|Number of Errors|2|7|-|
|Duration (sec)|76498.91|68978.05|-|

# Install & Usage

```script
$ pip install -U openai 
$ python asynchronous.py
```
