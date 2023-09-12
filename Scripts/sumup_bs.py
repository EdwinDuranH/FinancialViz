import pandas as pd
import numpy as np

#Function that recursively sums up the childrens of accounts to replace them with the value of the aggregated account
"""It identifies children for an account and then identifies its descendants recursively. This function 
incorporates the logic from the original 'sumup' framework but applies it to the extensive data structure 
of the SCVS. Instead of summing individual accounts for a single company, it performs this operation for 
all the rows in each of the accounts' columns"""

def sumup_bs(df,acct):
    acct = f"CUENTA_{acct}"
    cols = df.columns
    #List of Immediate Children
    children = [i for i in cols if (i.startswith(acct)) & (len(i) == len(acct)+2)]

    #Check for presence of children
    if not bool(children):
        return df[acct]
    else:
        #Aggregate children for all companies
        sum_children = np.zeros(len(df))
        for child in children:
            sum_children += sumup(df,child.replace("CUENTA_",""))

        #If it's the equity account, sum account 31, which was registered in pair numbers of digits for an unknown reason
        if acct == "3":
            sum_children += df["CUENTA_31"]
        #Update the parent's value with the sum of children
        df[acct] = sum_children
        return sum_children