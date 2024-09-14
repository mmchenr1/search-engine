# Search Engine
developers: Molly McHenry and Allie Masthay


## Instructions for use:
<ol>
<li>Run the indexer on a wiki file to be searched.</li>
<li>tart up the querier by running:

```python3 query.py [--pagerank] <titleIndex> <documentIndex> <wordIndex>```
</li>
<li>After the querier starts, you will be prompted to enter a query. Enter a search term or search terms and the querier will return the top 10 page results to match your query.</li>
<li>Continue to enter queries, and exit the querier by entering

```:quit```.
</li>
</ol>


## How the pieces fit together:
The indexer parses in the wiki file to be searched and writes information that will later be used during queries into three different txt files: a titles file, a documents file, and a words file. When the querier is run, it will read from these files to quickly get the results for a query.

## Testing
### Testing the Indexer
#### Parsing Tests
We tested our parsing function by parsing in various wiki files and running unit tests on the indexer's handling of those files. Edges cases we covered included:
<ol>
    <li>empty wiki file</li>
    <li>duplicate words in one file</li>
    <li>a page completely comprised of stop words</li>
    <li>words that were different on the page, but identical after stemming</li>
    <li>stop word as the title of a page ("A")</li>
    <li>special characters within a word </li>
    <li>words with only special characters</li>
    <li>having a pipe link in the title of a page</li>
    <li>pages that link to itself</li>
    <li>correct processing of piped links into links dictionary and corpus dictionary</li>
    <li>wikis with multiple pages</li>
    <li>wiki with one page</li>
    <li>duplicate links on the same page with case insensitivity</li>
    <li>links to pages not in the wikifile</li>
    <li>page with empty text</li>
    <li>page with empty title</li>
    <li>wikifile with no links in any pages</li>
</ol>
    
#### Relevancy Algorithm Tests
We also tested our Relevancy Algorithm by calculating and testing the relevancy scores of our wiki files. Edge cases we covered included:
<ol>
<li>empty wiki</li>
<li>words that appear in multiple pages</li>
</li>duplicate words within the same page</li>
<li>page with only a link</li>
<li>page with duplicate links</li>
<li>page with category link almost identicaly to other duplicate links</li>
<li>special character strings as words</li>
<li>pipe link inside of a page title</li>
<li>only one paged wiki</li>
</ol>

#### PageRank Algorithm Tests
We tested our PageRank Algorithm using our ```emptywiki.xml``` and four populated wikis. Becuase all of our assertions passed on the handout pagerank examples, all necesasry edge cases for the pagerank algorithm were covered.

#### Indexer Function Tests
We tested our Indexer function by indexing the wiki files and then using the read functions in file_io.py to check that the files were written to correctly during indexing. Becuase we thoroughly tested all of the helper functions used for the computations in the indexer, all edge cases were already tested in the tests written for those functions.

### Testing the Querier:
The querier runs as a main method, so we moved the portion of the function evaluating the query term and retrieving the page results of a search to a helper function which we could then test (`get_results`). In addition to testing wheats, where we also verified that the pagerank v. no-pagerank query conditions produced distinct and correct results. Other edge cases included:
<ol>
<li>searched term not in corpus</li>
<li>query with only special characters</li>
<li>query with attached special characters</li>
<li>empty query</li>
<li>multi-word query</li>
<li>multi-word query, with a word not in corpus</li>
<li>running a query on empty files/dictionaries</li>
</ol>

### System Tests/Usage Examples:
Here are a few example of how the search engine works, exhibiting how the inclusion of the PageRank algorithm affects search results. For each of the examples, the indexer was run on ```MedWiki.xml```.

#### with pagerank
<ol>
<li>query: "baseball"<br>
results: 

```
    1 Oakland Athletics
    2 February 2
    3 Kenesaw Mountain Landis
    4 Netherlands
    5 Miami Marlins
    6 Ohio
    7 Minor league baseball
    8 Fantasy sport
    9 Kansas
    10 Pennsylvania
```
</li>
    
<li>query: "United States"
results:

```
    1 Netherlands
    2 Ohio
    3 Illinois
    4 Michigan
    5 Pakistan
    6 International Criminal Court
    7 Franklin D. Roosevelt
    8 Pennsylvania
    9 Norway
    10 Louisiana
```
</li>
</ol>

#### without pagerank

<ol>
<li>query: "baseball"

results: 

```
    1 Oakland Athletics
    2 Minor league baseball
    3 Kenesaw Mountain Landis
    4 Fantasy sport
    5 Miami Marlins
    6 October 30
    7 January 7
    8 Hub
    9 May 14
    10 November 7
```
</li>

<li>query: "United States"

results:

```
    1 Federated States of Micronesia
    2 Imperial units
    3 Joule
    4 Knowledge Aided Retrieval in Activity Context
    5 Imperialism in Asia
    6 Elbridge Gerry
    7 Martin Van Buren
    8 Pennsylvania
    9 Finite-state machine
    10 Metastability
```
</li>
</ol>