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
                                     value = 'Countplot', inline = False, margin = (10, 0, 0, 10))

# Separate x and y selectors for each plot type, set default values to reasonable qualitative columns from dataset
x_axis_selection = pn.widgets.Select(name = 'X-axis: ', options = api.get_columns(), value = api.get_columns()[0],
                                     margin = (10, 0, 5, 10))
y_axis_selection = pn.widgets.Select(name = 'Y-axis: ', options = api.get_columns(), value = api.get_columns()[6],
                                     margin = (5, 0, 10, 10))

# Implement widgets to restrict plotting data based on respective column values, setting reasonable default values
gender_selection = pn.widgets.CheckBoxGroup(name = 'Gender(s): ', options = api.get_unique_genders(), value = [],
                                         margin = (5, 0, 10, 10))
race_selection = pn.widgets.MultiSelect(name = 'Race(s): ', options = api.get_unique_races(), value = [],
                                        margin = (5, 0, 10, 10))
second_language_selection = pn.widgets.MultiSelect(name = 'Second language(s): ', options = api.get_unique_second_languages(),
                                                     value = [], margin = (5, 0, 10, 10))
adult_live_with_selection = pn.widgets.MultiSelect(name = 'Adult(s) living with: ', options = api.get_unique_adult_live_with(),
                                                     value = [], margin = (5, 0, 10, 10))
job_format_selection = pn.widgets.CheckBoxGroup(name = 'Job format(s): ', options = api.get_unique_job_formats(), value = [],
                                         inline = False, margin = (5, 0, 10, 10))
program_selection = pn.widgets.CheckBoxGroup(name = 'Program(s): ', options = api.get_unique_programs(), value = [],
                                         inline = False, margin = (5, 0, 10, 10))
hours_worked_per_week_selection = pn.widgets.CheckBoxGroup(name = 'Hours worked per week: ', options = api.get_unique_hours_worked(),
                                                         value = [], inline = False, margin = (5, 0, 10, 10))
daily_work_type_selection = pn.widgets.MultiSelect(name = 'Daily work type(s): ', options = api.get_unique_daily_work(),
                                                         value = [], margin = (5, 0, 10, 10))

# Plotting widgets:

# Implement width and height widgets with values based on display size
width = pn.widgets.IntSlider(name = 'Width: ', start = 500, end = 1000, value = 750, step = 50, margin = (10, 0, 0, 10))
height = pn.widgets.IntSlider(name = 'Height: ', start = 200, end = 1200, value = 400, step = 50)

# Implement widgets for visual plot customization and plot legibility (x-tick tilt/size/display/skip)
# Note: default countplot_color_picker value is matplotlib default blue hex code, #1f77b4
countplot_color_picker = pn.widgets.ColorPicker(name = 'Countplot color: ', value = '#1f77b4')
stacked_palette_selector = pn.widgets.Select(name = 'Stacked bar plot palette: ',
                                             options = ['Set1', 'Set2', 'Set3', 'Pastel1', 'Pastel2', 'Paired'])
heatmap_cmap_selector = pn.widgets.Select(name = 'Heatmap colormap: ',
                                          options = ['Blues', 'Reds', 'Greens', 'coolwarm', 'viridis', 'plasma'])
border_checkbox = pn.widgets.Checkbox(name = 'Add border?', value = False, margin = (5, 0, 5, 10))
tilt_x_ticks = pn.widgets.Checkbox(name = 'Tilt x-axis ticks?', value = True, margin = (10, 0, 5, 10))
x_tick_font_size = pn.widgets.IntSlider(name = 'X-axis tick font size: ', start = 4, end = 20, value = 8, step = 1,
                                        margin = (20, 0, 10, 10))
show_all_x_ticks = pn.widgets.Checkbox(name = 'Show all x-axis ticks?', value = False, margin = (10, 0, 5, 10))
tick_skip_slider = pn.widgets.IntInput(name = 'Skip every n x-axis ticks: ', start = 2, end = 20, value = 4,
                                       margin = (10, 0, 10, 10))

# Table widgets:

# Implement widgets for customizing data displayed in table (series and overview)
include_all_data_checkbox = pn.widgets.Checkbox(name = 'Include all data?', value = False, margin = (10, 0, 0, 10))

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
        additional_columns = ['program', 'first_name', 'last_name', 'email', 'same_employer', 'job_format', 'hours_worked_per_week', 'daily_work_type', 'job_match_interests', 'consider_career_likelihood', 'supervisor_support', 'supervisor_properly_train', 'supervisor_understand_role', 'supervisor_understand_expectations', 'supervisor_give_feedback', 'supervisor_achieve_goals', 'supervisor_comfortable', 'experience_rating', 'job_reference_person', 'mentor_person', 'recommend_job', 'new_job_prepared', 'interested_in_pursuing', 'post_high_school_plans', 'prepared_resume', 'prepared_cover_letter', 'asked_adult_reference', 'searched_jobs_online', 'discussed_wanted_jobs', 'developed_interview_answers', 'practiced_interviewing', 'usually_on_time_school_work', 'rarely_absent_school', 'meet_deadlines', 'keep_track_assignments', 'work_independently', 'ask_for_help', 'work_in_teams', 'rarely_get_upset_or_lose_temper', 'rarely_get_upset_when_corrected', 'rarely_get_into_arguments_friends', 'rarely_get_into_arguments_parents_teachers', 'rarely_difficulty_resolving_arguments', 'often_eye_contact_during_conversation', 'skills_to_improve', 'typically_manage_money', 'household_items_paid_for', 'parent_role_model', 'sibling_role_model', 'family_role_model', 'teacher_role_model', 'coach_role_model', 'clergy_role_model', 'supervisor_role_model', 'contribute_family', 'contribute_friends', 'contribute_coworkers', 'contribute_neighborhood', 'contribute_school', 'contribute_worship', 'feeling_nervous', 'cannot_stop_worrying', 'feeling_down', 'little_interest_in_things', 'gender', 'race', 'second_language_spoken_at_home', 'adult_live_with']
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


# DASHBOARD WIDGET CONTAINERS ("CARDS")

card_width = 330

# Add headers above widgets to guide user selections
plot_type_header = pn.pane.Markdown("#### Plot type: ", margin = (-5, 0, -15, 0))
gender_header = pn.pane.Markdown("Gender: ", margin = (-20, 0, -20, 0))
job_format_header = pn.pane.Markdown("Job format: ", margin = (-20, 0, -20, 0))
program_header = pn.pane.Markdown("Program: ", margin = (-20, 0, -20, 0))
hours_worked_per_week_header = pn.pane.Markdown("Hours worked per week: ", margin = (-20, 0, -20, 0))
search_type_header_demographics = pn.pane.Markdown("#### Demographics: ", margin = (-10, 0, -10, 0))
search_type_header_program = pn.pane.Markdown("#### Program attributes: ", margin = (-10, 0, -10, 0))
add_border_header = pn.pane.Markdown("#### For countplots and stacked bar plots ONLY: ", margin = (0, 0, -10, 0))
show_all_x_ticks_header = pn.pane.Markdown("#### If NOT showing all x-axis ticks: ", margin = (-10, 0, -15, 0))

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
        daily_work_type_selection
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
        tick_skip_slider
    ),
    title = 'Plot', width = card_width, collapsed = True
)

# Create 'Table' card
table_card = pn.Card(
    pn.Column(
        include_all_data_checkbox
    ),
    title = 'Table', width = card_width, collapsed = True
)


# LAYOUT

# Set up layout
layout = pn.template.FastListTemplate(
    title = 'SYEP Database Explorer',
    sidebar = [
        search_card,
        plot_card,
        table_card
    ],
    theme_toggle = False,
    main = [
        pn.Tabs(
            ('Plot', plot),  # Replace None with callback binding
            ('Table', datatable),  # Replace None with callback binding
            ('Guide', survey_guide),
            active = 0  # Which tab is active by default?
        )
    ],
    header_background = '#000000'
).servable()

layout.show()
