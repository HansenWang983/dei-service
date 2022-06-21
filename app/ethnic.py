import pandas as pd
from ethnicolr import census_ln, pred_wiki_name

races_census = ["White","Black","Asian","Other", "Other", "Hispanic/Latino"]
races_wiki = {
    "Asian,GreaterEastAsian,EastAsian": "Asian",
    "Asian,GreaterEastAsian,Japanese": "Asian",
    "Asian,IndianSubContinent": "Asian",
    "GreaterAfrican,Africans": "Black",
    "GreaterAfrican,Muslim": "Other",
    "GreaterEuropean,British": "White",
    "GreaterEuropean,EastEuropean": "White",
    "GreaterEuropean,Jewish": "White",
    "GreaterEuropean,WestEuropean,French": "White",
    "GreaterEuropean,WestEuropean,Germanic": "White",
    "GreaterEuropean,WestEuropean,Hispanic": "Hispanic/Latino",
    "GreaterEuropean,WestEuropean,Italian": "White",
    "GreaterEuropean,WestEuropean,Nordic": "White",
}
races_wiki_index = { # the index of mean value of each race in result dataframe from pred_wiki_name model 
    "Asian,GreaterEastAsian,EastAsian": 4,
    "Asian,GreaterEastAsian,Japanese": 8,
    "Asian,IndianSubContinent": 12,
    "GreaterAfrican,Africans": 16,
    "GreaterAfrican,Muslim": 20,
    "GreaterEuropean,British": 24,
    "GreaterEuropean,EastEuropean": 28,
    "GreaterEuropean,Jewish": 32,
    "GreaterEuropean,WestEuropean,French": 36,
    "GreaterEuropean,WestEuropean,Germanic": 40,
    "GreaterEuropean,WestEuropean,Hispanic": 44,
    "GreaterEuropean,WestEuropean,Italian": 48,
    "GreaterEuropean,WestEuropean,Nordic": 52,
}

def infer_from_batch_input(names):
    results = []
    c_infer_max_prob_arr = []
    c_infer_race_arr = []

    # inference from census_ln
    c_last_names = []
    for name in names:
        c_last_names.append({"name": name["last_name"]})
    
    df = pd.DataFrame(c_last_names)
    cdf = census_ln(df, 'name', 2010)
    cnp = cdf.to_numpy()

    for c in cnp:
        c_infer_max_prob = 0.0
        c_infer_race = ""
        for i in range(1,7):
            try:
                prob = float(c[i])
            except:
                continue
            if c_infer_max_prob < prob:
                c_infer_max_prob = prob
                c_infer_race = races_census[i-1]

        c_infer_max_prob_arr.append(c_infer_max_prob)
        c_infer_race_arr.append(c_infer_race)

    # inference from pred_wiki_name  
    w_names = []
    for name in names:
        w_names.append({"first": name["first_name"], "last":name["last_name"]})
    
    df = pd.DataFrame(w_names)
    wdf = pred_wiki_name(df, 'last', 'first')
    wnp = wdf.to_numpy()

    i = 0
    for w in wnp:
        w_infer_race = races_wiki[w[-1]]
        w_infer_max_prob = 0.0  
        result = {}
        result["first_name"] = w[0]
        result["last_name"] = w[1]
        result["estimated_ethnicity"] = c_infer_race_arr[i]
        result["estimated_ethnicity_prob"] = c_infer_max_prob_arr[i]
        result["estimated_gender"] = ""
        
        if w_infer_race != c_infer_race_arr[i]:
            index = races_wiki_index[w[-1]]
            try:
                w_prob = float(w[index])
            except:
                results.append(result)
                i += 1
                continue
                
            w_infer_max_prob = w_prob * 100
            if w_infer_max_prob > c_infer_max_prob_arr[i]: # choose one with higher probability
                result["estimated_ethnicity"] = w_infer_race
                result["estimated_ethnicity_prob"] = w_infer_max_prob
        
        results.append(result)
        i += 1
    
    return results