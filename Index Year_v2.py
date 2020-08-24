# Index Year Program version 2
# This program is for calculating the index year for a given person.
# This program will take csv files as input.
# Last updated Augest 24, 2020

import pandas as pd
from pandas import DataFrame

main = pd.read_csv('BIOG_MAIN_BirthDeathYears_20200528_for index years cal.csv') # main data
degree = pd.read_csv('ENTRY YEARS_20200528_for index years cal.csv') # degree data
kinship = pd.read_csv('KIN DATA_20200528_for index years cal.csv') # kinship data

def index_year_dic(df): # main data will be used
  dic = {} # create an empty dictionary
  for i in df.index: # load all person id into the dic
    dic[df['c_personid'][i]] = -9999 # set initial value index year = -9999 for all
  return 
  
def personid_list(index_year_dic):
  return index_year_list.keys()

def gender_dic(df): # main data will be used
  dic = {} # create an empty dictionary
  for i in df.index: # load all person id into the dic
    if df['c_female'][i] == True: # female
      dic[df['c_personid'][i]] = 'female'
    elif df['c_female'][i] == False: # male
      dic[df['c_personid'][i]] = 'male'
  return dic

def birthyear_dic(df): # main data will be used
  dic = {} # create an empty dictionary
  for i in df.index: # load all person id into the dic
    if pd.isna(df['c_birthyear'][i]) != True and df['c_birthyear'][i] != 0: # check whether the birth year is known
      dic[df['c_personid'][i]] = int(df['c_birthyear'][i]) # load birth year into the dic
    else:
      dic[df['c_personid'][i]] = -9999 # set birth year = -9999 for those who birth year are unknown
  return dic

def deathyear_dic(df): # main data will be used
  dic = {} # create an empty dictionary
  for i in df.index: # load all person id into the dic
    if pd.isna(df['c_deathyear'][i]) != True and df['c_deathyear'][i] != 0: # check whether the death year is known
      dic[df['c_personid'][i]] = int(df['c_deathyear'][i]) # load death year into the dic
    else:
      dic[df['c_personid'][i]] = -9999 # set death year = -9999 for those who death year are unknown
  return dic

def death_age_dic(df): # main data will be used
  dic = {} # create an empty dictionary
  for i in df.index: # load all person id into the dic
    if pd.isna(df['c_death_age'][i]) != True and df['c_death_age'][i] != 0: # check whether the death age is known
      dic[df['c_personid'][i]] = int(df['c_death_age'][i]) # load death age into the dic
    else:
      dic[df['c_personid'][i]] = -9999 # set death age = -9999 for those who death age are unknown
  return dic

def children_dic(df): # kinship data will be used
  dic = {} # create an empty dictionary
  for i in df.index:
    list = []
    exist = True
    while exist = True:
      if df['c_kin_code'][i] == 182 or df['c_kin_code'][i] == 193 or df['c_kin_code'][i] == 327 or df['c_kin_code'][i] == 343 or df['c_kin_code'][i] == 176 or df['c_kin_code'][i] == 180:
        list.append(df['c_kin_id'][i])
      else:
        exist = False
    if len(list) > 0:
      dic[df['c_personid'][i]] = list
  return dic
    
def get_oldest_child(children_dic,personid):
  oldest_birth_year = 9999
  oldest_index_year = 9999
  if personid in children_dic:
    for i in children_dic[personid]:
      if birthyear_dic[i] != -9999:
        if birthyear_dic[i] < oldest_birth_year:
          oldest_birth_year = birthyear_dic[i] 
      if birthyear_dic[i] == -9999 and index_year_dic[i] != -9999:
        if index_year_dic[i] < oldest_index_year:
          oldest_index_year = index_year_dic[i]
  return oldest_birth_year,oldest_index_year    

def rule1and2(personid_list):
# Rule 1: index year = birth year
# Rule 2: index year = death year - death age
  for i in personid_list:
    if birthyear_dic[i] != -9999:
      index_year_dic[i] = birthyear_dic[i]
    elif birthyear_dic[i] == -9999:
      if deathyear_dic[i] != -9999 and death_age_dic[i] != -9999:
        index_year_dic[i] = deathyear_dic[i] - death_age_dic[i]

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

def rule9(df,children_dic): # kinship data will be used
# Rule 9:
  # for male: index year = oldest child's birth year - 30 
  # for female: index year = oldest child's birth year - 27
  for i in df.index:
    if index_year_dic[df['c_personid'][i]] == 0: # check whether the index year has been already calculated
      child_birthyear = get_oldest_child(children_dic,df['c_personid'][i])[0]
      if child_birthyear != 9999: # check whether oldest child's birth year is known
        if gender_dic[df['c_personid'][i]] = 'male' # male
          index_year_dic[df['c_personid'][i]] = (child_birthyear-30)
        elif gender_dic[df['c_personid'][i]] = 'female': # female
          index_year_dic[df['c_personid'][i]] = (child_birthyear-27)

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

def rule12(df): # kinship data will be used
# Rule 12: 
  # for male: index year = oldest son-in-law's birth year - 27
  # for female: index year = oldest son-in-law's birth year - 24
  for i in df.index:
    if index_year_dic[df['c_personid'][i]] == 0: # check whether the index year has been already calculated
      if df['c_kin_code'][i] == 332: # oldest son-in-law (first daughter's husband)
        if df['c_kin_id'][i] in birthyear_dic: # check whether oldest son-in-law's birth year is known
          if gender_dic[df['c_personid'][i]] == 'male': # male
            index_year_dic[df['c_personid'][i]] = (birthyear_dic[df['c_kin_id'][i]]-27)
          elif gender_dic[df['c_personid'][i]] == 'female': # female
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

def rule15(df,children_dic): # kinship data will be used
# Rule 15:
  # for male: index year = oldest child's index year - 30
  # for female: index year = oldest child's index year - 27
  for i in df.index:
    if index_year_dic[df['c_personid'][i]] == 0: # check whether the index year has been already calculated
      child_index_year = get_oldest_child(children_dic,df['c_personid'][i])[1]
      if child_index_year != 9999: # check whether oldest child's birth year is known
        if gender_dic[df['c_personid'][i]] = 'male' # male
          index_year_dic[df['c_personid'][i]] = (child_index_year-30)
        elif gender_dic[df['c_personid'][i]] = 'female': # female
          index_year_dic[df['c_personid'][i]] = (child_index_year-27)

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

def rule18(df): # kinship data will be used
# Rule 18: 
  # for male: index year = oldest son-in-law's index year - 27
  # for female: index year = oldest son-in-law's index year - 24
  for i in df.index:
    if index_year_dic[df['c_personid'][i]] == 0: # check whether the index year has been already calculated
      if df['c_kin_code'][i] == 332: # oldest son-in-law (first daughter's husband)
        if df['c_kin_id'][i] in index_year_dic: # check whether oldest son-in-law's index year has been already calculated
          if gender_dic[df['c_personid'][i]] == 'male': # male
            index_year_dic[df['c_personid'][i]] = (index_year_dic[df['c_kin_id'][i]]-27)
          elif gender_dic[df['c_personid'][i]] == 'female': # female
            index_year_dic[df['c_personid'][i]] = (index_year_dic[df['c_kin_id'][i]]-24)

def rule19(df): # kinship data will be used
# Rule 19: index year = grandfather's index year + 60
  for i in df.index:
    if index_year_dic[df['c_personid'][i]] == 0: # check whether the index year has been already calculated
      if df['c_kin_code'][i] == 62: # grandfather
        if df['c_kin_id'][i] in index_year_dic: # check whether grandfather's index year has been already calculated
          index_year_dic[df['c_personid'][i]] = (index_year_dic[df['c_kin_id'][i]]+60)

def rule20(personid_list):
# Rule 20:
  # for male: index year = death year - 63
  # for female: index year = death year - 55
  for i in personid_list:
    if index_year_dic[i] == 0: # check whether the index year has been already calculated
      if deathyear_dic[i] != -9999: # check whether the death year is known
        if gender_dic[i] == 'male': # male
          index_year_dic[i] = int(deathyear_dic[i]-63)
        elif gender_dic[i] == 'female': # female
          index_year_dic[i] = int(deathyear_dic[i]-55)

index_year_dic = index_year_dic(main)
gender_dic = gender_dic(main)
birthyear_dic = birthyear_dic(main)
deathyear_dic = deathyear_dic(main)
death_age_dic = death_age_dic(main)
personid_list = personid_list(index_year_dic)
children_dic = children_dic(kinship)
rule1and2(personid_list)
rule_degree(degree)
rule4(kinship)
rule8(kinship)
rule9(kinship,children_dic)
rule10(kinship)
rule11(kinship)
rule12(kinship)
rule13(kinship)
rule14(kinship)
rule15(kinship,children_dic)
rule16(kinship)
rule17(kinship)
rule18(kinship)
rule19(kinship)
rule20(personid_list)
df = DataFrame(list(index_year_dic.items()),columns=['c_personid','c_index_year'])
df.to_csv('output.csv',index=False)
