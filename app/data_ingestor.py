import os
import json
import csv
import pandas as pd

class DataIngestor:
    def __init__(self, csv_path: str):
        # The csv has the following columns:
        # YearStart,YearEnd, LocationAbbr, LocationDesc, Datasource, Class, Topic, Question, Data_Value_Unit,Data_Value_Type,Data_Value,
        # Data_Value_Alt, Data_Value_Footnote_Symbol, Data_Value_Footnote, Low_Confidence_Limit, High_Confidence_Limit, Sample_Size,Total,
        # Age(years), Education, Gender, Income, Race/Ethnicity, GeoLocation, ClassID, TopicID, QuestionID, DataValueTypeID, LocationID,
        # StratificationCategory1, Stratification1, StratificationCategoryId1, StratificationID1
        # Create the results directory if it does not exist
        if not os.path.exists('results'):
            os.makedirs('results')

        self.data = pd.read_csv(csv_path)

    def __get__(self):
        return self.data

class JobMaintainer:
    def __init__(self):
        self.running_jobs = set()
        self.done_jobs = set()

    def is_job_running(self, job_id):
        return job_id in self.running_jobs
    
    def is_job_done(self, job_id):
        return job_id in self.done_jobs
    
    def finish_job(self, job_id):
        self.running_jobs.remove(job_id)
        self.done_jobs.add(job_id)

    def start_job(self, job_id):
        self.running_jobs.add(job_id)
    
class DataParser:
    def __init__(self, data: DataIngestor):
        self.job_maintainer = JobMaintainer()
        self.data = data.__get__()

        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]

        self.questions_best_is_max = [
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week',
            'Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week',
        ]

    def json_writer(self, data, job_id):
        # Use zip to create a dictionary with the structure {state: mean}
        data_dict = dict(zip(data['LocationDesc'], data['Data_Value']))

        # Save the results in results/ directory with the name of the job_id as json file  
        with open(f'results/{job_id}.json', 'w') as f:
            # Write field:value pairs in json format
            json.dump(data_dict, f)       

    def get_global_mean(self, data):
        # Computes the global mean of the data values for the question in the the interval 2011-2022
        # Extract question from data
        question = data['question']
        best_is_min = False
        if question in self.questions_best_is_min:
            best_is_min = True

        # Filter data for the question
        data_filtered = self.data[self.data['Question'] == question]
        data_filtered = data_filtered[(data_filtered['YearStart'] >= 2011) & (data_filtered['YearEnd'] <= 2022)]
        data_filtered = data_filtered.dropna(subset=['Data_Value'])

        # Compute the global mean of the data values
        data_mean = data_filtered['Data_Value'].mean()
        data_mean = pd.DataFrame({'Data_Value': [data_mean]})

        # Return data_mean as value
        return data_mean      

    def states_mean(self, data, job_id):
        # Start job
        self.job_maintainer.start_job(job_id)

        # Computes the mean of the data values for each state in the the interval 2011-2022 and orders ascendingly by mean
        # Extract question from data
        question = data['question']
        best_is_min = False
        if question in self.questions_best_is_min:
            best_is_min = True

        # Filter data for the question
        data_filtered = self.data[self.data['Question'] == question]
        data_filtered = data_filtered[(data_filtered['YearStart'] >= 2011) & (data_filtered['YearEnd'] <= 2022)]
        data_filtered = data_filtered.dropna(subset=['Data_Value'])

        # Compute the mean of the data values for each state
        data_mean = data_filtered.groupby('LocationDesc')['Data_Value'].mean().reset_index()   
        data_mean = data_mean.sort_values('Data_Value', ascending=best_is_min)

        # Write the results in results/ directory with the name of the job_id as json file
        self.json_writer(data_mean, job_id)

        self.job_maintainer.finish_job(job_id)

    def state_mean(self, data, job_id):
        # Start job
        self.job_maintainer.start_job(job_id)

        # Computes the mean of the data values for the state in the the interval 2011-2022
        # Extract question and state from data
        question = data['question']
        state = data['state']

        # Filter data for the question and state
        data_filtered = self.data[(self.data['Question'] == question) & (self.data['LocationDesc'] == state)]
        data_filtered = data_filtered[(data_filtered['YearStart'] >= 2011) & (data_filtered['YearEnd'] <= 2022)]
        data_filtered = data_filtered.dropna(subset=['Data_Value'])
        
        # Create the mean result from filter
        data_mean = data_filtered['Data_Value'].mean()
        data_mean = pd.DataFrame({'LocationDesc': [state], 'Data_Value': [data_mean]})

        print(data_mean)

        # Write the results in results/ directory with the name of the job_id as json file  
        self.json_writer(data_mean, job_id)

        self.job_maintainer.finish_job(job_id)

    def best5(self, data, job_id):
        # Start job
        self.job_maintainer.start_job(job_id)

        # Computes the best 5 states for the question in the the interval 2011-2022
        # Extract question from data
        question = data['question']
        best_is_min = False
        if question in self.questions_best_is_min:
            best_is_min = True

        # Filter data for the question
        data_filtered = self.data[self.data['Question'] == question]
        data_filtered = data_filtered[(data_filtered['YearStart'] >= 2011) & (data_filtered['YearEnd'] <= 2022)]
        data_filtered = data_filtered.dropna(subset=['Data_Value'])

        # Compute the mean of the data values for each state
        data_mean = data_filtered.groupby('LocationDesc')['Data_Value'].mean().reset_index()   
        data_mean = data_mean.sort_values('Data_Value', ascending=best_is_min)

        # Get the best 5 states
        data_best5 = data_mean.head(5)

        # Write the results in results/ directory with the name of the job_id as json file
        self.json_writer(data_best5, job_id)

        self.job_maintainer.finish_job(job_id)

    def worst5(self, data, job_id):
        # Start job
        self.job_maintainer.start_job(job_id)
        
        # Computes the worst 5 states for the question in the the interval 2011-2022
        # Extract question from data
        question = data['question']
        best_is_min = False
        if question in self.questions_best_is_min:
            best_is_min = True

        # Filter data for the question
        data_filtered = self.data[self.data['Question'] == question]
        data_filtered = data_filtered[(data_filtered['YearStart'] >= 2011) & (data_filtered['YearEnd'] <= 2022)]
        data_filtered = data_filtered.dropna(subset=['Data_Value'])

        # Compute the mean of the data values for each state
        data_mean = data_filtered.groupby('LocationDesc')['Data_Value'].mean().reset_index()   
        data_mean = data_mean.sort_values('Data_Value', ascending=not best_is_min)

        # Get the worst 5 states
        data_worst5 = data_mean.head(5)

        # Write the results in results/ directory with the name of the job_id as json file
        self.json_writer(data_worst5, job_id)

        self.job_maintainer.finish_job(job_id)

    def global_mean(self, data, job_id):
        # Start job
        self.job_maintainer.start_job(job_id)
        
        # Computes the global mean of the data values for the question in the the interval 2011-2022
        data_mean = self.get_global_mean(data)

        # Create output as {"global_mean" : value}
        data_dict = {"global_mean": data_mean['Data_Value'].values[0]}
        with open(f'results/{job_id}.json', 'w') as f:
            # Write field:value pairs in json format
            json.dump(data_dict, f)

        self.job_maintainer.finish_job(job_id)

    def diff_from_mean(self, data, job_id):
        # Start job
        self.job_maintainer.start_job(job_id)

        # Computes the difference of the data values for the state from the global mean in the the interval 2011-2022
        # Extract question from data
        question = data['question']

        # Filter data for the question
        data_filtered = self.data[self.data['Question'] == question]
        data_filtered = data_filtered[(data_filtered['YearStart'] >= 2011) & (data_filtered['YearEnd'] <= 2022)]
        data_filtered = data_filtered.dropna(subset=['Data_Value'])

        # Compute the global mean of the data values
        global_mean = self.get_global_mean(data)
        global_mean = global_mean['Data_Value'].values[0]

        # Create dict with differences between the global mean and the state mean
        data_diff = data_filtered.groupby('LocationDesc')['Data_Value'].mean().reset_index()
        data_diff['Data_Value'] = global_mean - data_diff['Data_Value']

        # Write the results in results/ directory with the name of the job_id as json file
        self.json_writer(data_diff, job_id)

        self.job_maintainer.finish_job(job_id)

    def state_diff_from_mean(self, data, job_id):
        # Start job
        self.job_maintainer.start_job(job_id)

        # Computes the difference of the data values for the state from the global mean in the the interval 2011-2022
        # Extract question and state from data
        question = data['question']
        state = data['state']

        # Filter data for the question and state
        data_filtered = self.data[(self.data['Question'] == question) & (self.data['LocationDesc'] == state)]
        data_filtered = data_filtered[(data_filtered['YearStart'] >= 2011) & (data_filtered['YearEnd'] <= 2022)]
        data_filtered = data_filtered.dropna(subset=['Data_Value'])

        # Compute the global mean of the data values
        global_mean = self.get_global_mean(data)
        global_mean = global_mean['Data_Value'].values[0]

        # Create dict with differences between the global mean and the state mean
        data_diff = data_filtered['Data_Value'].mean()
        data_diff = global_mean - data_diff

        # Create a dict with a value state and the difference
        data_dict = {state: data_diff}
        with open(f'results/{job_id}.json', 'w') as f:
            # Write field:value pairs in json format
            json.dump(data_dict, f)

        self.job_maintainer.finish_job(job_id)

    def mean_by_category(self, data, job_id):
        # Start job
        self.job_maintainer.start_job(job_id)

        # Computes the mean of the data values for each category for each state in the the interval 2011-2022
        # Extract question from data
        question = data['question']

        # Filter data for the question
        data_filtered = self.data[self.data['Question'] == question]
        data_filtered = data_filtered[(data_filtered['YearStart'] >= 2011) & (data_filtered['YearEnd'] <= 2022)]
        data_filtered = data_filtered.dropna(subset=['Data_Value'])

        # Compute the mean of the data values for each state and category
        data_mean = data_filtered.groupby(['LocationDesc', 'StratificationCategory1', 'Stratification1'])['Data_Value'].mean().reset_index()

        # Prepare the result dictionary
        result = {}

        for _, row in data_mean.iterrows():
            key = f"('{row['LocationDesc']}', '{row['StratificationCategory1']}', '{row['Stratification1']}')"
            result[key] = row['Data_Value']

        # Save the dictionary as a JSON file in the specified path
        with open(f'results/{job_id}.json', 'w') as f:
            json.dump(result, f)

        self.job_maintainer.finish_job(job_id)

    def state_mean_by_category(self, data, job_id):
        # Start job
        self.job_maintainer.start_job(job_id)
        
        # Computes the mean of the data values for each category for the state in the the interval 2011-2022
        # Extract question and state from data
        question = data['question']
        state = data['state']

        # Filter data for the question and state
        data_filtered = self.data[(self.data['Question'] == question) & (self.data['LocationDesc'] == state)]
        data_filtered = data_filtered[(data_filtered['YearStart'] >= 2011) & (data_filtered['YearEnd'] <= 2022)]

        # Drop rows where 'Data_Value' is NaN because we cannot compute mean of NaN values
        data_filtered = data_filtered.dropna(subset=['Data_Value'])

        # Compute the mean of the data values for each category
        data_mean = data_filtered.groupby(['StratificationCategory1', 'Stratification1'])['Data_Value'].mean().reset_index()

        # Prepare the result dictionary
        result = {state: {}}
        for _, row in data_mean.iterrows():
            category_description = f"('{row['StratificationCategory1']}', '{row['Stratification1']}')"
            result[state][category_description] = row['Data_Value']

        # Save the dictionary as a JSON file in the specified path
        with open(f'results/{job_id}.json', 'w') as f:
            json.dump(result, f)

        self.job_maintainer.finish_job(job_id)
