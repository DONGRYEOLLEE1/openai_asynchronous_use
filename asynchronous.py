import time
import openai
import asyncio
import pandas as pd

from tqdm import tqdm
from typing import List, Dict, Any
from packaging import version
from openai import AsyncOpenAI

if version.parse(openai.__version__) < version.parse("1.6.0"):
    raise ValueError("If you wanna use a gpt-4-1106-preview model, Please update version at latest 1.6.0. >> pip install -U openai")


# Initialization
api_key = "..."
client = AsyncOpenAI(api_key = api_key)     # This is the default and can be omitted

async def chat_completion(prompt: str) -> Dict[str, Any]:
    r"""
    - Asynchronously request an openai api. 
    - Detail is [HERE](https://github.com/openai/openai-python/blob/main/README.md)
    
    Args:
        prompt (str): Your prompt.
    
    Returns:
        response (Dict[str, Any]): `openai.AsyncOpenAI.client.chat.completions.create()` response that corresponding to your prompt.
    
    """
    response = await client.chat.completions.create(
        model = "gpt-3.5-turbo-1106",
        messages = [
            {"role": "user", "content": prompt}
        ]
    )
    
    return response

async def label_text_async(text: str) -> str:
    r"""
    - Asynchronously labels a given text with categories using function of chat_completion.
    - If outputs is resulted "none" in first prompt, the second category(minor category) for that text will automatically be "none".
    
    Args:
        text (str): data to be labeled.
    Returns:
        second_category (str): Result in after 2 prompts.
    """
    
    first_prompt = f"""... {text}"""

    # Assuming chat_completion returns a result with choices attribute
    result = await chat_completion(first_prompt)
    first_category = result.choices[0].message.content

    # Initialize second prompt
    second_prompt = ""
    
    if first_category == "...":
        second_prompt = f"""..."""
    elif first_category == "...":
        second_prompt = f"""..."""
    else:
        pass
    
    if first_category == "none":
        second_category = "none"
    else:
        result = await chat_completion(second_prompt)
        second_category = result.choices[0].message.content
        
    return second_category


async def label_text_async_batch(text_batch: List[str]) -> List[str]:
    r"""
    Asynchronously labels a batch of texts.
    
    Args:
        text_batch (List[str]): List of texts to be labeled.
        
    Returns:
        results (List[str]): List of labels corresponding to each text.
    """
    
    tasks = [label_text_async(text.strip()) for text in text_batch]
    results = await asyncio.gather(*tasks)
    return results

async def main(batch_size: int) -> None:
    r"""
    Main function to process a large dataset of texts asynchronously.
    
    1. Loads a list of texts from a DataFrame.
    2. Divides the texts into batches for efficient processing.
    3. Labels each batch of texts asynchronously using label_text_async_batch function that will be outputting a list data [label_{1}, label_{2}, ..., label_{batch_size}].
    4. Labeled data will be concatenated to f_df.
    5. Save to main directory.
    
    Args:
        batch_size (int): Divides texts by batch_size
        
    Return:
        None
    """
    
    # data load
    df = pd.read_csv("...")
    text_list = df['text'].to_list()
    
    # frame data initialization
    f_df = pd.DataFrame(columns = ['text', 'minor_category'])
    
    for i in tqdm(range(0, len(text_list), batch_size), desc = 'Asynchronous Response Iterator'):
        
        text_batch = text_list[i:i+batch_size]
        
        try:
            batch_results = await label_text_async_batch(text_batch)    # ex) ["label_1", "label_2", ..., "label_{batch_size}"], [...], ...
        
        except Exception as e:
            print(f"API Error Occurred: {e}")
            
            try:
                await asyncio.sleep(60)
                batch_results = await label_text_async_batch(text_batch)
                
            except (openai.RateLimitError or openai.Timeout or openai.APIConnectionError or openai.APIError) as e2:
                print(f"Consecutive Error: {e2}")
                f_df.reset_index(drop = True).to_csv("./main-tmp.csv", index = False)
            
        tmp = pd.DataFrame(data = {"text": text_batch, "minor_category": batch_results})
        f_df = pd.concat([f_df, tmp])
    
    f_df.reset_index(drop = True).to_csv("./main.csv", index = False)



if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main(batch_size = 200))   # tweak batch_size whatever you want
    print(f"end of time: {time.time() - start_time}")