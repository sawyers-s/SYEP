'''
File: syep_explorer.py

Description: The main application for creating interactive dashboard for SYEP dataset.
'''

# Import necessary packages
import panel as pn
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from syep_api import SYEP_API

# Loads javascript dependencies and configures Panel (required)
pn.extension()
pn.extension('tabulator')
pn.config.theme = 'default'


# INITIALIZE API
api = SYEP_API()
api.load_syep('Datasets/csv/SYEP.csv')
api.prepare_data()


# WIDGET DECLARATIONS

# Search widgets:

# Implement widget allowing user to select desired plot type
plot_type = pn.widgets.RadioBoxGroup(name = 'Plot type: ', options = ['Countplot', 'Stacked Bar Plot', 'Heatmap'],
                                     value = 'Countplot', inline = False, margin = (10, 0, 0, 30))

# Separate x and y selectors for each plot type, set default values to reasonable qualitative columns from dataset
x_axis_selection = pn.widgets.Select(name = 'X-axis: ', options = api.get_columns(), value = api.get_columns()[0],
                                     margin = (10, 0, 5, 20))
y_axis_selection = pn.widgets.Select(name = 'Y-axis: ', options = api.get_columns(), value = api.get_columns()[6],
                                     margin = (5, 0, 10, 20))

# Implement widgets to restrict plotting data based on respective column values, setting reasonable default values
gender_selection = pn.widgets.CheckBoxGroup(name = 'Gender(s): ', options = api.get_unique_genders(), value = [],
                                         margin = (5, 0, 10, 30))
race_selection = pn.widgets.MultiSelect(name = 'Race(s): ', options = api.get_unique_races(), value = [],
                                        margin = (5, 0, 10, 20))
second_language_selection = pn.widgets.MultiSelect(name = 'Second language(s): ', options = api.get_unique_second_languages(),
                                                     value = [], margin = (5, 0, 10, 20))
adult_live_with_selection = pn.widgets.MultiSelect(name = 'Adult(s) living with: ', options = api.get_unique_adult_live_with(),
                                                     value = [], margin = (5, 0, 10, 20))
job_format_selection = pn.widgets.CheckBoxGroup(name = 'Job format(s): ', options = api.get_unique_job_formats(), value = [],
                                         inline = False, margin = (5, 0, 10, 30))
program_selection = pn.widgets.CheckBoxGroup(name = 'Program(s): ', options = api.get_unique_programs(), value = [],
                                         inline = False, margin = (5, 0, 10, 30))
hours_worked_per_week_selection = pn.widgets.CheckBoxGroup(name = 'Hours worked per week: ', options = api.get_unique_hours_worked(),
                                                         value = [], inline = False, margin = (5, 0, 10, 30))
daily_work_type_selection = pn.widgets.MultiSelect(name = 'Daily work type(s): ', options = api.get_unique_daily_work(),
                                                         value = [], margin = (5, 0, 10, 20))


# Plotting widgets:

# Implement width and height widgets with values based on display size
width = pn.widgets.IntSlider(name = 'Width', start = 500, end = 1000, value = 650, step = 50, margin = (10, 0, 0, 30))
height = pn.widgets.IntSlider(name = 'Height', start = 200, end = 1200, value = 400, step = 50, margin = (10, 0, 0, 30))

# Implement widgets for visual plot customization and plot legibility (x-tick tilt/size/display/skip)
# Note: default countplot_color_picker value is matplotlib default blue hex code, #1f77b4
countplot_color_picker = pn.widgets.ColorPicker(name = 'Countplot color: ', value = '#1f77b4', margin = (10, 0, 0, 30))
stacked_palette_selector = pn.widgets.Select(name = 'Stacked bar plot palette: ',
                                             options = ['Set1', 'Set2', 'Set3', 'Pastel1', 'Pastel2', 'Paired'],
                                             margin = (10, 0, 0, 30))
heatmap_cmap_selector = pn.widgets.Select(name = 'Heatmap colormap: ',
                                          options = ['Blues', 'Reds', 'Greens', 'coolwarm', 'viridis', 'plasma'],
                                          margin = (10, 0, 0, 30))
border_checkbox = pn.widgets.Checkbox(name = 'Add border?', value = False, margin = (5, 0, 5, 30))
tilt_x_ticks = pn.widgets.Checkbox(name = 'Tilt x-axis ticks?', value = True, margin = (10, 0, 5, 30))
x_tick_font_size = pn.widgets.IntSlider(name = 'X-axis tick font size: ', start = 4, end = 20, value = 8, step = 1,
                                        margin = (20, 0, 10, 30))
show_all_x_ticks = pn.widgets.Checkbox(name = 'Show all x-axis ticks?', value = True, margin = (10, 0, 5, 30))
tick_skip_slider = pn.widgets.IntInput(name = 'Skip every n x-axis ticks: ', start = 2, end = 20, value = 2,
                                       margin = (10, 0, 10, 30))

# Table widgets:

# Implement widgets for customizing data displayed in table (series and overview)
include_all_data_checkbox = pn.widgets.Checkbox(name = 'Include all data?', value = False, margin = (10, 0, 10, 30))

# CALLBACK FUNCTIONS

def generate_table(x_axis_selection, y_axis_selection, gender_selection, race_selection, second_language_selection,
                   adult_live_with_selection, job_format_selection, program_selection, hours_worked_per_week_selection,
                   daily_work_type_selection, include_all_data_checkbox):
    '''
    Generate and return datatable in 'Table' tab of dashboard based on selections
    '''
    # Filter data by year, genre, and vote conditions
    filtered_data = api.filter_data(gender_selection, race_selection, second_language_selection, adult_live_with_selection,
                                    job_format_selection, program_selection, hours_worked_per_week_selection,
                                    daily_work_type_selection)

    # If filtered data is empty (no data meets all conditions), return error message
    if filtered_data.empty:
        return pn.pane.Markdown('### No data found matching the selected criteria.')

    # Ensure x_axis_selection and y_axis_selection are not None
    if x_axis_selection is None:
        print('X selection is None, cannot generate datatable.')

    if y_axis_selection is None:
        print('Y selection is None, cannot generate datatable.')

    # Initialize columns to include in datatable
    columns = [y_axis_selection]

    # If x_axis_selection or y_axis_selection are not valid, print error message
    if x_axis_selection not in api.syep.columns or y_axis_selection not in api.syep.columns:
        print(f'Selected values are not in dataframe columns: {x_axis_selection}, {y_axis_selection}')
    # If x_axis_selection and y_axis_selection are valid, add x_axis_selection to columns with y_axis_selection
    columns.insert(0, x_axis_selection)
    local = filtered_data[columns].dropna()

    # Include all data if checkbox is checked
    if include_all_data_checkbox:
        additional_columns = ['Program', 'Summer Job Experience: Did you work at the same location/employer last summer?', 'Summer Job Experience: What category best describes what you did this summer?', 'Summer Job Experience: On average, how many hours did you work each week this summer?', 'Summer Job Experience: What type of daily work did you do this summer?', 'Summer Job Experience: Overall, how well did the job match with your skills and interests?', 'Summer Job Experience: How likely are you to consider a career in the type of work you did this summer?', 'Summer Job Experience: If you had a job supervisor, how supportive were they overall?', 'Summer Job Experience: Did your supervisor - Properly train for your summer job?', 'Summer Job Experience: Did your supervisor - Help you understand your role at your summer job?', 'Summer Job Experience: Did your supervisor - Help you understand what was expected of you for your summer job?', 'Summer Job Experience: Did your supervisor - Give you feedback on how you were doing at your summer job?', 'Summer Job Experience: Did your supervisor - Help you think about how to achieve your educational or career goals?', 'Summer Job Experience: Did your supervisor - Make you feel comfortable talking about challenges outside of work?', 'Summer Job Experience: Overall, how would you rate your job experience this summer?', 'Summer Job Experience: Now that the summer is over - Do you have someone you can use as a job reference?', 'Summer Job Experience: Now that the summer is over - Do you have an adult you worked with that you consider a mentor?', 'Summer Job Experience: Now that the summer is over - Would you recommend this job to a friend?', 'Summer Job Experience: Now that the summer is over - Do you feel better prepared to enter a new job?', 'Summer Job Experience: Which of the following industries are you most interested in pursuing as a career?', 'Summer Job Experience: What do you plan to do after high school?', 'Job Search Skills: Indicate whether you have completed any of the following - I have prepared, edited, and proofread my resume.', 'Job Search Skills: Indicate whether you have completed any of the following - I have prepared, edited, and proofread my cover letter.', 'Job Search Skills: Indicate whether you have completed any of the following - I have asked an adult (e.g. family member, teacher, or neighbor) to serve as a reference for me when I apply for jobs.', 'Job Search Skills: Indicate whether you have completed any of the following - I have searched for jobs online using a job board (e.g. Monster, Indeed, Career Builder, Snagajob, Zip Recruiter)', 'Job Search Skills: Indicate whether you have completed any of the following  - I have talked with my family, neighbors, teachers, and friends, about the types of jobs I want -- and have asked for their help finding job opportunities.', 'Job Search Skills: Indicate whether you have completed any of the following  - I have developed some answer to the usual questions asked during an interview (e.g. what are your strength and weaknesses?)', 'Job Search Skills: Indicate whether you have completed any of the following - I have practiced my interviewing skills with an adult (e.g. family member, teacher, or neighbor).', 'Work Habits: Indicate how much you agree with each of the following phrases - I am usually on time for school or work.', 'Work Habits: Indicate how much you agree with each of the following phrases - I am rarely absent from school or call in sick.', 'Work Habits: Indicate how much you agree with each of the following phrases - I usually meet my deadlines and hand in assignments on time.', 'Work Habits: Indicate how much you agree with each of the following phrases - I often keep track of my assignments and rarely forget to hand things in.', 'Work Habits: Indicate how much you agree with each of the following phrases - I usually work independently without a lot of supervision.', 'Work Habits: Indicate how much you agree with each of the following phrases - I often ask for help if directions are not clear.', 'Work Habits: Indicate how much you agree with each of the following phrases - I often work in teams with other people.', 'Communication Skills: Indicate how much you agree with each of the following phrases - I rarely get upset or lose my temper with other people.', 'Communication Skills: Indicate how much you agree with each of the following phrases - I rarely get upset when supervisors or teachers correct my mistakes.', 'Communication Skills: Indicate how much you agree with each of the following phrases - I rarely get into arguments with my friends.', 'Communication Skills: Indicate how much you agree with each of the following phrases - I rarely get into arguments with my parents or teachers.', 'Communication Skills: Indicate how much you agree with each of the following phrases - I rarely have difficulty resolving arguments with people.', 'Communication Skills: Indicate how much you agree with each of the following phrases - I often make eye contact when having a conversation.', 'Job Search Skills: What skills do you feel that you need to develop and improve to meet your future career goals?', 'Job Search Skills: Which of the following best describe how you typically manage your money?', 'Job Search Skills: Do you have any items that you regularly help pay for in your household?', 'Relationships: Over the past 30 days, how often did you feel that EACH of the following was a positive role model for you?  - Parent', 'Relationships: Over the past 30 days, how often did you feel that EACH of the following was a positive role model for you?  - Brother or sister', 'Relationships: Over the past 30 days, how often did you feel that EACH of the following was a positive role model for you?  - Other family member (grandparent, aunt/uncle)', 'Relationships: Over the past 30 days, how often did you feel that EACH of the following was a positive role model for you?  - Teacher', 'Relationships: Over the past 30 days, how often did you feel that EACH of the following was a positive role model for you?  - Coach', 'Relationships: Over the past 30 days, how often did you feel that EACH of the following was a positive role model for you?  - Clergy (Minister/Priest, Imam, Rabbi)', 'Relationships: Over the past 30 days, how often did you feel that EACH of the following was a positive role model for you?  - Job Supervisor', 'Relationships: Over the past 30 days, how often did you feel that you had a lot to contribute to EACH of the following groups? - Family', 'Relationships: Over the past 30 days, how often did you feel that you had a lot to contribute to EACH of the following groups?  Friends', 'Relationships: Over the past 30 days, how often did you feel that you had a lot to contribute to EACH of the following groups? - Co-workers', 'Relationships: Over the past 30 days, how often did you feel that you had a lot to contribute to EACH of the following groups? - People in your neighborhood', 'Relationships: Over the past 30 days, how often did you feel that you had a lot to contribute to EACH of the following groups? - People in your school', 'Relationships: Over the past 30 days, how often did you feel that you had a lot to contribute to EACH of the following groups? - People in your place of worship', 'Well-being: Over the last two weeks, how often have you been bothered by the following problems? - Feeling nervous, anxious, or on edge', 'Well-being: Over the last two weeks, how often have you been bothered by the following problems? - Not being able to stop or control worrying', 'Well-being: Over the last two weeks, how often have you been bothered by the following problems? - Feeling down, depressed or hopeless', 'Well-being: Over the last two weeks, how often have you been bothered by the following problems? - Little interest or pleasure in doing things', 'Demographics: Gender', 'Demographics: Race', 'Demographics: Is there another language other than English that is regularly spoken in your home?', 'Demographics: What best describes the adult guardian that you primarily live with?']
        for column in additional_columns:
            if column == x_axis_selection:
                additional_columns.remove(column)
            elif column == y_axis_selection:
                additional_columns.remove(column)

        if additional_columns:
            local = pd.concat([local, filtered_data[additional_columns]], axis = 1)

    # Create and return datatable
    table = pn.widgets.Tabulator(local, selectable = False, show_index = False, pagination = None)
    return table


def generate_plot(plot_type, x_axis_selection, y_axis_selection, gender_selection, race_selection, second_language_selection,
                  adult_live_with_selection, job_format_selection, program_selection, hours_worked_per_week_selection,
                  daily_work_type_selection, width, height, countplot_color_picker, stacked_palette_selector,
                  heatmap_cmap_selector, border_checkbox, tilt_x_ticks, x_tick_font_size, show_all_x_ticks, tick_skip_slider):
    '''
    Generate and return plot in 'Plot' tab of dashboard based on selections
    '''
    # Close all previously open figures to prevent memory leaks
    plt.close('all')

    # Clear current plot
    plt.clf()

    # Ensure x_axis_selection is valid if appropriate. If not valid, set to default value to avoid error.
    if x_axis_selection is None:
            x_axis_selection = 'program'

    # Filter data by job format, program, hours worked per week, and daily job type conditions
    filtered_data = api.filter_data(gender_selection, race_selection, second_language_selection, adult_live_with_selection,
                                    job_format_selection, program_selection, hours_worked_per_week_selection,
                                    daily_work_type_selection)

    # If filtered data is empty (no data meets all conditions), return error message
    if filtered_data.empty:
        return pn.pane.Markdown('### No data found matching the selected criteria.')

    # Set border to black if border_checkbox is checked
    edgecolor = 'black' if border_checkbox else 'none'

    # Create plot based on plot_type selection
    if plot_type == 'Countplot':
        plot_figure = api.create_plot(plot_type, width, height, x_axis_selection, y_axis_selection, filtered_data,
                                      countplot_color=countplot_color_picker, edgecolor=edgecolor)
    elif plot_type == 'Stacked Bar Plot':
        plot_figure = api.create_plot(plot_type, width, height, x_axis_selection, y_axis_selection, filtered_data,
                                      stacked_bar_plot_palette=stacked_palette_selector, edgecolor=edgecolor)
    elif plot_type == 'Heatmap':
        plot_figure = api.create_plot(plot_type, width, height, x_axis_selection, y_axis_selection, filtered_data,
                                      heatmap_cmap=heatmap_cmap_selector, edgecolor=edgecolor)

    # Get current axis
    ax = plt.gca()

    # If wanting to show all x-ticks, use get_xticks() for tick locations. Force x-tick locations to be integers.
    tick_locations = ax.get_xticks()
    int_tick_locations = np.arange(int(min(tick_locations)), int(max(tick_locations)) + 1)
    plt.xticks(ticks = int_tick_locations, fontsize = x_tick_font_size)

    # If not wanting to show all x-ticks, calculate new tick locations to skip tick_skip_slider values (documentation
    # help from ChatGPT)
    if not show_all_x_ticks and tick_skip_slider > 1:
        int_tick_locations = [loc for i, loc in enumerate(int_tick_locations) if i % tick_skip_slider == 0]
        plt.xticks(ticks = int_tick_locations, fontsize = x_tick_font_size)

    # Rotate x-ticks if tilt_x_ticks is checked
    if tilt_x_ticks:
        plt.xticks(rotation = 45)

    return pn.pane.Matplotlib(plot_figure)


# CALLBACK BINDINGS (Connecting widgets to callback functions)

# Bind datatable to widgets
datatable = pn.bind(generate_table, x_axis_selection, y_axis_selection, gender_selection, race_selection,
                    second_language_selection, adult_live_with_selection, job_format_selection, program_selection,
                    hours_worked_per_week_selection, daily_work_type_selection, include_all_data_checkbox)

# Bind plot to widgets
plot = pn.bind(generate_plot, plot_type, x_axis_selection, y_axis_selection, gender_selection, race_selection,
               second_language_selection, adult_live_with_selection, job_format_selection, program_selection,
                hours_worked_per_week_selection, daily_work_type_selection, width, height, countplot_color_picker,
                stacked_palette_selector, heatmap_cmap_selector, border_checkbox, tilt_x_ticks, x_tick_font_size,
               show_all_x_ticks, tick_skip_slider)


# Define the dashboard content (main dashboard components)
dashboard = pn.Column(
    pn.Tabs(
        ('Plot', plot),  # Replace with actual plot content
        ('Table', datatable),  # Replace with actual table content
        active=0  # Which tab is active by default?
    ),
)


# LANDING PAGE COMPONENT
# Define the landing page content (this will be shown in a dialog)
landing_page_content = pn.Column(
    pn.pane.Markdown("""
    <h1 style="font-size: 40px;">Welcome to the SYEP Database Explorer!</h1>

    <p style="font-size: 20px;">This dashboard allows you to interactively explore the <strong>Summer Youth Employment Program (SYEP)</strong> dataset. 
    The data includes insights about youth participants in various summer job programs, including details about their experiences, demographics, and employment conditions.</p>

    <strong>Click the button below to start exploring the data.</strong>
    """, sizing_mode='stretch_width'),

    pn.widgets.Button(
        name="Start Exploring",
        button_type='primary',
        width=200,
        height=50,  # Set a fixed height
        sizing_mode='fixed',
        align='center',
        margin=(10, 10, 10, 10)
    )
)

# Make dashboard initially invisible
dashboard.visible = False

# Callback to transition from Dialog to main dashboard
def show_dashboard(event):
    landing_page_content.visible = False  # Close the dialog
    dashboard.visible = True  # Show the dashboard

# Attach the callback to the button
landing_page_content[1].on_click(show_dashboard)


# DASHBOARD WIDGET CONTAINERS ("CARDS")

card_width = 400

# Add headers above widgets to guide user selections
plot_type_header = pn.pane.Markdown("#### Plot type: ", margin = (-5, 0, -15, 10))
gender_header = pn.pane.Markdown("Gender: ", margin = (-20, 0, -20, 10))
job_format_header = pn.pane.Markdown("Job format: ", margin = (-20, 0, -20, 10))
program_header = pn.pane.Markdown("Program: ", margin = (-20, 0, -20, 10))
hours_worked_per_week_header = pn.pane.Markdown("Hours worked per week: ", margin = (-20, 0, -20, 10))
search_type_header_demographics = pn.pane.Markdown("#### Demographics: ", margin = (-10, 0, -10, 10))
search_type_header_program = pn.pane.Markdown("#### Program attributes: ", margin = (-10, 0, -10, 10))
add_border_header = pn.pane.Markdown("#### For countplots and stacked bar plots ONLY: ", margin = (0, 0, -10, 10))
show_all_x_ticks_header = pn.pane.Markdown("#### If NOT showing all x-axis ticks: ", margin = (-10, 0, -15, 10))

# Create markdown for survey question guide
survey_guide_df = pd.read_csv("survey_question_guide.csv")
md_table = survey_guide_df.to_markdown(index=False)
survey_guide = pn.pane.Markdown(f"### Survey question guide\n\n{md_table}", height=400, sizing_mode="stretch_width")

# Create 'Search' card
search_card = pn.Card(
    pn.Column(
        plot_type_header,
        plot_type,
        x_axis_selection,
        y_axis_selection,
        search_type_header_demographics,
        gender_header,
        gender_selection,
        race_selection,
        second_language_selection,
        adult_live_with_selection,
        search_type_header_program,
        job_format_header,
        job_format_selection,
        program_header,
        program_selection,
        hours_worked_per_week_header,
        hours_worked_per_week_selection,
        daily_work_type_selection,
    ),
    title = 'Search', width = card_width, collapsed = False
)

# Create 'Plot' card
plot_card = pn.Card(
    pn.Column(
        width,
        height,
        countplot_color_picker,
        stacked_palette_selector,
        heatmap_cmap_selector,
        add_border_header,
        border_checkbox,
        x_tick_font_size,
        tilt_x_ticks,
        show_all_x_ticks,
        show_all_x_ticks_header,
        tick_skip_slider,
    ),
    title = 'Plot', width = card_width, collapsed = True
)

# Create 'Table' card
table_card = pn.Card(
    pn.Column(
        include_all_data_checkbox,
    ),
    title = 'Table', width = card_width, collapsed = True
)


# LAYOUT

css = """
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&display=swap');

/* Set Montserrat font globally and in the host */
:host {
    --base-font: 'Montserrat', sans-serif !important;
}

/* Default font family for the entire layout */
body {
    font-family: 'Montserrat', sans-serif !important;
}

/* Apply bold font to the header */
#header .app-header .title {
    font-weight: bold;
}
"""

# Initialize Panel with the custom CSS
pn.extension(raw_css=[css])

# Set up layout
layout = pn.template.FastListTemplate(
    title = 'CITY of BOSTON SYEP Database Explorer',
    sidebar = [
        search_card,
        plot_card,
        table_card
    ],
    theme_toggle = False,
    main = [
        pn.Column(landing_page_content, dashboard)
    ],
    header_background = '#091F2F',
    logo = 'https://www.boston.gov/sites/default/files/styles/med_small_square__200x200_/public/img/columns/2016/11/cob_b_white-01.png?itok=-SZRDrhw',
    sidebar_width=405,
).servable()