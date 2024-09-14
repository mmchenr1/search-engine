import math
import sys
from xml.dom.minidom import Element
import nltk
from src.file_io import write_docs_file, write_title_file, write_words_file
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re
import xml.etree.ElementTree as et  #wiki files are stored in an xml tree
# each wiki/xml file is a root, children = pages, childrenx2 = title, id, text

'''
the indexer: 
    prepares corpus from wiki files
    determines relevance and authority of documents
 '''

def parse_wiki(xml_filepath: str, corpus_dict: dict, dict_ids_titles: dict, dict_ids_links: dict, dict_words_freq: dict, dict_words_ids: dict):
    '''
    creates corpus_dict for each page, dict mapping ids to titles, and dict of page ids to the links in that page

    Parameters:
    xml_filepath -- the filepath to the wiki file being parsed as a String
    corpus_dict -- the dict for the corpus to be stored in (dict of ids that maps to dictionaries of words to their counts)
    dict_ids_title -- the empty dictionary for ids to be mapped to titles
    dict_ids_links -- the empty dictionary that maps ids to the other pages as ids they link to
    dict_words_freq -- the empty dict to store all words in a corpus mapped to the number of pages they appear in 
    dict_words_ids -- the empty dict to store all the words in a corpus to the ids of the pages they appear in

    Returns: n/a
    '''

    root: Element = et.parse(xml_filepath).getroot() #the xml file

    #iterate through children nodes
    for page in root:
        # extract tiles as a str
        title: str = page.find('title').text.strip()

        #extract id as an int
        id: int = int(page.find('id').text)

        # map id to titles in a hashmap
        dict_ids_titles[id] = title

        # make corpus
        #  1. extract text from each page in a xml file
        text: str = page.find('text').text #do we need .strip() ?
        text = title + " " + text

        #  2. tokenize
        regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        all_words = re.findall(regex, text) 

        # links --> stored in dict_ids to links and replaced as how they appear in text
        links_list = []
        dict_ids_links[id] = links_list
        id_dict = dict()
        max_freq = 0
        STOP_WORDS = set(stopwords.words('english'))
        nltk_test = PorterStemmer()

        #for word in all_words:
        #for i in range(0, len(all_words), 1):
        i = 0
        while i < len(all_words):
            word = all_words[i]
            if '[[' and ']]' in word:
                all_words.remove(word)
                if '|' in word:

                    split_index = word.find('|')

                    #store the link in the dict_ids_links dictionary
                    linked_page = word[2 : split_index]
                    links_list.append(linked_page)
                    dict_ids_links[id] = links_list

                    #reduce to the word that appears in the corpus
                    word = word[split_index + 1 : len(word) - 2]

                else:
                    word = word[2 : len(word) - 2]
                    links_list.append(word)
                    dict_ids_links[id] = links_list
                
                word = re.findall(regex, word)

                for w in word:
                    w.lower()
                    if w not in STOP_WORDS:
                        w = nltk_test.stem(w)
                        all_words.append(w)
            
            else: #not a link
                word = word.lower()
                # update frequency of word to store within corpus dict + keep track of max frequency
                if word not in STOP_WORDS:
                    word = nltk_test.stem(word) 
                    if word in id_dict.keys():
                        new_value = id_dict[word] + 1
                        id_dict[word] = new_value
                        
                    else:
                        id_dict[word] = 1
                    
                    # if the freq of this word is greater than current max_freq --> update max_freq key to this word's freq
                    if id_dict[word] >= max_freq:
                        max_freq = id_dict[word]
                    
                    
                    # map words to a list of the page ids they appear in
                    if word in dict_words_ids.keys():
                        if id not in dict_words_ids[word]:
                            ids_list = dict_words_ids[word]
                            ids_list.append(id)
                            dict_words_ids[word] = ids_list

                    else:
                        dict_words_ids[word] = [id]
                    
                id_dict["max_freq"] = max_freq

                i = i + 1

        # STORE IN CORPUS DICT
        corpus_dict[id] = id_dict

        #populate dict_words_freq
        for word in id_dict.keys():
            if word != "max_freq":
                if word in dict_words_freq:
                    dict_words_freq[word] = dict_words_freq[word] + 1
                else:
                    dict_words_freq[word] = 1
                    

def relevance(corpus_dict: dict, dict_words_freq: dict, words_to_doc_relevance: dict, dict_words_ids: dict):
    '''
    generates a dictionary that maps words to ids to term relevance

    Parameters:
    corpus_dict -- dict mapping page ids to their terms + frequencies
    dict_words_freq -- dict mapping each words to the number of pages it appears in
    words_to_doc_relevance -- the dict being populated; maps words to ids to term relevance
    dict_words_ids -- the dict mapping each word in the corpus to the page ids that word appears in

    Returns: n/a
    '''

    #alternative:
    #mapping of word to the docs it appears in and their counts --> have inner for loop only go over the docs a word appears in
    #if a score doesn't appear in ---, it's 0


    num_docs = len(corpus_dict.keys())
    for word in dict_words_freq.keys():
        word_dict = dict()
        idf = math.log(num_docs / dict_words_freq[word])

        for page_id in dict_words_ids[word]: #change after 'in' to only go through the specific docs to that word

            #if word in corpus_dict[page_id]:
            max_freq = corpus_dict[page_id]["max_freq"]
            tf = corpus_dict[page_id][word] /  max_freq

            relevance = tf*idf

            word_dict[page_id] = relevance
        
        words_to_doc_relevance[word] = word_dict


def euclid_dist(r: dict, r_prime: dict):
    ''' Calculates the Euclidian Distance between r and r_prime, assuming both have same dimensions and are not empty
    
    Paramteters:
    x1 -- the first dictionary containing float entries
    x2 -- the second dictionary containing float entries
    
    Returns:
    a float representing the distance between r and r_prime'''

    entries = []
    for i in r.keys():
        new_entry = (r_prime[i] - r[i]) ** 2
        entries.append(new_entry)
    
    return math.sqrt(sum(entries))


def pagerank(dict_ids_links: dict, dict_ids_titles: dict):
    '''
    populates dictionary of ids to pageranks

    Parameters:
    dict_ids_links -- a dict that maps page ids to the links contained in that page

    Returns: n/a
    '''

    n = len(dict_ids_titles.keys())
    dict_pagerank = dict()

    #PART 1: CALCULATE WEIGHTS:
    dict_page_weights = dict()
    for page_id in dict_ids_titles.keys():
        # dict to stores weight from page_id to each page
        weights_dict = dict()

        # get ride of repeats and link to itself
        links_list_raw = dict_ids_links[page_id]
        links_list = [i for n, i in enumerate(links_list_raw) if i not in links_list_raw[:n] and i != dict_ids_titles[page_id]] # distincts elts in list

        #remove links to pages outside of corpus
        for link in dict_ids_links[page_id]:
            if link not in dict_ids_titles.values() and link in links_list:
                links_list.remove(link)

        #distinct number of links from this page
        nk = len(links_list)

        for page in dict_ids_titles.keys():

            if links_list == [] and page_id != page:
                #if links list is empty, considered to link once to everywhere except to themselves
                weight = 0.15/n + 0.85/(n-1)

            # if has links (list not empty)
            elif dict_ids_titles[page] in links_list:
                weight = 0.15/n + 0.85/nk

            # sets weight from a page to iself + sets weights to pages not linked to
            else:
                weight = 0.15/n

            #add weight to weights dict
            weights_dict[page] = weight
        
        dict_page_weights[page_id] = weights_dict

    #PART 2: RANKS!
    r = {}
    r_prime = {}

    for key in dict_ids_titles.keys():
        r[key] = 0
        r_prime[key] = 1/n

    pages = dict_ids_titles.keys()
    while euclid_dist(r, r_prime) > 0.001:
        #move r_prime to r
        r = r_prime.copy()
        for j in pages:
            r_prime[j] = 0
            for k in pages:
                r_prime[j] = r_prime[j] + dict_page_weights[k][j] * r[k]
    
    dict_pagerank = r_prime
    return dict_pagerank


def indexer(xml_filepath: str, titles_filepath: str, docs_filepath: str, words_filepath: str):
    ''' The indexer that processes an XML document into a list of terms, determines the 
    relevance between terms and documents, and determines the authority of each document.
    
    Parameters:
    xml_filepath -- the filepath to the wiki file being used to generate the indexer
    titles_filepath -- the document that titles will get written to
    docs_filepath -- the document that docs will be written to in order of pagerank
    words_filepath -- the document that words to ids to nu appearances will be written to 
    
    Returns: n/a
    '''

    #Parse
    corpus_dict = dict()
    dict_ids_titles = dict()
    dict_ids_links = dict()
    dict_words_freq = dict()
    dict_words_ids = dict()
    parse_wiki(xml_filepath,corpus_dict, dict_ids_titles, dict_ids_links, dict_words_freq, dict_words_ids)

    #PageRank
    dict_pagerank = pagerank(dict_ids_links, dict_ids_titles)

    #Relevance
    words_to_doc_relevance = dict()
    relevance(corpus_dict, dict_words_freq, words_to_doc_relevance, dict_words_ids)

    #Write to files
    write_title_file(titles_filepath, dict_ids_titles)
    write_docs_file(docs_filepath, dict_pagerank)
    write_words_file(words_filepath, words_to_doc_relevance)


if __name__ == "__main__":
    '''indexer written as a main method so that we can run it in the terminal!
    arguments passed in as: <XML filepath> <titles filepath> <docs filepath> <words filepath>'''
    if len(sys.argv) == 5:
        xml_filepath = sys.argv[1] 
        titles_filepath = sys.argv[2]
        docs_filepath = sys.argv[3]
        words_filepath = sys.argv[4]

        indexer(xml_filepath, titles_filepath, docs_filepath, words_filepath)

    else:
        print("Sorry, incorrect number of arguments!")