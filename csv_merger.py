
# Useful librairies
import os
import glob
import pandas as pd
import promptlib


extension = "csv"
#Prompt directory in which all files were downloaded, so that all downloaded files can be merged
prompter = promptlib.Files()
#Set working directory to chosen directory
dir = prompter.dir()

#Data cleaning
# Select stations with enough data (doing a missing values analysis)
def available_data_per_pollutant(df):
	if set(['Date de début', 'Date de fin', 'Organisme', 'code zas']).issubset(df.columns):
		df.drop(columns=['Date de début', 'Date de fin', 'Organisme', 'code zas'], axis=1, inplace=True)

	NO2_percent = (df['NO2'] / df['code site']) * 100
	O3_percent = (df['O3'] / df['code site']) * 100
	PM10_percent = (df['PM10'] / df['code site']) * 100
	PM25_percent = (df['PM2.5'] / df['code site']) * 100
	SO2_percent = (df['SO2'] / df['code site']) * 100

	polluant_data_available = pd.concat([NO2_percent, O3_percent, PM10_percent, PM25_percent, SO2_percent], axis=1)
	polluant_data_available = polluant_data_available.rename(
		columns={0: 'NO2', 1: 'O3', 2: 'PM10', 3: 'PM2.5', 4: 'SO2'})

	return polluant_data_available.round(2)





#Function to merge csv files
def csv_merge(dir,extension):
    #Create a directory, cut and paste all the csv files there and put the file path instead "directory_name"
    os.chdir(dir)

    dfs = []
    #Get list of all csv files
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

    #combine all files in the list
    #df = pd.concat([pd.read_csv(f,encoding='latin-1',sep=";") for f in all_filenames ])
    #Read all csv files as pandas dataframe and concatenate them
    for f in all_filenames:
        df = pd.read_csv(f, encoding='utf-8-sig')
        # take the data less the header row
        # df.columns = new_header  # set the header row as the df header
        df = df.iloc[1:]
        dfs.append(df)
    #final concantenated dataframe of all csv files
    df = pd.concat(dfs)
    #Convert concentration variable 'valeur' to float
    df["valeur"] = pd.to_numeric(df["valeur"], downcast="float")
    #Since pollutants are in columns entries, so they repeat themselves, this takes a lot of space
    #So dataframe is pivoted, so that each pollutant has a column
    df = pd.pivot_table(df,
                         values='valeur',
                         index=['Date de début','code site', 'nom site'],
                         columns='Polluant'
                         )
    #Drop unregulated pollutants
    df.drop(columns=['C6H6', 'CO', 'NO', 'NOX as NO2'], axis=1, inplace=True)


    df[df["SO2"] < 0] = 0
    df[df["PM2.5"] < 0] = 0
    df[df["PM10"] < 0] = 0
    df[df["O3"] < 0] = 0
    df[df["NO2"] < 0] = 0

    df.reset_index(inplace=True)

    #convert concatenated dataframe to csv in same directory as all downloaded csv files
    df.to_csv("App_ds_2021.csv", encoding='utf-8-sig',index=False)

csv_merge(dir,extension)

df = pd.read_csv('App_ds_2021.csv')
df_halles = df[df['nom site'] == 'PARIS 1er Les Halles']
df_halles.to_csv('App_ds_2021_halles.csv', index=False)