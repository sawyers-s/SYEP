'''
File: syep_api.py

Description: The primary API for interacting with the SYEP data.
'''

# Import necessary packages
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define API class
class SYEP_API:

    syep = None  # dataframe

    def load_syep(self, filename):
        '''
        Load in dataset as pandas dataframe
        '''
        self.syep = pd.read_csv(filename)


    def get_columns(self):
        '''
        Get and return list of columns in dataset
        '''
        return list(self.syep.columns)


    def prepare_data(self):
        '''
        Remove excess whitespace from all values in the data
        '''
        self.syep = self.syep.map(lambda x: x.strip() if isinstance(x, str) else x)


    def get_unique_genders(self):
        '''
        Get and return list of unique genders from dataset
        '''
        unique_genders = self.syep['gender'].dropna().astype(str).unique()
        return sorted(unique_genders)


    def get_unique_races(self):
        '''
        Get and return list of unique races from dataset
        '''
        unique_races = self.syep['race'].dropna().astype(str).unique()
        return sorted(unique_races)


    def get_unique_second_languages(self):
        '''
        Get and return list of unique second languages from dataset
        '''
        unique_second_languages = self.syep['second_language_spoken_at_home'].dropna().astype(str).unique()
        return sorted(unique_second_languages)


    def get_unique_adult_live_with(self):
        '''
        Get and return list of unique adults live with from dataset
        '''
        unique_adults_live_with = self.syep['adult_live_with'].dropna().astype(str).unique()
        return sorted(unique_adults_live_with)


    def get_unique_job_formats(self):
        '''
        Get and return list of unique job formats from dataset
        '''
        unique_job_formats = self.syep['job_format'].dropna().astype(str).unique()
        return sorted(unique_job_formats)


    def get_unique_programs(self):
        '''
        Get and return list of unique programs from dataset
        '''
        unique_programs = self.syep['program'].dropna().astype(str).unique()
        return sorted(unique_programs)


    def get_unique_hours_worked(self):
        '''
        Get and return list of unique hours worked per week values from dataset
        '''
        unique_hours_worked = self.syep['hours_worked_per_week'].dropna().astype(str).unique()
        return sorted(unique_hours_worked)


    def get_unique_daily_work(self):
        '''
        Get and return list of unique daily work type values from dataset
        '''
        unique_daily_work = self.syep['daily_work_type'].dropna().astype(str).unique()
        return sorted(unique_daily_work)


    def filter_data(self, gender=None, race=None, second_language_spoken_at_home=None, adult_live_with=None,
                    job_format=None, program=None, hours_worked_per_week=None, daily_work_type=None):
        '''
        Filter data by demographics (gender, race, second_language_spoken_at_home, adult_live_with) and program attributes
        (job_format, program, hours_worked_per_week, daily_work_type) and return filtered dataset
        '''
        # Start with the complete dataset
        filtered_data = self.syep

        # Ensure single values are converted to lists
        if gender and not isinstance(gender, list):
            gender = [gender]
        if race and not isinstance(race, list):
            race = [race]
        if second_language_spoken_at_home and not isinstance(second_language_spoken_at_home, list):
            second_language_spoken_at_home = [second_language_spoken_at_home]
        if adult_live_with and not isinstance(adult_live_with, list):
            adult_live_with = [adult_live_with]
        if job_format and not isinstance(job_format, list):
            job_format = [job_format]
        if program and not isinstance(program, list):
            program = [program]
        if hours_worked_per_week and not isinstance(hours_worked_per_week, list):
            hours_worked_per_week = [hours_worked_per_week]
        if daily_work_type and not isinstance(daily_work_type, list):
            daily_work_type = [daily_work_type]

        # Filter by gender if provided
        if gender:
            filtered_data = filtered_data[filtered_data['gender'].isin(gender)]

        # Filter by race if provided
        if race:
            filtered_data = filtered_data[filtered_data['race'].isin(race)]

        # Filter by second language spoken at home if provided
        if second_language_spoken_at_home:
            filtered_data = filtered_data[filtered_data['second_language_spoken_at_home'].isin(second_language_spoken_at_home)]

        # Filter by adult live with if provided
        if adult_live_with:
            filtered_data = filtered_data[filtered_data['adult_live_with'].isin(adult_live_with)]

        # Filter by job format if provided
        if job_format:
            filtered_data = filtered_data[filtered_data['job_format'].isin(job_format)]

        # Filter by program if provided
        if program:
            filtered_data = filtered_data[filtered_data['program'].isin(program)]

        # Filter by hours worked per week if provided
        if hours_worked_per_week:
            filtered_data = filtered_data[filtered_data['hours_worked_per_week'].isin(hours_worked_per_week)]

        # Filter by daily work type if provided
        if daily_work_type:
            filtered_data = filtered_data[filtered_data['daily_work_type'].isin(daily_work_type)]

        # Return the filtered data
        return filtered_data


    def create_plot(self, plot_type, width=600, height=400, x_axis=None, y_axis=None, data=None, countplot_color='#1f77b4',
                    stacked_bar_plot_palette='Set1', heatmap_cmap='Blues', edgecolor='None'):
        '''
        Create and return a plot (countplot, stacked bar plot, or heatmap) based on plot_type and
        parameter widget selections
        '''
        # Use original data if none is provided
        if data is None:
            data = self.syep

        # Clear current figure
        plt.clf()

        # Create new figure
        plt.figure(figsize=(width / 100, height / 100))

        # Create plot_type
        if plot_type == 'Countplot':
            # For categorical data (countplot)
            sns.countplot(x=x_axis, data=data, color=countplot_color, edgecolor=edgecolor)
            # Remove underscore from column name for x-label and use same method for title
            plt.xlabel(x_axis.replace('_', ' '))
            plt.ylabel('Count')
            plt.title(f'Count Plot of {x_axis.replace("_", " ").title()}')

        elif plot_type == 'Stacked Bar Plot':
            # For stacked bar plot, using crosstab and plotting
            crosstab_data = pd.crosstab(data[x_axis], data[y_axis])
            colors = sns.color_palette(stacked_bar_plot_palette)
            crosstab_data.plot(kind='bar', stacked=True, color=colors, edgecolor=edgecolor)
            plt.xlabel(x_axis.replace('_', ' '))
            plt.ylabel('Count')
            plt.title(f'Stacked Bar Plot of {y_axis.replace("_", " ").title()} by {x_axis.replace("_", " ").title()}')

        elif plot_type == 'Heatmap':
            # For heatmap, using crosstab for two categorical variables
            crosstab_data = pd.crosstab(data[x_axis], data[y_axis])
            # Ensure the colormap input is valid before applying it
            if isinstance(heatmap_cmap, str) and heatmap_cmap in plt.colormaps():
                cmap = heatmap_cmap
            else:
                cmap = 'Blues' # use default if given heatmap cmap is invalid
            sns.heatmap(crosstab_data, annot=True, cmap=cmap, cbar_kws={'label': 'Count'})
            plt.xlabel(x_axis.replace('_', ' '))
            plt.ylabel(y_axis.replace('_', ' '))
            plt.yticks(rotation=90)
            plt.title(f'Heatmap of {y_axis.replace("_", " ").title()} by {x_axis.replace("_", " ").title()}')

        # Set x-tick rotation default value to horizontal
        plt.xticks(rotation=0)

        return plt.gcf()


def main():

    # Create instance of SYEP_API
    syep_api = SYEP_API()

    # Load IMDb dataset
    syep_api.load_syep('Datasets/csv/SYEP.csv')

    # Get and display columns in dataset
    columns = syep_api.get_columns()
    print('Columns: ', columns, '\n')

    # Prepare data for use in dashboard creation
    syep_api.prepare_data()

    # Get and display unique values
    unique_genders = syep_api.get_unique_genders()
    print('Unique genders: ', unique_genders, '\n')
    unique_races = syep_api.get_unique_races()
    print('Unique races: ', unique_races, '\n')
    unique_second_languages = syep_api.get_unique_second_languages()
    print('Unique second languages: ', unique_second_languages, '\n')
    unique_adult_live_with =  syep_api.get_unique_adult_live_with()
    print('Unique adults live with: ', unique_adult_live_with, '\n')
    unique_job_formats = syep_api.get_unique_job_formats()
    print('Unique job formats: ', unique_job_formats, '\n')
    unique_programs = syep_api.get_unique_programs()
    print('Unique programs: ', unique_programs, '\n')
    unique_hours_worked = syep_api.get_unique_hours_worked()
    print('Unique hours worked per week: ', unique_hours_worked, '\n')
    unique_daily_work = syep_api.get_unique_daily_work()
    print('Unique daily work: ', unique_daily_work, '\n')

    # Sample filter data and display filtered data
    gender = 'Female'
    race = 'Hispanic or Latino'
    job_format = 'I had an in-person job or internship'
    hours_worked_per_week = '21 to 25'
    filtered_data = syep_api.filter_data(gender, race, job_format=job_format, hours_worked_per_week=hours_worked_per_week)
    print('Filtered data: ', filtered_data, '\n')

    # Create sample plot
    if not filtered_data.empty:
        plot_type = 'Heatmap'
        width = 800
        height = 800
        x_axis = 'race'
        y_axis = 'household_items_paid_for'
        sample_plot = syep_api.create_plot(plot_type, width, height, x_axis, y_axis, filtered_data)
        plt.show()


if __name__ == '__main__':
    main()