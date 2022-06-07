import numpy as np
import pandas as pd


def parse_plans():
    try:
        from bs4 import BeautifulSoup
    except ImportError as e:
        from pip._internal import main as pip
        pip(['install', '--user', 'beautifulsoup4'])
        from bs4 import BeautifulSoup

    from urllib.request import Request, urlopen

    base_link = "https://www.sis.itu.edu.tr/TR/ogrenci/lisans/ders-planlari/plan/YZVE/"
    req = Request(base_link)
    html_page = urlopen(req)

    soup = BeautifulSoup(html_page, "lxml")

    links = []
    titles = []
    texts = []
    for link in soup.findAll('a'):
        links.append(link.get('href'))
        titles.append(link.get('title'))
        texts.append(link.text)
      
    plan_links = []
    plan_titles = []

    for link, title, text in zip(links, titles, texts):
        if title == 'Ders Planını Görmek İçin Tıklayınız':
            plan_links.append(base_link + link)
            plan_titles.append(text)
    plans = []
    check = np.array(['Ders Kodu', 'Ders Adı', 'Kredi', 'Ders', 'Uyg.', 'Lab.', 'AKTS',
          'Türü', 'Z/S', 'Yarıyıl'])
    for plan_link in plan_links:
        tables = pd.read_html(plan_link)
        plan_tables = []
        for t in tables:
            if (t.iloc[0].values == check).all():
                plan_tables.append(t)
        plans.append(plan_tables)

    return plan_titles, plans


def filter_terms(df, term_list, titles, plans):
    titles = np.array(titles)
    if 'All Courses' in term_list:
        return df
    else:
        merged_df = None
        for term in term_list:
            term, no = term.split(' Donem: ')
            no, _ = no.split(' Zorunlu Dersler')
            sub_df = plans[np.argwhere(term == titles).item()][int(no)-1]
            sub_df.columns = sub_df.iloc[0]
            sub_df = sub_df[1:]
            if merged_df is not None:
                merged_df = pd.concat([merged_df, sub_df])
            else:
                merged_df = sub_df
        merged_df = merged_df.drop_duplicates()
        merged_df = merged_df[merged_df['Z/S']=='Z']
        merged_df.reset_index(inplace=True)
        if any(merged_df['Ders Kodu'] == 'YZV 101E') and \
            any(merged_df['Ders Kodu'] == 'YZV 103E'):
            merged_df = merged_df.drop(merged_df.index[
                          merged_df['Ders Kodu'] == 'YZV 101E'])
        if any(merged_df['Ders Kodu'] == 'YZV 102E') and \
            any(merged_df['Ders Kodu'] == 'YZV 104E'):
            merged_df = merged_df.drop(merged_df.index[
                          merged_df['Ders Kodu'] == 'YZV 102E'])
        if any(merged_df['Ders Kodu'] == 'YZV 212E') and \
            any(merged_df['Ders Kodu'] == 'YZV 321E'):
            merged_df = merged_df.drop(merged_df.index[
                          merged_df['Ders Kodu'] == 'YZV 212E'])
        if any(merged_df['Ders Kodu'] == 'YZV 302E') and \
            any(merged_df['Ders Kodu'] == 'YZV 203E'):
            merged_df = merged_df.drop(merged_df.index[
                          merged_df['Ders Kodu'] == 'YZV 302E'])
        if any(merged_df['Ders Kodu'] == 'YZV 311E') and \
            any(merged_df['Ders Kodu'] == 'YZV 312E'):
            merged_df = merged_df.drop(merged_df.index[
                          merged_df['Ders Kodu'] == 'YZV 311E'])

        merged_df['Ders Kodu'].mask(merged_df['Ders Kodu'] == 'YZV 101E',
                                    'YZV 101E/103E', inplace=True)
        merged_df['Ders Kodu'].mask(merged_df['Ders Kodu'] == 'YZV 103E',
                                    'YZV 101E/103E', inplace=True)
        merged_df['Ders Kodu'].mask(merged_df['Ders Kodu'] == 'YZV 102E',
                                    'YZV 102E/104E', inplace=True)  
        merged_df['Ders Kodu'].mask(merged_df['Ders Kodu'] == 'YZV 104E',
                                    'YZV 102E/104E', inplace=True)    
        merged_df['Ders Kodu'].mask(merged_df['Ders Kodu'] == 'YZV 212E',
                                    'YZV 212E/321E', inplace=True)  
        merged_df['Ders Kodu'].mask(merged_df['Ders Kodu'] == 'YZV 321E',
                                    'YZV 212E/321E', inplace=True)    
        merged_df['Ders Kodu'].mask(merged_df['Ders Kodu'] == 'YZV 302E',
                                    'YZV 302E/303E', inplace=True)    
        merged_df['Ders Kodu'].mask(merged_df['Ders Kodu'] == 'YZV 303E',
                                    'YZV 302E/303E', inplace=True)
        merged_df['Ders Kodu'].mask(merged_df['Ders Kodu'] == 'YZV 311E',
                                    'YZV 311E/312E', inplace=True)   
        merged_df['Ders Kodu'].mask(merged_df['Ders Kodu'] == 'YZV 312E',
                                    'YZV 311E/312E', inplace=True)                     

        filtered_df = df.loc[df.index.isin(merged_df['Ders Kodu'])]
        print(*term_list)
        return filtered_df
            


def parse_courses():
    from google.colab import auth
    auth.authenticate_user()

    import gspread
    from google.auth import default

    creds, _ = default()
    gc = gspread.authorize(creds)
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
    df1 = pd.DataFrame(rec[4:52, :26].T, index=midx)
    df1, df1.columns = df1.loc[df1.index.values[1:]], df1.loc[df1.index.values[0]]
    df1.sort_index(inplace=True)
    df1 = df1.T
    df1 = df1.drop(['YZV 101E', 'YZV 102E', 'YZV 212E', 'YZV 302E', 'YZV 311E'])
    df1 = df1.rename(index={'YZV 103E': 'YZV 101E/103E',
                                  'YZV 104E': 'YZV 102E/104E',
                                  'YZV 321E': 'YZV 212E/321E',
                                  'YZV 303E': 'YZV 302E/303E',
                                  'YZV 312E': 'YZV 311E/312E'})
    df1 = df1.T
    df2 = df1[~(df1 == "")].dropna(axis=1)
    df3 = df1.drop(df2.columns, axis=1)
    df1, df2, df3 = df1.T, df2.T, df3.T
    df2.values[:, :-1] = df2.values[:, :-1].astype(int)
    mand_df = df2[df2["Courses", "Mandatory"] == "TRUE"]
    elec_df = df2[df2["Courses", "Mandatory"] == "FALSE"]
    return df1, df2, df3, mand_df, elec_df
