from bs4 import BeautifulSoup
import requests, lxml, os, re
import pandas as pd
import numpy as np
import time

headers = {
            'User-agent':
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
            }


def extract_number(results_list:list) -> str:

    result_num = 0
    
    for term in results_list:
        selected_text = re.findall('about', term.lower())
        if selected_text:
            print(selected_text)
            result_num = re.findall('about (.*) results', term.lower())[0]
            result_num = re.sub(',', '', result_num)
            result_num = int(result_num)

    return result_num

def scrape_number_of_results(phrase:str)->int:

    
    params = {"q": phrase, "hl": "en"}
    html = requests.get('https://scholar.google.com/scholar', headers=headers, params=params).text
    soup = BeautifulSoup(html, 'lxml')
    time.sleep(0.8)
        
    # the dictionary will be collected here
    results_list = []

    # Container where all needed dict_ is located
    for result in soup.select('.gs_ab_mdw'):
        results_list.append(result.text)

    result_num = extract_number(results_list)
    
    return result_num

def determine_node_size(phrases:list) -> dict:
    """
    get the list of phrases
    output a dictionary of their size (number of search results for each phrase)
    """
    sizes_dict = {}
    # single term search for size of node
    for phrase in phrases:
        sizes_dict[phrase] = scrape_number_of_results(phrase)
        
    return sizes_dict

def create_graph(phrases):
    
    graph_ = {'nodes':[], 'links':[]}
    
    sizes_dict =  determine_node_size(phrases)

    
    # for nodes
    # {'nodes' : [{'id': , 'group':2 , 'size':name_freq[char]}]}
    for term, numb_ in sizes_dict.items():
        graph_['nodes'].append({'id': term, 'group': 1, "size":float(np.log(numb_)) })
    
    list_of_phrase_comb = []
    # combination of terms
    for i in range(len(phrases)):
        for j in range(len(phrases)):
            if i>j:
                new_phrase = "\"" + phrases[i] + "\"" + " AND " + "\"" + phrases[j] + "\""
                print(new_phrase)
                results_num = scrape_number_of_results(phrase=new_phrase)

                graph_['links'].append({'source': phrases[i], 
                                        'target': phrases[j],
                                        'value': float(results_num), 
                                        'color': float(results_num)})
    
    
    return graph_

graph_ = create_graph(phrases=[
    'natural language processing', 'decision support systems', 
    'clinical setting', 'artificial intelligence' , 'healthcare'
    ])