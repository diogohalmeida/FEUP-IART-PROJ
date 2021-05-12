import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

ten_k_fillings_data = pd.read_csv('10_k_fillings.csv')
ten_k_fillings_data.rename(columns={'Unnamed: 0':'Company'}, inplace=True)
#ten_k_fillings_data.head()

variation_data = pd.read_csv('price_variation.csv')
variation_data.rename(columns={'Unnamed: 0':'Company'}, inplace=True)
#variation_data.head()

full_data = pd.merge(ten_k_fillings_data, variation_data, on='Company', how='inner')


sb.pairplot(full_data, hue='class')

#full_data.describe()