# Index Year Program version 1
# This program is for calculating the index year for a given person.
# This program will take csv files as input.
# Last updated July 7, 2020

import pandas as pd
from pandas import DataFrame

main = pd.read_csv('BIOG_MAIN_BirthDeathYears_20200528_for index years cal.csv') # main data
degree = pd.read_csv('ENTRY YEARS_20200528_for index years cal.csv') # degree data
kinship = pd.read_csv('KIN DATA_20200528_for index years cal.csv') # kinship data

def create_dic(df):
  dic = {} # create an empty dictionary
  for i in df.index:
    dic[df['c_personid'][i]] = 0 # set an initial value index year = 0 for all
  return dic

def get_oldest_child(df,personid):
  oldest_birth_year = 0
  oldest_child_id = 0
  for i in df.index:
    if df['c_personid'][i] == personid:
      if df['c_kin_code'][i] == 182 or df['c_kin_code'][i] == 193 or df['c_kin_code'][i] == 327 or df['c_kin_code'][i] == 343:
        if df['c_kin_id'][i] in birthyear_dic:
          if birthyear_dic[df['c_kin_id'][i]] > oldest_birth_year:
            oldest_birth_year = birthyear_dic[df['c_kin_id'][i]]
            oldest_child_id = df['c_kin_id'][i]
  if oldest_birth_year == 0:
    list = []
    for i in df.index:
      if df['c_personid'][i] == personid:
        if df['c_kin_code'][i] == 176 or df['c_kin_code'][i] == 180:
          list.append(df['c_kin_id'][i])
    for i in range (len(list)):
      if list[i] in birthyear_dic:
        if birthyear_dic[list[i]] > oldest_birth_year:
          oldest_birth_year = birthyear_dic[list[i]]
          oldest_child_id = [list][i]
  return oldest_birth_year,oldest_child_id

def rule1(df): # main data will be used
# Rule 1: index year = birth year
  for i in df.index:
    if pd.isna(df['c_birthyear'][i]) != True and df['c_birthyear'][i] != 0: # check whether the birth year is known
      index_year_dic[df['c_personid'][i]] = int(df['c_birthyear'][i])
      birthyear_dic[df['c_personid'][i]] = int(df['c_birthyear'][i])

def rule2(df): # main data will be used
# Rule 2: index year = death year - death age
  for i in df.index:
    if index_year_dic[df['c_personid'][i]] == 0: # check whether the index year has been already calculated
      if pd.isna(df['c_deathyear'][i]) != True and df['c_deathyear'][i] != 0: # check whether the death year is known
        if pd.isna(df['c_death_age'][i]) != True and df['c_death_age'][i] != 0: # check whether the death age is known
          index_year_dic[df['c_personid'][i]] = int(df['c_deathyear'][i])-int(df['c_death_age'][i])

def rule_degree(df): # degree data will be used
# Rule 5 (for male): index year = the year obtained the Jinshi - 30
# Rule 6 (for male): index year = the year obtained the Juren - 27
# Rule 7 (for male): index year = the year obtained the Xiucai - 21
  for i in df.index:
    if index_year_dic[df['c_personid'][i]] == 0: # check whether the index year has been already calculated
      if df['c_entry_code'][i] == 36 or df['c_entry_code'][i] == 37 or df['c_entry_code'][i] == 124 or df['c_entry_code'][i] == 165: # Jinshi
        index_year_dic[df['c_personid'][i]] = (df['c_year'][i]-30)
      elif df['c_entry_code'][i] == 34 or df['c_entry_code'][i] == 39: # Juren
        index_year_dic[df['c_personid'][i]] = (df['c_year'][i]-27)
      elif df['c_entry_code'][i] == 47 or df['c_entry_code'][i] == 173: # Xiucai
        index_year_dic[df['c_personid'][i]] = (df['c_year'][i]-21)

def rule4(df): # kinship data will be used
# Rule 4W (for female): index year = husband's birth year + 3
# Rule 5W-7W are also included in this function since all degree information has already been checked at this point
  for i in df.index:
    if index_year_dic[df['c_personid'][i]] == 0: # check whether the index year has been already calculated
      if df['c_kin_code'][i] == 134: # husband
        if df['c_kin_id'][i] in birthyear_dic: # Rule 4W
          index_year_dic[df['c_personid'][i]] = (birthyear_dic[df['c_kin_id'][i]]+3)
        elif df['c_kin_id'][i] in index_year_dic: # Rule 5W-7W
          index_year_dic[df['c_personid'][i]] = (index_year_dic[df['c_kin_id'][i]]+3)

def rule8(df): # kinship data will be used
# Rule 8: index year = father's birth year + 30
  for i in df.index:
    if index_year_dic[df['c_personid'][i]] == 0: # check whether the index year has been already calculated
      if df['c_kin_code'][i] == 75: # father
        if df['c_kin_id'][i] in birthyear_dic: # check whether father's birth year is known
          index_year_dic[df['c_personid'][i]] = (birthyear_dic[df['c_kin_id'][i]]+30)

def rule9(df,main): # kinship data will be used
# Rule 9:
  # for male: index year = oldest child's birth year - 30 
  # for female: index year = oldest child's birth year - 27
  for i in main.index:
    if index_year_dic[main['c_personid'][i]] == 0: # check whether the index year has been already calculated
      child = get_oldest_child(df,main['c_personid'][i])[0]
      if child != 0: # check whether oldest child's birth year is known
        if main['c_female'] == False: # male
          index_year_dic[df['c_personid'][i]] = (child-30)
        elif main['c_female'] == True: # female
          index_year_dic[df['c_personid'][i]] = (child-27)

def rule10(df): # kinship data will be used
# Rule 10: index year = elder brother's birth year + 2
  for i in df.index:
    if index_year_dic[df['c_personid'][i]] == 0: # check whether the index year has been already calculated
      if df['c_kin_code'][i] == 125: # elder brother
        if df['c_kin_id'][i] in birthyear_dic: # check whether elder brother's birth year is known
          index_year_dic[df['c_personid'][i]] = (birthyear_dic[df['c_kin_id'][i]]+2)

def rule11(df): # kinship data will be used
# Rule 11: index year = younger brother's birth year - 2
  for i in df.index:
    if index_year_dic[df['c_personid'][i]] == 0: # check whether the index year has been already calculated
      if df['c_kin_code'][i] == 126: # younger brother
        if df['c_kin_id'][i] in birthyear_dic: # check whether younger brother's birth year is known
          index_year_dic[df['c_personid'][i]] = (birthyear_dic[df['c_kin_id'][i]]-2)

def rule12(df,main): # kinship data will be used
# Rule 12: 
  # for male: index year = oldest son-in-law's birth year - 27
  # for female: index year = oldest son-in-law's birth year - 24
  for i in df.index:
    if index_year_dic[df['c_personid'][i]] == 0: # check whether the index year has been already calculated
      if df['c_kin_code'][i] == 332: # oldest son-in-law (first daughter's husband)
        if df['c_kin_id'][i] in birthyear_dic: # check whether oldest son-in-law's birth year is known
          if main['c_female'][df[main['c_personid'].isin([df['c_personid'][i]])].index[0]] == False: # male
            index_year_dic[df['c_personid'][i]] = (birthyear_dic[df['c_kin_id'][i]]-27)
          elif main['c_female'][df[main['c_personid'].isin([df['c_personid'][i]])].index[0]] == True: # female
            index_year_dic[df['c_personid'][i]] = (birthyear_dic[df['c_kin_id'][i]]-24)

def rule13(df): # kinship data will be used
# Rule 13: index year = grandfather's birth year + 60
  for i in df.index:
    if index_year_dic[df['c_personid'][i]] == 0: # check whether the index year has been already calculated
      if df['c_kin_code'][i] == 62: # grandfather
        if df['c_kin_id'][i] in birthyear_dic: # check whether grandfather's birth year is known
          index_year_dic[df['c_personid'][i]] = (birthyear_dic[df['c_kin_id'][i]]+60)

def rule14(df): # kinship data will be used
# Rule 14: index year = father's index year + 30
  for i in df.index:
    if index_year_dic[df['c_personid'][i]] == 0: # check whether the index year has been already calculated
      if df['c_kin_code'][i] == 75: # father
        if df['c_kin_id'][i] in index_year_dic: # check whether father's index year has been already calculated
          index_year_dic[df['c_personid'][i]] = (index_year_dic[df['c_kin_id'][i]]+30)

def rule15(df,main): # kinship data will be used
# Rule 15:
  # for male: index year = oldest child's index year - 30 
  # for female: index year = oldest child's index year - 27
  for i in main.index:
    if index_year_dic[main['c_personid'][i]] == 0: # check whether the index year has been already calculated
      child_id = get_oldest_child(df,main['c_personid'][i])[1]
      child = index_year_dic[child_id]
      if child != 0: # check whether oldest child's index year has been already calculated
        if main['c_female'] == False: # male
          index_year_dic[df['c_personid'][i]] = (child-30)
        elif main['c_female'] == True: # female
          index_year_dic[df['c_personid'][i]] = (child-27)

def rule16(df): # kinship data will be used
# Rule 16: index year = elder brother's index year + 2
  for i in df.index:
    if index_year_dic[df['c_personid'][i]] == 0: # check whether the index year has been already calculated
      if df['c_kin_code'][i] == 125: # elder brother
        if df['c_kin_id'][i] in index_year_dic: # check whether elder brother's index year has been already calculated
          index_year_dic[df['c_personid'][i]] = (index_year_dic[df['c_kin_id'][i]]+2)

def rule17(df): # kinship data will be used
# Rule 17: index year = younger brother's index year - 2
  for i in df.index:
    if index_year_dic[df['c_personid'][i]] == 0: # check whether the index year has been already calculated
      if df['c_kin_code'][i] == 126: # younger brother
        if df['c_kin_id'][i] in index_year_dic: # check whether younger brother's index year has been already calculated
          index_year_dic[df['c_personid'][i]] = (index_year_dic[df['c_kin_id'][i]]-2)

def rule18(df,main): # kinship data will be used
# Rule 18: 
  # for male: index year = oldest son-in-law's index year - 27
  # for female: index year = oldest son-in-law's index year - 24
  for i in df.index:
    if index_year_dic[df['c_personid'][i]] == 0: # check whether the index year has been already calculated
      if df['c_kin_code'][i] == 332: # oldest son-in-law (first daughter's husband)
        if df['c_kin_id'][i] in index_year_dic: # check whether oldest son-in-law's index year has been already calculated
          if main['c_female'][df[main['c_personid'].isin([df['c_personid'][i]])].index[0]] == False: # male
            index_year_dic[df['c_personid'][i]] = (index_year_dic[df['c_kin_id'][i]]-27)
          elif main['c_female'][df[main['c_personid'].isin([df['c_personid'][i]])].index[0]] == True: # female
            index_year_dic[df['c_personid'][i]] = (index_year_dic[df['c_kin_id'][i]]-24)

def rule19(df): # kinship data will be used
# Rule 19: index year = grandfather's index year + 60
  for i in df.index:
    if index_year_dic[df['c_personid'][i]] == 0: # check whether the index year has been already calculated
      if df['c_kin_code'][i] == 62: # grandfather
        if df['c_kin_id'][i] in index_year_dic: # check whether grandfather's index year has been already calculated
          index_year_dic[df['c_personid'][i]] = (index_year_dic[df['c_kin_id'][i]]+60)

def rule20(df): # main data will be used
# Rule 20:
  # for male: index year = death year - 63
  # for female: index year = death year - 55
  for i in df.index:
    if index_year_dic[df['c_personid'][i]] == 0: # check whether the index year has been already calculated
      if pd.isna(df['c_deathyear'][i]) != True and df['c_deathyear'][i] != 0: # check whether the death year is known
        if df['c_female'][i] == False: # male
          index_year_dic[df['c_personid'][i]] = int(df['c_deathyear'][i]-63)
        elif df['c_female'][i] == True: # female
          index_year_dic[df['c_personid'][i]] = int(df['c_deathyear'][i]-55)
        
index_year_dic = create_dic(main)
birthyear_dic = {}
rule1(main)
rule2(main)
rule_degree(degree)
rule4(kinship)
rule8(kinship)
rule9(kinship,main)
rule10(kinship)
rule11(kinship)
rule12(kinship,main)
rule13(kinship)
rule14(kinship)
rule15(kinship,main)
rule16(kinship)
rule17(kinship)
rule18(kinship,main)
rule19(kinship)
rule20(main)
df = DataFrame(list(index_year_dic.items()),columns=['c_personid','c_index_year'])
df.to_csv('output.csv',index=False)
