import ipywidgets as widgets
from src.parsers.parser import parse_courses


df1, df2, df3, mand_df, elec_df = parse_courses()


course_types = {'All':df2.index, 'Mandatory':mand_df.index, 'Elective': elec_df.index}


def handle_choice(choice):
    if 'All' in choice:
        return df2.index
    elif 'Mandatory' in choice and 'Elective' in choice:
        return df2.index
    elif 'Mandatory' in choice:
        return mand_df.index
    elif 'Elective' in choice:
        return elec_df.index
    else:
        return list(choice)
        

course_widget = widgets.Dropdown(
    options=df2.index,
    value=df2.index[0],
    description='Course:',
    continuous_update=False,
    disabled=False,
)

pi_widget = widgets.SelectionSlider(
    options=['1', '2', '3', '4', '5', '6', '7'],
    value='1',
    description='PI Selection:',
    disabled=False,
    continuous_update=True,
    orientation='horizontal',
    readout=True
)

subpi_widget = widgets.Dropdown(
    options=list(df2.loc[:, "1":"7"].T.index.levels[1][2:]),
    value='PI.1.1',
    description='Sub-PI Selection:',
    disabled=False,
    continuous_update=True,
    readout=True
)

dist_widget = widgets.SelectMultiple(
    options=list(course_types.keys()) + list(df2.index),
    value=('All',),
    description='Courses:',
    disabled=False
)
