import pandas as pd
import re
from pathlib import Path

wos_groups = pd.read_csv(Path("../data/JCR_CategoriesResults_groups.csv"), encoding = 'utf-8', index_col=[0])
wos_groups["Category"] = wos_groups["Category"].str.lower()
wos_groups = wos_groups.rename(columns={"# of journals": "journal_ct", "Citable Items": "citableitems_ct", "Total Citations": "totalcits_ct"})
wos_groups_sub = wos_groups.loc[:, ["Category", "Group"]]

groupsums = pd.read_csv("../data/wos_group_counts_Apr2024.csv", encoding="utf-8")


# strip leading / trailing punctuation
def strip_outer_punct(txt: str):
    newtxt = re.sub(r"^[\W\s]*(.*?)[\W\s]*$", r"\1", txt)
    return newtxt


def wos_add_and_explode_groups(df: pd.DataFrame):
    """
    Reads in a WoS dataframe (created from a csv file with
        two-letter abbreviations like "PT" and "AU")
    returns a dataframe exploded by both WoS categories ("WC") 
        and groups (imported and matched with categ's separately)
    """
    print(f"original dataset has {df.shape[0]} rows and {df.shape[1]} columns")

    # Clean df and explode by "WC" categories
    df.loc[:, "WC"] = df.loc[:, "WC"].fillna("")    
    df['wos_categs'] = df['WC'].str.split(';')
    df_wc_explode = df.explode("wos_categs")
    df_wc_explode['wos_categs'] = df_wc_explode['wos_categs']\
        .apply(strip_outer_punct)
    df_wc_explode["wos_categs"] = df_wc_explode["wos_categs"].fillna("")
    df_wc_explode["wos_categs"] = df_wc_explode["wos_categs"].str.lower()
    print(f"exploding by wos_categ (WC) produces a df with {df_wc_explode.shape[0]} rows and {df_wc_explode.shape[1]} columns")

    # add in WoS group data
    df2 = pd.merge(df_wc_explode, wos_groups_sub, how="inner", 
                   left_on="wos_categs", right_on="Category")

    # explode by groups
    df2["Group"] = df2["Group"].fillna("")
    df2["Group"] = df2["Group"].str.split(";")
    df2["Group"] = df2["Group"].apply(lambda x: [item.strip() for item in x])
    df2_explode = df2.explode("Group")

    # need to remove duplicate group categories 
    df2_explode = df2_explode.drop_duplicates(subset=["UT", "Group"])

    print(f"after adding in WoS groups and also exploding by groups, the resulting df has {df2_explode.shape[0]} rows and {df2_explode.shape[1]} columns")
    return df2_explode


def wos_groupby_Groups(df: pd.DataFrame):
    """
    Reads in a wos df exploded by groups using wos_add_and_explode_groups

    Returns df grouped by WoS groups
    """
    group_counts = df.groupby("Group").size()
    group_counts = group_counts.sort_values(ascending=False)
    group_counts2 = pd.merge(group_counts.rename("group_ct"),
                             groupsums, left_index=True, right_on="Group")
    group_counts2["numitems_insample_per100kinWOS"] = group_counts2["group_ct"] / group_counts2["citableitem_ct"] * 100000
    group_counts2 = group_counts2.sort_values(
        by="numitems_insample_per100kinWOS", ascending=False)

    return group_counts2


def wos_groupby_Yr_Groups(df: pd.DataFrame):
    """
    Reads in a wos df exploded by groups using wos_add_and_explode_groups

    Returns df grouped by WoS groups and publication year
    """
