"""This module is responsible for reading the csv file and returning the data as a
pandas dataframe"""
import os
import pandas as pd

class DataIngestor:
    """This class reads the csv file and returns the data as a pandas dataframe"""
    def __init__(self, csv_path: str):
        """Read the csv file and return the data as a pandas dataframe"""
        # The csv has the following columns:
        # YearStart,YearEnd, LocationAbbr, LocationDesc, Datasource, Class, Topic, Question,
        # Data_Value_Unit,Data_Value_Type,Data_Value,
        # Data_Value_Alt, Data_Value_Footnote_Symbol, Data_Value_Footnote, Low_Confidence_Limit,
        # High_Confidence_Limit, Sample_Size,Total,
        # Age(years), Education, Gender, Income, Race/Ethnicity, GeoLocation, ClassID, TopicID,
        # QuestionID, DataValueTypeID, LocationID,
        # StratificationCategory1, Stratification1, StratificationCategoryId1, StratificationID1
        # Create the results directory if it does not exist
        if not os.path.exists('results'):
            os.makedirs('results')

        if csv_path:
            self.data = pd.read_csv(csv_path)
        else:
            self.data = None

    def read_test_csv(self, csv_path: str):
        """Read the csv file and return the data as a pandas dataframe"""
        self.data = pd.read_csv(csv_path)
        return self.data

    def get(self):
        """Return the data"""
        return self.data
 