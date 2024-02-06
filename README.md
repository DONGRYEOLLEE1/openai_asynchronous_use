# openai_asynchronous_use
Openai API Asynchronously Using Script

- In my case, Implemented an automatic labelling system.
- For training dataset, I processed a huge dataset that approximately 130k.

# asynchronous batch size test

- In my case, Used a total of 201 data and checked duration by batch size
- There is no guarantee that increasing the batch size further than this will reduce time.
- For reference, my openai api tier is 4.

||sequential parse|Asynchronous parse1|Asynchronous parse2|
|---|---|---|---|
|Volume|201|201|201|
|Batch size|-|100|50|
|Duration (sec)|733|**164.9**|478.82|

# Install

```script
$ pip install -U openai 
```
