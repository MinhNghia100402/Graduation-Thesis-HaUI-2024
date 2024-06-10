import requests

# root_data = 'root_data.txt'
# with open(root_data,'r') as link_data:
#     links = link_data.readlines()
#     headers = {'Accept-Encoding': 'identity'}
#     r = requests.get(links[0].strip(), headers=headers)
#     print(r.text)
    
    
from llama_index.core import SummaryIndex
from llama_index.readers.web import SimpleWebPageReader
from IPython.display import Markdown, display
import os