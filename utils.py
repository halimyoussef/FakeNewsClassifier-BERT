import wikipedia as wiki

def get_clean_page_name(page_name: str) -> str:
    """
    Clean the page name by replacing -LRB- and -RRB- with ( and ) respectively.
    Also replace _ with space.

    Args:
        page_name: A string containing the page name.
    Returns: 
        A string containing the cleaned page name.
    """

    if "-LRB-" in page_name:
        page_name = page_name.replace("-LRB-", "(")
    if "-RRB-" in page_name:
        page_name = page_name.replace("-RRB-", ")")

    page_name = page_name.replace("_", " ")

    return page_name



def get_wikipedia_data(page_name: str) -> str:
    """
    Get the original docuement (wikipedia page) for the given page name.

    Args:
        page_name: A string containing the page name from the FEVER dataset.
    Returns: 
        A string containing the wikipedia page data.
    """
    try:
        page = get_clean_page_name(page_name=page_name)
        print(">>> Getting data for: " + page + " (Original name: " + page_name + ")")
        data = wiki.page(page).content
        return data
    except:
        return ""



def get_one_ETS(data: str, sentence_id: int) -> str:
    """
    Get the ETS from the wikipedia page data for the given sentence id.

    Args:
        data: A string containing the wikipedia page data.
        sentence_id: An integer containing the sentence id from the FEVER dataset.
    Returns: 
        A string containing the ETS
    """
    tab_data = data.split(".")
    return tab_data[sentence_id]



def get_all_ETS_and_document(evidence: list):
    """
    Get the ETS and the document of the wikipedia page for the given evidence.

    Args:
        evidence: A list containing the evidence for one instance of the FEVER dataset.
    Returns:
        a tuple containing the ETS and the document from the wikipedia page --> ETS and Original Document
    """
    ets = ""; document = ""; first_title = ""
    
    for e in evidence: # only first 2
        print(">>> Starting process for: " + str(e[0]))
        title= e[0][2]
        if title != first_title:
            data = get_wikipedia_data(title)

            if len(data) == 0:
                raise Exception(">>> Error: Wiki page not found.")
            
            document += data
            print(">>> Getting ETS for: " + title)
            ets += get_one_ETS(data, e[3])
            
            first_title = title
        else:
            print(">>> Already got data for: " + title)
            print(">>> Getting ETS for: " + title)
            ets += ". " + get_one_ETS(data, e[3])

    return ets, document
