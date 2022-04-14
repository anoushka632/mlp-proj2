
#%%
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split

#%%
d = pd.read_csv("../hotel.csv")
df = d.copy()

df["date"] = pd.to_datetime(df.arrival_date_day_of_month.astype(str) + "-"  + df.arrival_date_month + "-" + df.arrival_date_year.astype(str))
df.index = df["date"]

#%%
df = df.drop(["country", "date"], axis = 1)
df.children = df["children"].fillna(0)
missing_cols = ["company", "agent"]
for i in missing_cols:
    df[i] = df[i].astype('str') ##Change to object for categorical classification
    df[i] = df[i].fillna("Not Used") ##Fill "NA" with new variable

##create new variable for agent used and company used
binary_cols = ["company_used", "agent_used"]
for i in range(len(binary_cols)):
    df[binary_cols[i]] = np.where(df[missing_cols[i]]!= 'Not Used', 1, 0)

df = df.drop_duplicates(keep = 'first')

df["group_type"] = np.where((df["children"] == 0) & (df["babies"] == 0) & (df["adults"] > 1), "Adult_Group",
                   np.where(((df["children"] > 0) | (df["babies"] > 0)) & (df["adults"] > 0), "Family",
                   np.where((df["children"]) == 0 & (df["babies"] == 0) & (df["adults"] == 1), "Single_User",
                   np.where(df["adults"] == 0, "Zero Adults", "Not Valid"))))

df.reset_index(inplace=True, drop = True)

ohe_col = df.select_dtypes(exclude = np.number).columns
ohe = OneHotEncoder(sparse = False)
dohe = ohe.fit_transform(df[ohe_col])
dohe = pd.DataFrame(dohe)
dohe.columns = ohe.get_feature_names_out()
df = pd.concat([df,dohe], axis = 1).drop(ohe_col, axis = 1)
X = df.drop("is_canceled", axis = 1)
y = df["is_canceled"]

X = X.reset_index(drop = True)

df.to_csv("full_dat.csv")
#df.iloc[0:42675,].to_csv("full_dat_part1.csv")
#df.iloc[42675:,].to_csv("full_dat_part2.csv")

#%%
# %%
