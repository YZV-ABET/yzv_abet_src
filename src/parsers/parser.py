

def parse_courses():
    import numpy as np
    import pandas as pd
    import gspread
    from google.colab import auth
    auth.authenticate_user()

    import gspread
    from oauth2client.client import GoogleCredentials
    
    gc = gspread.authorize(GoogleCredentials.get_application_default())
    sht1 = gc.open_by_key('1T4agbXrPsCXcSwvjtnEw90IFcmR4Ut6N7M8fTZC4Hq4')
    ws1 = sht1.get_worksheet(0)
    rec = np.array(ws1.get_all_values())
    id1 = np.array(rec[2])[:26]
    id2 = np.array(rec[3])[:26]
    for i, s in enumerate(id1):
        if id1[i] != "":
            id1[i] = s
        else:
            id1[i] = id1[i-1]
    arrays = [id1, id2]
    midx = pd.MultiIndex.from_arrays(arrays, names=('category', 'subcategory'))
    df1 = pd.DataFrame(rec[5:52, :26].T, index=midx)
    df1, df1.columns = df1.loc[df1.index.values[1:]], df1.loc[df1.index.values[0]]
    df1.sort_index(inplace=True)
    df2 = df1[~(df1 == "")].dropna(axis=1)
    df3 = df1.drop(df2.columns, axis=1)
    df1, df2, df3 = df1.T, df2.T, df3.T
    df2.values[:, :-1] = df2.values[:, :-1].astype(int)
    mand_df = df2[df2["Courses", "Mandatory"] == "TRUE"]
    elec_df = df2[df2["Courses", "Mandatory"] == "FALSE"]
    return df1, df2, df3, mand_df, elec_df
