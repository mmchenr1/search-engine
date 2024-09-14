from indexer import parse_wiki
import pytest 

def test_parse_wiki():
    '''tests the parse_wiki function in indexer.py'''

    corpus_dict = dict()
    dict_ids_titles = dict()
    dict_ids_links = dict()
    parse_wiki("testwiki1.xml",corpus_dict, dict_ids_titles, dict_ids_links)
    
    assert corpus_dict is {
        1 : {
            "cat" : 1,
            "jump" : 1,
            "dog" : 1,
            "get" : 1,
            "side" : 1,
            "road" : 1,
        },

        2 : dict(),

        3 : {
            "cs@brown" : 1,
            "class" : 1,
            "second" : 1,
            "semest": 1,
            "freshmen" : 1,
            "take" : 1,
            "interest" : 1,
            "computer" : 1,
            "science" : 1,
        }
    }

    assert dict_ids_titles is {
        1:"A",
        2:"B",
        3:"C"
    }

    assert dict_ids_links is {
        1 : "dog",
        2 : list(),
        3 : "CS200",
    }

test_parse_wiki()