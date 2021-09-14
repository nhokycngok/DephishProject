import pandas as pd
import glob

f = []
# for file in glob.glob("url_information\*.json"):
for file in glob.glob("D:\\Code\\dephish\\front-end\\db\\whitelist\\tinnhiemmang-json\\*.json"):
    f.append(file)
# print(f)
list_df = []
c=0
for i in f:
    # print(c)
    df = pd.read_json(i)
    list_df.append(df)
    c+=1
all_df = pd.concat(list_df)
# print(all_df)
all_df.to_csv("D:\\Code\\dephish\\front-end\\db\\whitelist\\tinnhiemmang.csv", index=False)


# result = pd.read_csv("jsonfile//csvfile//new.csv")
# print(result)