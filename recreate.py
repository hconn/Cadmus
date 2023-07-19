import numpy as np
import pandas as pd
from scipy.stats import zscore
from scipy.stats import boxcox 
import scipy.special as sc

data = pd.read_csv(r'C:\Users\HConner\Downloads\CAT Data and Code (from client)\CAT Data and Code (from client)\Data\Query2_County Data.csv')
metric = pd.read_csv(r'C:\Users\HConner\Downloads\CAT Data and Code (from client)\CAT Data and Code (from client)\Data\Metric Information Table.csv', header=[0])
metric_transformations = pd.read_csv(r'C:\Users\HConner\Downloads\CAT Data and Code (from client)\CAT Data and Code (from client)\Code\cat_metric_transformations.csv')
data.columns.to_list()

metric_information_table = pd.read_csv(r'C:\Users\HConner\Downloads\CAT Data and Code (from client)\CAT Data and Code (from client)\Code\cat_metric_information.csv')


# box cox transformation
box_cox_transformation_variables = metric[metric['Data Transformation'] == 'Box-Cox-Adjusted Z-Score'].reset_index(drop=True)

box_cox_transformation_variables['Scaling Factor'].unique()
# all box cox transformation have same coefficient for pre and post deployment
box_cox_transformation_variables.filter(regex='Importance')

box_cox_tranformed, h = boxcox(data['population_below_100_pct_poverty_level'])
    
box_cox_zscore_trnsfrmd = zscore(box_cox_tranformed, nan_policy='omit')
np.argwhere(np.isnan(box_cox_zscore_trnsfrmd))
np.nanmax(box_cox_zscore_trnsfrmd)
box_cox_zscore = 
# this happens later 
# #box_cox_zscore_trnsfrmd_scaled = box_cox_zscore_trnsfrmd * 0.056 #importance coeffienct
# np.nanmax(box_cox_zscore_trnsfrmd_scaled)

#percentile transformation
percentile_tranformations = metric[metric['Data Transformation'] == 'Percentile'].reset_index(drop=True)
data.percentage_of_minority_population.rank(pct = True)


data = pd.read_csv(r'C:\Users\HConner\Downloads\CAT Data and Code (from client)\CAT Data and Code (from client)\Data\Query2_County Data.csv')
metric = pd.read_csv(r'C:\Users\HConner\Downloads\CAT Data and Code (from client)\CAT Data and Code (from client)\Data\Metric Information Table.csv', header=[0])
metric_transformations = pd.read_csv(r'C:\Users\HConner\Downloads\CAT Data and Code (from client)\CAT Data and Code (from client)\Code\cat_metric_transformations.csv')
####################################################################
# data transformation
####################################################################
# column names do not match for the metric table and the data
# Have not incorporated the IA data yet so looping through the columns that map to the county data table only
map_column_names = pd.read_csv(r'C:\Users\HConner\Downloads\CAT Data and Code (from client)\Data for transformation\mapping_column_names.csv')
# Loop through all data columns for transformation
for data_col in map_column_names['data_col_names']:
    #find the column name in the metric table
    metric_col = map_column_names[map_column_names['data_col_names']==data_col]['metric_col_names'].iloc[0]
    # find transformation
    transformation = metric_information_table[metric_information_table['metric']==metric_col]['data_transformation'].iloc[0]
    # transform data dependent on tranformation
    if transformation == 'box_cox':
        # box cox
        # second variable is not used, value used to fit data to normal distribution
        # find lambda for transformation
        # can't use this function with 0 values
        __, h  = boxcox(data[data[data_col]>0][data_col])
        # use lambda in this function to transform all data
        data[data_col] = sc.boxcox(data[data_col], h)
        # z score
        # need to omit nan or entire column is nan
        data[data_col] = zscore(data[data_col], nan_policy='omit')
        # mulitply by scaling factor
        data[data_col] = data[data_col] * metric_information_table[metric_information_table['metric']==metric_col]['scaling_factor'].iloc[0]
        # add centering constant
        data[data_col] = data[data_col] + metric_information_table[metric_information_table['metric']==metric_col]['centering_constant'].iloc[0]
        # limit upper and lower range
        data[data_col] = data[data_col].clip(-2, 2)
        
    # percentile
    elif transformation == 'percentile':
        data[data_col] = data[data_col].rank(pct = True)
        
    # If the data does not have one of these transformations it does not get transformded
