import pubchempy as pcp
import pandas as pd 
import ast
import requests
import json 


DESC = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/"

def get_description(cid):
    url = DESC+str(cid)+"/description/JSON"
    r = requests.get(url)
    json_data = json.loads(r.text)
    data = dict(json_data)

    desc = data["InformationList"]["Information"][1]["Description"]
    desc_source = data["InformationList"]["Information"][1]["DescriptionSourceName"]
    desc_url = data["InformationList"]["Information"][1]["DescriptionURL"]
    print(desc, desc_source, desc_url)
    return desc, desc_source, desc_url


def get_cid(x):
    c = pcp.get_compounds(x.strip(),'name')
    print(c)
    return c

def clean(x):
    return [i.replace("Compound(","").replace(")","") for i in x]



df = pd.read_excel("input.xlsx")

df["PubChem_url"] = df["Name"].apply(get_cid)

df["PubChem_url"] = df["PubChem_url"].apply(clean)

df = df.explode("PubChem_url")

df[["description","desc_source","description_url"]] = df.apply(lambda x:get_description(x["PubChem_url"]) , axis=1, result_type='expand' )


df.to_excel("FINAL_OUTPUT.xlsx")


