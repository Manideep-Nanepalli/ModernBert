import preprocessor as p 
import re
import wordninja
import csv
import pandas as pd


# Data Cleaning seniors code
# def data_clean(strings, norm_dict):
#     # Manually remove URLs
#     clean_data = re.sub(r'http\S+', '', strings)
#     # Remove emojis (you can add more Unicode ranges for more emoji types)
#     clean_data = re.sub(r'[😀-🙏]', '', clean_data)
#     # Remove special reserved words or unwanted symbols if needed
#     clean_data = re.findall(r"[A-Za-z#@]+|[,.!?&/\\<>=$]|[0-9]+", clean_data)
    
#     clean_data = [[x.lower()] for x in clean_data]

#     # Normalize words if in norm_dict
#     for i in range(len(clean_data)):
#         if clean_data[i][0] in norm_dict:
#             clean_data[i] = norm_dict[clean_data[i][0]].split()

#     return clean_data



def load_data(filename):

    concat_text = pd.DataFrame()
    raw_text = pd.read_csv(filename,usecols=[0], encoding='ISO-8859-1')
    raw_target = pd.read_csv(filename,usecols=[1], encoding='ISO-8859-1')
    raw_label = pd.read_csv(filename,usecols=[2], encoding='ISO-8859-1')
    seen = pd.read_csv(filename,usecols=[3], encoding='ISO-8859-1')
    label = pd.DataFrame.replace(raw_label,['AGAINST','FAVOR','NONE'], [0,1,2])
    concat_text = pd.concat([raw_text, label, raw_target, seen], axis=1)
    concat_text.rename(columns={'Stance 1':'Stance','Target 1':'Target'}, inplace=True)
    if 'train' not in filename:
        concat_text = concat_text[concat_text['seen?'] != 1] # remove few-shot labels
    
    return concat_text









from contractions import fix

def data_clean(strings, norm_dict):
    
    p.set_options(p.OPT.URL,p.OPT.EMOJI,p.OPT.RESERVED)
    clean_data = p.clean(strings) # using lib to clean URL,hashtags...
    clean_data = re.sub(r"#SemST", "", clean_data)
    
    # clean_data = re.findall(r"[A-Za-z#@]+|[,.!?&/\<>=$]|[0-9]+",clean_data)
    clean_data = clean_data.split()
    # print(clean_data)
    clean_data = [fix(token) for token in clean_data]
    clean_data = " ".join(clean_data)
    clean_data = re.findall(r"[A-Za-z0-9#@]+[,.]?|[,.!?&/\<>=$]", clean_data)
    # print(clean_data)
    clean_data = [[x.lower()] for x in clean_data]

    
    
    for i in range(len(clean_data)):
        temp = clean_data[i][0].strip("#")
        temp = temp.strip("@")

        if temp in norm_dict.keys():
            clean_data[i] = norm_dict[temp].split()
            continue
        if clean_data[i][0].startswith("#") or clean_data[i][0].startswith("@"):
            clean_data[i] = wordninja.split(clean_data[i][0]) # separate hashtags
    clean_data = [j for i in clean_data for j in i]
    clean_data = [i.lower() for i in clean_data]
    # print(clean_data)


    return clean_data

# # Clean All Data
def clean_all(filename, norm_dict):
    
    concat_text = load_data(filename) # load all data as DataFrame type
    raw_data = concat_text['Tweet'].values.tolist() # convert DataFrame to list ['string','string',...]
    label = concat_text['Stance'].values.tolist()
    x_target = concat_text['Target'].values.tolist()
    clean_data = [None for _ in range(len(raw_data))]
    
    for i in range(len(raw_data)):
        clean_data[i] = data_clean(raw_data[i],norm_dict) # clean each tweet text [['word1','word2'],[...],...]
        x_target[i] = data_clean(x_target[i],norm_dict)
    avg_ls = sum([len(x) for x in clean_data])/len(clean_data)
    
    print("average length: ", avg_ls)
    print("num of subset: ", len(label))

    return clean_data,label,x_target



