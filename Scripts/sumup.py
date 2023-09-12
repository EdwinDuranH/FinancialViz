import pandas as pd
#Function that recursively sums up the childrens of accounts to replace them with the value of the aggregated account
"""It identifies children for an account, and then it identifies the children of the children, recursively, 
until there are no more children, at which point it sums up all of the children to replace this sum with the value of 
the aggregate account"""

def sumup(df,acct):
    acct = str(acct)
    #Children dframe
    children = df[(df["CÓDIGO"].str.startswith(acct)) & (df["CÓDIGO"].str.len() == len(acct)+2)]
    #Check for presence of children
    if children.empty:
        return df[df["CÓDIGO"] == acct]["VALOR (En USD$)"].values[0]
    else:
        sum_children = 0
        for index,child in children.iterrows():
            sum_children += sumup(df,child["CÓDIGO"])

        #If it's the equity account, sum account 31, which was registered in pair numbers of digits for an unknown reason
        if acct == "3":
            sum_children += df[df["CÓDIGO"] == "31"]["VALOR (En USD$)"].values[0]
        #Update the parent's value with the sum of children
        df.loc[df["CÓDIGO"] == acct,"VALOR (En USD$)"] = sum_children
        return round(sum_children,2)
