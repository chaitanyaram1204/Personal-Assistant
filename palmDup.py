
"""
Created on Thu Oct  5 23:32:22 2023

@author: CHAITANYA
"""

import pprint
import google.generativeai as palm

def talk_to_palm(data):

    palm.configure(api_key='AIzaSyCfB8zi95jtaf7T74gKxki4zVDoYWqarOk')
    
    
    models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
    model = models[0].name

    
    completion = palm.generate_text(
        model=model,
        prompt=data,
        temperature=0,
        # The maximum length of the response
        max_output_tokens=1600,
    )

    print(completion.result)
    return completion.result
