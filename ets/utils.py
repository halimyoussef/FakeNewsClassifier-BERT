import wikipedia as wiki
import pandas as pd

def get_clean_page_name(page_name: str) -> str:
    """
    Clean the page name by replacing -LRB- and -RRB- with ( and ) respectively.
    Also replace _ with space.

    Parameters:
        - page_name (str): A string containing the page name.
    
    Returns: 
        - str: the cleaned page name.
    """

    if "-LRB-" in page_name:
        page_name = page_name.replace("-LRB-", "(")
    if "-RRB-" in page_name:
        page_name = page_name.replace("-RRB-", ")")

    page_name = page_name.replace("_", " ")

    return page_name



def get_wikipedia_data(page_name: str, articles: pd.DataFrame) -> str:
    """
    Get the original docuement (wikipedia page) for the given page name.

    Parameters:
        - page_name (str): A string containing the page name from the FEVER dataset.
    
    Returns: 
        - str: the wikipedia page data.
    """
    
    try:
        page = get_clean_page_name(page_name=page_name)

        if page in articles.page.values:
            #print(">>> Already got data for: " + page)
            return articles[articles.page == page].data.values[0]
        else:
            #print(">>> Getting data for: " + page + " (Original name: " + page_name + ")")
            data = wiki.page(page).content
            #print('>>> TEST for data length: ' + str(len(data)) + ' characters')
            #print('>>> Saving data for: ' + page)
            articles.loc[len(articles)] = {'page': page, 'data': data}
            return data
    except Exception as e:
        #print(e)
        return "Error: Wiki page not found (get_wikipedia_data)"



def get_one_ETS(data: str, sentence_id: int) -> str:
    """
    Get the ETS from the wikipedia page data for the given sentence id.

    Parameters:
        - data (str): the wikipedia page data.
        - sentence_id (int): sentence id from the FEVER dataset.

    Returns: 
        - str : one ETS
    """
    tab_data = data.split(".")
    return tab_data[sentence_id]



def get_all_ETS_and_document(evidence: list, articles: pd.DataFrame):
    """
    Get the ETS and the document of the wikipedia page for the given evidence.

    Parameters:
        - evidence (list): all evidence for one instance of the FEVER dataset.
        - articles (pd.DataFrame): dataframe containing all the wikipedia pages data.
        
    Returns:
        - tuple:  ETS (Evidence Text Sentence) and the original document from the Wikipedia page 
    """
    ets = ""; document = ""; first_title = ""
    
    
    for e in evidence[:2]: # only first 2 ETS
        #print(">>> ================================")
        #print(">>> Starting process for: " + str(e[0]))
        title= e[0][2]
        if title != first_title:
            data = get_wikipedia_data(title, articles)

            if len(data) == 0:
                raise Exception(">>> Error: Wiki page not found.")
            
            document += data
            #print(">>> Getting ETS for: " + title + " , sentence id: " + str(e[0][3]))
            ets += get_one_ETS(data, e[0][3]) #ISSUE
            first_title = title
        else:
            #print(">>> Already got data for: " + title)
            #print(">>> Getting ETS for: " + title)
            ets += ". " + get_one_ETS(data, e[0][3])

    return ets, document