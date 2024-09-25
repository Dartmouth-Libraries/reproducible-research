import re
import pandas as pd
# import pybliometrics
import time
from pybliometrics.scopus import AuthorSearch, AuthorRetrieval, AbstractRetrieval


def modify_affils(text: str):
    """
    Reads in an affiliation string taken from the scopus API's 
    "Affiliation" field
    Modifies that string by:
    1. removing unicode symbols?
    2. expanding "U." to "University"
    3. removing parenthetical information
    4. stripping leading and trailing whitespace
    Then returns the modified string
    """

    oldtext = text
    text = re.sub(r'[^\x00-\x7F]+',' ', text)
    text = re.sub(r'(?<!\w)U\.(?!\w)', 'University', text)
    text = re.sub(r'\(.*\)', '', text)
    text = text.strip()
    # text = re.sub(r"^\W", "", text)
    # text = re.sub(r"\W*$", "", text)

    if text != oldtext:
        print(f"modify affils from {oldtext} to {text}")
        
    return (text)


def get_author_eids(lastname: str, firstname: str, affil_list: list):
    """
    Searches Scopus API (using pybliometrics) using lastname, firstname, and affiliation list
    returns list of researcher eids and affiliation ids
    """

    print("searching for: ", lastname, firstname, affil_list)
    eidlist = []
    affidlist = []
    for aff in affil_list:
        aff = modify_affils(aff)
        au = AuthorSearch(f"AUTHLAST({lastname}) and AUTHFIRST({firstname}) and AFFIL({aff})")
        print(au.get_results_size())

        if au.get_results_size() == 0:
            eidlist.append(0)
            affidlist.append(0)
            continue
        for author in au.authors:
            eidlist.append(author.eid)
            affidlist.append(author.affiliation_id)

    print("eids:", eidlist)
    print("affids:", affidlist)

    return ([eidlist, affidlist])


def get_scopus_authorinfo(eid: int|str, coldict: dict):
    """
    Reads in a Scopus eid for an author
    and a dictionary of columns (key = new column name, value = matching scopus field)

    Returns columns (specified in coldict) with info
    retrieved using Scopus AuthorRetrieval function
    """

    time.sleep(0.4)
    infolist = []
    if type(eid) is int:
        eid = str(eid)
    try:
        au = AuthorRetrieval(eid)
    except IOError as e:
        print("I/O error(): {}".format(e))
    except Exception as e:
        print('An exception occurred: {}'.format(e))
        return ([""] * len(coldict.keys()))
    for v in list(coldict.values()):
        try:
            infolist.append(getattr(au, v))
        except (AttributeError, KeyError):
            infolist.append("")
        except IOError as e:
            print("I/O error(): {}".format(e))
        except ValueError:
            print("ValueError")
        except Exception as e:
            print('An exception occurred: {}'.format(e))
            infolist.append("")
    # infolist = [getattr(au, v) for v in list(coldict.values())]
    return (infolist)


def create_docdfs(author_eid):
    """
    Reads in an author eid
    retrieves document info for this author
    using pybliometrics' AuthorRetrieval and its
    get_documents() method

    Returns a dataframe
    """
    au = AuthorRetrieval(author_eid)
    docs = pd.DataFrame(au.get_documents())
    docs['search_author_eid'] = author_eid
    return (docs)


def getdocs_multauthors(eidcol: pd.Series, namecol: pd.Series):
    """
    reads in a dataframe column (pd.Series) of author eids
    returns
    + dfs with doc info for each indiv author
    + one df with all docs from all authors
    """

    # eidlist = authorids_df['identifier'].to_list()
    eidlist = eidcol.to_list()
    namelist = namecol.to_list()
    all_df = pd.DataFrame
    for i, eid in enumerate(eidlist):
        print("eid:", eid)
        try:
            df = create_docdfs(eid)
        except PermissionError:
            print(f"missing eid ({eid}) for {i}. {name}")
            with open(f"data/docs_by_author/docs_{name}_{eid}_missing.csv", 
                      'w', encoding='utf-8') as f:
                f.write("")
            continue
        name = namelist[i]
        print(name)
        if name is not None:
            name = re.sub(r"\W", "", name)
        print(name)
        df.to_csv(f"data/docs_by_author/docs_{name}_{eid}.csv", 
                  encoding='utf-8')
        if i > 0:
            all_df = pd.concat([all_df, df], ignore_index=True)
            print(all_df.shape)
        else:
            all_df = df.copy()
            print("0:", all_df.shape)
    return (all_df)


"""
def get_scopus_abstractinfo(eid: int|str):

    if type(eid) is int:
        eid = str(eid)
    ab = AbstractRetrieval(eid)
    #subjareas = [sa.code for sa in au.subject_areas] 
    abdict = {}
    abdict['doc_eid'] = eid
    abdict['author_eids'] = [au.auid for au in ab.authors]
    abdict['date'] = ab.coverDate
    abdict['publName'] = ab.publicationName
    abdict['doi'] = ab.doi
    abdict['cited_by_ct'] = ab.citedby_count
    abdict["subj_areas"] = ab.subject_areas
    abdict['idxterms'] = ab.idxterms
    return abdict
"""


def get_scopus_abstractinfo(eid: int | str, coldict: dict):
    """
    Reads in a Scopus eid for a document
    #and a dictionary of columns (key = new column name, value = matching scopus field)

    Returns columns (specified in coldict) with info
    retrieved using Scopus AuthorRetrieval function
    """

    # time.sleep(0.4)
    # infolist = []
    infodict = {}
    if type(eid) is int:
        eid = str(eid)
    try:
        ab = AbstractRetrieval(eid)
    except IOError as e:
        print("I/O error(): {}".format(e))
    except Exception as e:
        print('An exception occurred: {}'.format(e))
        return ([""] * len(coldict.keys()))
    # for v in list(coldict.values()):
    for k, v in coldict.items():
        try:
            infodict[k] = getattr(ab, v)
            # infolist.append(getattr(ab, v))
        except (AttributeError, KeyError):
            infodict[k] = ""
            # infolist.append("")
        except IOError as e:
            print("I/O error(): {}".format(e))
        except ValueError:
            print("ValueError")
        except Exception as e:
            print('An exception occurred: {}'.format(e))
            infodict[k] = ""
            # infolist.append("")
    # infolist = [getattr(ab, v) for v in list(coldict.values())]
    return infodict
