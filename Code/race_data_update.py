#==================================================#
#                   OVERVIEW                       #
#==================================================#
#==================================================#
#                   IMPORTS                        #
#==================================================#
# Builtin
import sys
# Additional
import requests
from bs4 import BeautifulSoup
import pandas as pd
# Also requires the following to be installed (via pip):
#  * lxml
#  * html5lib

#==================================================#
#                    GLOBAL                        #
#==================================================#


#==================================================#
#                     CODE                         #
#==================================================#

def scrippity_scrape(year_start=None, year_end=None):
    """
    INPUT: N/A
    OUTPUT: N/A
    RETURN: DataFrame
    """

    # Perform Argument Checks


    # Scrape data
    url = f"http://racingaustralia.horse/arb/Group_ListedRaceDates/{year_start}-{year_end}.aspx"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features="lxml")

    ## Get the table
    df = pd.read_html(str(soup.findAll("table", {"class": "tableizer-table"})[0]))[0]

    return df




def load_current():
    """
    INPUT: N/A
    OUTPUT: CSV
        * ../Data/races.csv
    RETURN: N/A
    """
    pass


def main():
    # NOTE: The site does not have data before 2009-2010.
    year_range = [
        [2009,2010],
        [2010,2011],
        [2011,2012],
        [2012,2013],
        [2013,2014],
        [2014,2015],
        [2015,2016],
        [2016,2017],
        [2017,2018],
        [2018,2019]
    ]


    agg_list = []
    for year in year_range:
        print(f"Running search for: {year}")
        df = scrippity_scrape(year_start=year[0], year_end=year[1])

        # For some reason, pd.to_html() will use numbers as the column names (like an index, 0,1,2,3)
        # This only occurs on years < 2017 (i.e. the latest year set is 2015-2016. 2016-2017 is fine.)
        # These lines replace the column names with the first row (which is the actual column names), then drops the first row
        if year[1] < 2017:
            df.columns = df.iloc[0]                  # Fix the above mentioned issue
            df = df.reindex(df.index.drop(0))        # Fix the above mentioned issue
        df = df.dropna(axis=1, how='all')        # Drop any empty columns
        agg_list.append(df)

    df = pd.concat(agg_list, sort=True)
    # Convert to datetime
    df['MeetDate'] = pd.to_datetime(df["MeetDate"], errors="coerce")
    # Sort needs to come before fillna, because can't sort with mixed column values
    df.sort_values('MeetDate', ascending=False, inplace=True)
    ## Fill in NANs
    #df['MeetDate'].fillna("TBA", inplace=True)

    df.to_csv("../Data/races.csv", index=False)


if __name__ == "__main__":
    main()