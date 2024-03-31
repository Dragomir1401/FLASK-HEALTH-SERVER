import os
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

 