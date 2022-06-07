import ipywidgets as widgets
from src.parsers.parser import parse_courses, parse_plans


df1, df2, df3, mand_df, elec_df = parse_courses()

plan_titles, plans = parse_plans()


course_types = {'All':df2.index, 'Mandatory':mand_df.index, 'Elective': elec_df.index}

term_list = ['All Courses']
for plan_title in plan_titles:
    terms = [plan_title + ' Donem: ' + str(i) + ' Zorunlu Dersler' for i in range(1, 9)]
    term_list = term_list + terms

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

full_contrib_filter = widgets.Checkbox(
    value=False,
    description='Filter by Full Course Contribution',
    disabled=False
)

mandatory_filter = widgets.Checkbox(
    value=True,
    description='Filter Mandatory Course Contribution',
    disabled=False
)

termplan_widget = widgets.SelectMultiple(
    options=term_list,
    value=('All Courses',),
    description='Filter courses by plans and terms:',
    disabled=False,
    display='flex',
    layout={'height': '250px', 'width': '500px', 'description_width': '400px'}
)
