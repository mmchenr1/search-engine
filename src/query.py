import re
import sys
from src.file_io import read_docs_file, read_title_file, read_words_file
from nltk.stem import PorterStemmer

def get_results(query: list, condition: bool, words_to_doc_relevance: dict, pagerank_dict: dict, dict_ids_titles: dict) -> list:
    '''takes in query and pagerank condition, generates list of top 10 results
    
    Parameter:
    query -- the List of Strings corresponding to the query passed into the terminal
    condition -- a Boolean specifying true if pagerank should be used
    words_to_doc_relevance -- dict mapping words to the pageids they appear in along with the relevance on that page
    pagerank_dict -- dict mapping page ids to their pagerank
    dict_ids_titles -- dict mapping ids to the page title
    
    Results:
    a list of the top 10 documents to match the query
    '''

    relevancy_tracker = dict()

    for word in query:
        #find in dict
        #handle if query word doesn't show up in corpus
        try:
            id_to_relevancy_dict = words_to_doc_relevance[word]
        except(KeyError):
            id_to_relevancy_dict = {}

        for page_id in id_to_relevancy_dict.keys():
            if page_id in relevancy_tracker.keys():
                relevancy_tracker[page_id] = relevancy_tracker[page_id] + id_to_relevancy_dict[page_id]
            else:
                relevancy_tracker[page_id] = id_to_relevancy_dict[page_id]
            
    if condition == True:
        for page_id in relevancy_tracker.keys():
            pagerank = pagerank_dict[page_id]
            relevancy_tracker[page_id] = relevancy_tracker[page_id] * pagerank

    #sort relevancy_tracker --> in list structure
    sorted_list = sorted(relevancy_tracker.items(), key=lambda x: x[1], reverse=True)

    #pull out top 10 from list
    id_results = sorted_list[:10]

    page_results = []
    for id_tuple in id_results:
        id = id_tuple[0]
        page = dict_ids_titles[id]
        page_results.append(page)

    return page_results


if __name__ == "__main__":
    ''' Takes in a query (String) and searches the files for the top 10 documents as results to the search
    
    Parameters:
    pageRank -- an optional input specifying if pagerank should be used ("--pagerank")
    titleIndex -- the document path that titles are written in 
    documentIndex --  the document path that documents are written in 
    wordIndex -- the document path that words are written in 
    
    Returns: 
    The top 10 most relevant documents to the query (based on term relevance and PageRank (if specified))
    '''
    

    # Parse in arguments for the index files and an optional argument that says to use PageRank
    if len(sys.argv) == 4:
        titleIndex = sys.argv[1] # the name of the script (e.g. "index.py")... can usually ignore
        documentIndex = sys.argv[2] # the first argument
        wordIndex = sys.argv[3] # the second argument
    
    elif len(sys.argv) == 5:
        pageRankCondition = sys.argv[1]
        titleIndex = sys.argv[2] 
        documentIndex = sys.argv[3]
        wordIndex = sys.argv[4]

        if pageRankCondition != "--pagerank":
            raise Exception("Illegal argument passed in!")
    
    else:
        raise Exception("Illegal number of arguments passed in!")
    
    #Run indexer before starting REPL

    # find relevancy score of every term of the query in each document/page (words file has doc relevance)
    words_to_doc_relevance = dict()
    read_words_file(wordIndex, words_to_doc_relevance)

    dict_ids_titles = dict()
    read_title_file(titleIndex, dict_ids_titles)

    condition = False
    pagerank_dict = dict()
    if len(sys.argv) == 5:
        if pageRankCondition == "--pagerank":
            read_docs_file(documentIndex, pagerank_dict)
            condition = True

    # Run REPL that takes in and processes search queries
    query = input("enter query >> ")
    while query != ":quit":
        original_query = query

        regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        nltk_test = PorterStemmer()
        query = re.findall(regex, query) 
        query = [nltk_test.stem(word.lower()) for word in query]   

        page_results = get_results(query, condition, words_to_doc_relevance, pagerank_dict, dict_ids_titles)
    
        if page_results == []:
            print("Sorry no results were found for", original_query)
        else:
            for i in range (0, len(page_results), 1):
                print(i + 1, page_results[i])

        print("\n")
        query = input("enter query >> ")