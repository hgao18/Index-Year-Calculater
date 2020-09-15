# Index Year Program version 3
# This program is for calculating the index year for every given person
# This program will take csv files as input
# Last updated September 14, 2020

import pandas as pd
from pandas import DataFrame

def index_year_dict_func(df): # main data will be used
    dic = {} # create an empty dictionary
    for i in df.index: # load all person id into the dict
        dic[df['c_personid'][i]] = -9999 # set default value index year = -9999 for all
    return dic

def personid_list_func(index_year_dict):
    personid_list = list(index_year_dict.keys())
    return personid_list

def gender_dict_func(df): # main data will be used
    dic = {} # create an empty dictionary
    for i in df.index: # load all person id into the dict
        if df['c_female'][i] == True: # female
            dic[df['c_personid'][i]] = 'female'
        elif df['c_female'][i] == False: # male
            dic[df['c_personid'][i]] = 'male'
    return dic

def birthyear_dict_func(df): # main data will be used
    dic = {} # create an empty dictionary
    for i in df.index: # load all person id into the dict
        if pd.isna(df['c_birthyear'][i]) != True and df['c_birthyear'][i] != 0: # check whether the birth year is known
            dic[df['c_personid'][i]] = int(df['c_birthyear'][i]) # load birth year into the dict
    return dic

def deathyear_dict_func(df): # main data will be used
    dic = {} # create an empty dictionary
    for i in df.index: # load all person id into the dict
        if pd.isna(df['c_deathyear'][i]) != True and df['c_deathyear'][i] != 0: # check whether the death year is known
            dic[df['c_personid'][i]] = int(df['c_deathyear'][i]) # load death year into the dict
    return dic

def death_age_dict_func(df): # main data will be used
    dic = {} # create an empty dictionary
    for i in df.index: # load all person id into the dict
        if pd.isna(df['c_death_age'][i]) != True and df['c_death_age'][i] != 0: # check whether the death age is known
            dic[df['c_personid'][i]] = int(df['c_death_age'][i]) # load death age into the dict
    return dic

def children_dict_func(df): # kinship data will be used
    dic = {} # create an empty dictionary
    for i in personid_list:
        dic[i] = [] # create an empty list for every person to load their children's person id (if any)
    for i in df.index:
        if df['c_kin_code'][i] == 182 or df['c_kin_code'][i] == 193 or df['c_kin_code'][i] == 327 or df['c_kin_code'][i] == 343 or df['c_kin_code'][i] == 176 or df['c_kin_code'][i] == 180:
                dic[df['c_personid'][i]].append(df['c_kin_id'][i])
    return dic

def get_oldest_child(personid): # children_dict will be used
# This function will return the oldest birth year & index year among one's children
    oldest_birth_year = 9999 # default value
    oldest_index_year = 9999 # default value
    children_list = children_dict[personid] # for each person, get their children's person id from the dict
    if children_list != []: # check whether the person has any child
        for i in children_list: # for every children of this given person
            if i in birthyear_dict: # for the child's birth year is known
                if birthyear_dict[i] < oldest_birth_year: # compare the birth year with the oldest birth year
                    oldest_birth_year = birthyear_dict[i]
            elif i not in birthyear_dict and index_year_dict[i] != -9999: # for the child's birth year is not known, but the index year is known
                if index_year_dict[i] < oldest_index_year:
                    oldest_index_year = index_year_dict[i]
    return oldest_birth_year,oldest_index_year

def rule1and2(personid_list):
# Rule 1: index year = birth year
# Rule 2: index year = death year - death age
    for i in personid_list:
        if i in birthyear_dict: # if birth year is known
            index_year_dict[i] = birthyear_dict[i]
        else: # if birth year is unknown
            if i in deathyear_dict and i in death_age_dict: # if both death year and death age are known
                index_year_dict[i] = deathyear_dict[i] - death_age_dict[i]
                
def rule_degree(df): # degree data will be used
# Rule 5 (for male): index year = the year obtained the Jinshi - 30
# Rule 6 (for male): index year = the year obtained the Juren - 27
# Rule 7 (for male): index year = the year obtained the Xiucai - 21
    for i in df.index:
        if index_year_dict[df['c_personid'][i]] == -9999: # check whether the index year has been already calculated
            if df['c_entry_code'][i] == 36 or df['c_entry_code'][i] == 37 or df['c_entry_code'][i] == 124 or df['c_entry_code'][i] == 165: # Jinshi
                index_year_dict[df['c_personid'][i]] = (df['c_year'][i]-30)
            elif df['c_entry_code'][i] == 34 or df['c_entry_code'][i] == 39: # Juren
                index_year_dict[df['c_personid'][i]] = (df['c_year'][i]-27)
            elif df['c_entry_code'][i] == 47 or df['c_entry_code'][i] == 173: # Xiucai
                index_year_dict[df['c_personid'][i]] = (df['c_year'][i]-21)
                
def rule4(df): # kinship data will be used
# Rule 4W (for female): index year = husband's birth year + 3
# Rule 5W-7W are also included in this function since all degree information has already been checked at this point
    for i in df.index:
        if index_year_dict[df['c_personid'][i]] == -9999: # check whether the index year has been already calculated
            if df['c_kin_code'][i] == 134: # husband
                if df['c_kin_id'][i] in birthyear_dict: # Rule 4W
                    index_year_dict[df['c_personid'][i]] = (birthyear_dict[df['c_kin_id'][i]]+3)
                elif df['c_kin_id'][i] in index_year_dict: # Rule 5W-7W
                    index_year_dict[df['c_personid'][i]] = (index_year_dict[df['c_kin_id'][i]]+3)

def rule8(df): # kinship data will be used
# Rule 8: index year = father's birth year + 30
    for i in df.index:
        if index_year_dict[df['c_personid'][i]] == -9999: # check whether the index year has been already calculated
            if df['c_kin_code'][i] == 75: # father
                if df['c_kin_id'][i] in birthyear_dict: # check whether father's birth year is known
                    index_year_dict[df['c_personid'][i]] = (birthyear_dict[df['c_kin_id'][i]]+30)

def rule9(df): # kinship data will be used
# Rule 9:
    # for male: index year = oldest child's birth year - 30
    # for female: index year = oldest child's birth year - 27
    for i in df.index:
        if index_year_dict[df['c_personid'][i]] == -9999: # check whether the index year has been already calculated
            child_birthyear = get_oldest_child(df['c_personid'][i])[0]
            if child_birthyear != 9999: # check whether oldest child's birth year is known
                if gender_dict[df['c_personid'][i]] == 'male': # male
                    index_year_dict[df['c_personid'][i]] = (child_birthyear-30)
                elif gender_dict[df['c_personid'][i]] == 'female': # female
                    index_year_dict[df['c_personid'][i]] = (child_birthyear-27)

def rule10(df): # kinship data will be used
# Rule 10: index year = elder brother's birth year + 2
    for i in df.index:
        if index_year_dict[df['c_personid'][i]] == -9999: # check whether the index year has been already calculated
            if df['c_kin_code'][i] == 125: # elder brother
                if df['c_kin_id'][i] in birthyear_dict: # check whether elder brother's birth year is known
                    index_year_dict[df['c_personid'][i]] = (birthyear_dict[df['c_kin_id'][i]]+2)

def rule11(df): # kinship data will be used
# Rule 11: index year = younger brother's birth year - 2
    for i in df.index:
        if index_year_dict[df['c_personid'][i]] == -9999: # check whether the index year has been already calculated
            if df['c_kin_code'][i] == 126: # younger brother
                if df['c_kin_id'][i] in birthyear_dict: # check whether younger brother's birth year is known
                    index_year_dict[df['c_personid'][i]] = (birthyear_dict[df['c_kin_id'][i]]-2)

def rule12(df): # kinship data will be used
# Rule 12: 
    # for male: index year = oldest son-in-law's birth year - 27
    # for female: index year = oldest son-in-law's birth year - 24
    for i in df.index:
        if index_year_dict[df['c_personid'][i]] == -9999: # check whether the index year has been already calculated
            if df['c_kin_code'][i] == 332: # oldest son-in-law (first daughter's husband)
                if df['c_kin_id'][i] in birthyear_dict: # check whether oldest son-in-law's birth year is known
                    if gender_dict[df['c_personid'][i]] == 'male': # male
                        index_year_dict[df['c_personid'][i]] = (birthyear_dict[df['c_kin_id'][i]]-27)
                    elif gender_dict[df['c_personid'][i]] == 'female': # female
                        index_year_dict[df['c_personid'][i]] = (birthyear_dict[df['c_kin_id'][i]]-24)

def rule13(df): # kinship data will be used
# Rule 13: index year = grandfather's birth year + 60
    for i in df.index:
        if index_year_dict[df['c_personid'][i]] == -9999: # check whether the index year has been already calculated
            if df['c_kin_code'][i] == 62: # grandfather
                if df['c_kin_id'][i] in birthyear_dict: # check whether grandfather's birth year is known
                    index_year_dict[df['c_personid'][i]] = (birthyear_dict[df['c_kin_id'][i]]+60)

def rule14(df): # kinship data will be used
# Rule 14: index year = father's index year + 30
    for i in df.index:
        if index_year_dict[df['c_personid'][i]] == -9999: # check whether the index year has been already calculated
            if df['c_kin_code'][i] == 75: # father
                if index_year_dict[df['c_kin_id'][i]] != -9999: # check whether father's index year has been already calculated\n",
                    index_year_dict[df['c_personid'][i]] = (index_year_dict[df['c_kin_id'][i]]+30)

def rule15(df): # kinship data will be used
# Rule 15:
    # for male: index year = oldest child's index year - 30
    # for female: index year = oldest child's index year - 27
    for i in df.index:
        if index_year_dict[df['c_personid'][i]] == -9999: # check whether the index year has been already calculated
            child_index_year = get_oldest_child(df['c_personid'][i])[1]
            if child_index_year != 9999: # check whether oldest child's birth year is known
                if gender_dict[df['c_personid'][i]] == 'male': # male
                    index_year_dict[df['c_personid'][i]] = (child_index_year-30)
                elif gender_dict[df['c_personid'][i]] == 'female': # female
                    index_year_dict[df['c_personid'][i]] = (child_index_year-27)

def rule16(df): # kinship data will be used
# Rule 16: index year = elder brother's index year + 2
    for i in df.index:
        if index_year_dict[df['c_personid'][i]] == -9999: # check whether the index year has been already calculated
            if df['c_kin_code'][i] == 125: # elder brother
                if index_year_dict[df['c_kin_id'][i]] != -9999: # check whether elder brother's index year has been already calculated
                    index_year_dict[df['c_personid'][i]] = (index_year_dict[df['c_kin_id'][i]]+2)

def rule17(df): # kinship data will be used
# Rule 17: index year = younger brother's index year - 2
    for i in df.index:
        if index_year_dict[df['c_personid'][i]] == -9999: # check whether the index year has been already calculated
            if df['c_kin_code'][i] == 126: # younger brother
                if index_year_dict[df['c_kin_id'][i]] != -9999: # check whether younger brother's index year has been already calculated
                    index_year_dict[df['c_personid'][i]] = (index_year_dict[df['c_kin_id'][i]]-2)

def rule18(df): # kinship data will be used
# Rule 18:
    # for male: index year = oldest son-in-law's index year - 27
    # for female: index year = oldest son-in-law's index year - 24
    for i in df.index:
        if index_year_dict[df['c_personid'][i]] == -9999: # check whether the index year has been already calculated
            if df['c_kin_code'][i] == 332: # oldest son-in-law (first daughter's husband)
                if index_year_dict[df['c_kin_id'][i]] != -9999: # check whether oldest son-in-law's index year has been already calculated
                    if gender_dict[df['c_personid'][i]] == 'male': # male
                        index_year_dict[df['c_personid'][i]] = (index_year_dict[df['c_kin_id'][i]]-27)
                    elif gender_dict[df['c_personid'][i]] == 'female': # female
                        index_year_dict[df['c_personid'][i]] = (index_year_dict[df['c_kin_id'][i]]-24)

def rule19(df): # kinship data will be used
# Rule 19: index year = grandfather's index year + 60
    for i in df.index:
        if index_year_dict[df['c_personid'][i]] == -9999: # check whether the index year has been already calculated
            if df['c_kin_code'][i] == 62: # grandfather
                if index_year_dict[df['c_kin_id'][i]] != -9999: # check whether grandfather's index year has been already calculated
                    index_year_dict[df['c_personid'][i]] = (index_year_dict[df['c_kin_id'][i]]+60)

def rule20(personid_list):
# Rule 20:
    # for male: index year = death year - 63
    # for female: index year = death year - 55
    for i in personid_list:
        if index_year_dict[i] == -9999: # check whether the index year has been already calculated
            if i in deathyear_dict: # check whether the death year is known
                if gender_dict[i] == 'male': # male
                    index_year_dict[i] = int(deathyear_dict[i]-63)
                elif gender_dict[i] == 'female': # female
                    index_year_dict[i] = int(deathyear_dict[i]-55)

main = pd.read_csv('BIOG_MAIN_BirthDeathYears_20200528_for index years cal.csv') # main data
degree = pd.read_csv('ENTRY YEARS_20200528_for index years cal.csv') # degree data
kinship = pd.read_csv('KIN DATA_20200528_for index years cal.csv') # kinship data

index_year_dict = index_year_dict_func(main)
print("index_year_dict created.")
gender_dict = gender_dict_func(main)
print("gender_dict created.")
birthyear_dict = birthyear_dict_func(main)
print("birthyear_dict created.")
deathyear_dict = deathyear_dict_func(main)
print("deathyear_dict created.")
death_age_dict = death_age_dict_func(main)
print("death_age_dict created.")
personid_list = personid_list_func(index_year_dict)
print("personid_list created.")
children_dict = children_dict_func(kinship)
print("children_dict created.")

rule1and2(personid_list)
print("Rule 1 and 2 finished.")
rule_degree(degree)
rule4(kinship)
print("Rule 4, 5, 6, and 7 finished.")
rule8(kinship)
print("Rule 8 finished.")
rule9(kinship)
print("Rule 9 finished.")
rule10(kinship)
print("Rule 10 finished.")
rule11(kinship)
print("Rule 11 finished.")
rule12(kinship)
print("Rule 12 finished.")
rule13(kinship)
print("Rule 13 finished.")
rule14(kinship)
print("Rule 14 finished.")
rule15(kinship)
print("Rule 15 finished.")
rule16(kinship)
print("Rule 16 finished.")
rule17(kinship)
print("Rule 17 finished.")
rule18(kinship)
print("Rule 18 finished.")
rule19(kinship)
print("Rule 19 finished.")
rule20(personid_list)
print("Rule 20 finished.")
df = DataFrame(list(index_year_dict.items()),columns=['c_personid','c_index_year'])
df.to_csv('output.csv',index=False)
print("All calculation finished.")