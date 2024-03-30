import os
import json
import csv
import pandas as pd

class DataIngestor:
    def __init__(self, csv_path: str):
        # TODO: Read csv from csv_path
        # The csv has the following columns:
        # YearStart,YearEnd, LocationAbbr, LocationDesc, Datasource, Class, Topic, Question, Data_Value_Unit,Data_Value_Type,Data_Value,
        # Data_Value_Alt, Data_Value_Footnote_Symbol, Data_Value_Footnote, Low_Confidence_Limit, High_Confidence_Limit, Sample_Size,Total,
        # Age(years), Education, Gender, Income, Race/Ethnicity, GeoLocation, ClassID, TopicID, QuestionID, DataValueTypeID, LocationID,
        # StratificationCategory1, Stratification1, StratificationCategoryId1, StratificationID1

        # Create the results directory if it does not exist
        if not os.path.exists('results'):
            os.makedirs('results')

        self.data = pd.read_csv(csv_path)
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
        # Save the results in results/ directory with the name of the job_id as json file  
        # Format as "State": Value
        # Eliminate LocationDesc and Data_Value column names    
        data_mean = data_mean.to_dict(orient='records')
        data_mean = {item['LocationDesc']: item['Data_Value'] for item in data_mean}
        with open(f"results/{job_id}.json", 'w') as f:
            json.dump(data_mean, f)

    def states_mean(self, data, job_id):
        # Computes the mean of the data values for each state in the the interval 2011-2022 and orders ascendingly by mean
        # Extract question from data
        question = data['question']
        best_is_min = False
        if question in self.questions_best_is_min:
            best_is_min = True

        # Filter data for the question
        data_filtered = self.data[self.data['Question'] == question]
        data_filtered = data_filtered[(data_filtered['YearStart'] >= 2011) & (data_filtered['YearEnd'] <= 2022)]

        # Compute the mean of the data values for each state
        data_mean = data_filtered.groupby('LocationDesc')['Data_Value'].mean().reset_index()   
        data_mean = data_mean.sort_values('Data_Value', ascending=best_is_min)

       

    def state_mean(self, data, job_id):
        # Computes the mean of the data values for the state in the the interval 2011-2022
        # Extract question and state from data
        question = data['question']
        state = data['state']

        # Filter data for the question and state
        data_filtered = self.data[(self.data['Question'] == question) & (self.data['LocationDesc'] == state)]
        data_filtered = data_filtered[(data_filtered['YearStart'] >= 2011) & (data_filtered['YearEnd'] <= 2022)]

        # Compute the mean of the data values for the state
        data_mean = data_filtered['Data_Value'].mean()

        # Save the results in results/ directory with the name of the job_id as json file  
        # Format as "State": Value
        # Eliminate LocationDesc and Data_Value column names    
        data_mean = data_mean.to_dict(orient='records')
        data_mean = {item['LocationDesc']: item['Data_Value'] for item in data_mean}
        with open(f"results/{job_id}.json", 'w') as f:
            json.dump(data_mean, f)