"""
Original author: Joon Sung Park, Stanford University 
Last updated: December 15, 2020
"""
import random
import string
import csv
import time
import datetime as dt
import pathlib
import os
import sys
import numpy

from os import listdir
from collections import Counter 


def create_folder_if_not_there(curr_path): 
  """
  Checks if a folder in the curr_path exists. If it does not exist, creates
  the folder. 
  Note that if the curr_path designates a file location, it will operate on 
  the folder that contains the file. But the function also works even if the 
  path designates to just a folder. 

  Args:
    curr_list: list to write. The list comes in the following form:
               [['key1', 'val1-1', 'val1-2'...],
                ['key2', 'val2-1', 'val2-2'...],]
    outfile: name of the csv file to write    

  RETURNS: 
    True: if a new folder is created
    False: if a new folder is not created
  """
  outfolder_name = curr_path.split("/")
  if len(outfolder_name) != 1: 
    # This checks if the curr path is a file or a folder. 
    if "." in outfolder_name[-1]: 
      outfolder_name = outfolder_name[:-1]

    outfolder_name = "/".join(outfolder_name)
    if not os.path.exists(outfolder_name):
      os.makedirs(outfolder_name)
      return True

  return False 


def write_list_of_list_to_csv(curr_list_of_list, outfile):
  """
  Writes a list of list to csv. 
  Unlike write_list_to_csv_line, it writes the entire csv in one shot. 

  ARGS:
    curr_list_of_list: list to write. The list comes in the following form:
               [['key1', 'val1-1', 'val1-2'...],
                ['key2', 'val2-1', 'val2-2'...],]
    outfile: name of the csv file to write    

  RETURNS: 
    None
  """
  create_folder_if_not_there(outfile)
  with open(outfile, "w") as f:
    writer = csv.writer(f)
    writer.writerows(curr_list_of_list)


def write_list_to_csv_line(line_list, outfile): 
  """
  Writes one line to a csv file.
  Unlike write_list_of_list_to_csv, this opens an existing outfile and then 
  appends a line to that file. 
  This also works if the file does not exist already. 

  ARGS:
    curr_list: list to write. The list comes in the following form:
               ['key1', 'val1-1', 'val1-2'...]
               Importantly, this is NOT a list of list. 
    outfile: name of the csv file to write   

  RETURNS: 
    None
  """
  create_folder_if_not_there(outfile)

  # Opening the file first so we can write incrementally as we progress
  curr_file = open(outfile, 'a',)
  csvfile_1 = csv.writer(curr_file)
  csvfile_1.writerow(line_list)
  curr_file.close()


def read_file_to_list(curr_file, header=False): 
  """
  Reads in a csv file to a list of list. If header is True, it returns a 
  tuple with (header row, all rows)

  ARGS:
    curr_file: path to the current csv file. 

  RETURNS: 
    List of list where the component lists are the rows of the file. 
  """
  if not header: 
    analysis_list = []
    with open(curr_file) as f_analysis_file: 
      data_reader = csv.reader(f_analysis_file, delimiter=",")
      for count, row in enumerate(data_reader): 
        analysis_list += [row]
    return analysis_list
  else: 
    analysis_list = []
    with open(curr_file) as f_analysis_file: 
      data_reader = csv.reader(f_analysis_file, delimiter=",")
      for count, row in enumerate(data_reader): 
        analysis_list += [row]
    return analysis_list[0], analysis_list[1:]

def read_file_to_set(curr_file, col=0): 
  """
  Reads in a "single column" of a csv file to a set. 

  ARGS:
    curr_file: path to the current csv file. 

  RETURNS: 
    Set with all items in a single column of a csv file. 
  """
  analysis_set = set()
  with open(curr_file) as f_analysis_file: 
    data_reader = csv.reader(f_analysis_file, delimiter=",")
    for count, row in enumerate(data_reader): 
      analysis_set.add(row[col])
  return analysis_set


def get_row_len(curr_file): 
  """
  Get the number of rows in a csv file 

  ARGS:
    curr_file: path to the current csv file. 

  RETURNS: 
    The number of rows
    False if the file does not exist
  """
  try: 
    analysis_set = set()
    with open(curr_file) as f_analysis_file: 
      data_reader = csv.reader(f_analysis_file, delimiter=",")
      for count, row in enumerate(data_reader): 
        analysis_set.add(row[0])
    return len(analysis_set)
  except: 
    return False


def check_if_file_exists(curr_file): 
  """
  Checks if a file exists

  ARGS:
    curr_file: path to the current csv file. 

  RETURNS: 
    True if the file exists
    False if the file does not exist
  """
  try: 
    with open(curr_file) as f_analysis_file: pass
    return True
  except: 
    return False


def find_filenames(path_to_dir, suffix=".csv"):
  """
  Given a directory, find all files that ends with the provided suffix and 
  returns their paths.  

  ARGS:
    path_to_dir: Path to the current directory 
    suffix: The target suffix.

  RETURNS: 
    A list of paths to all files in the directory. 
  """
  filenames = listdir(path_to_dir)
  return [ path_to_dir+"/"+filename 
           for filename in filenames if filename.endswith( suffix ) ]


def average(list_of_val): 
  """
  Finds the average of the numbers in a list.

  ARGS:
    list_of_val: a list of numeric values  

  RETURNS: 
    The average of the values
  """
  return sum(list_of_val)/float(len(list_of_val))

def std(list_of_val): 
  """
  Finds the std of the numbers in a list.

  ARGS:
    list_of_val: a list of numeric values  

  RETURNS: 
    The std of the values
  """
  std = numpy.std(list_of_val)
  return std


def get_random_alphanumeric_string(length):
  """
  Returns a randomly generated alphanumeric string with a given length. 

  ARGS:
    length: the length of the alphanumeric string.  

  RETURNS: 
    A randomly generated string. 
  """
  letters_and_digits = string.ascii_letters + string.digits
  result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
  return result_str


def most_frequent(List): 
  """
  Given a list, find th element that is most frequently occuring. 

  ARGS:
    List: The input list.  

  RETURNS: 
    Element that is most frequently occuring.
  """
  occurence_count = Counter(List) 
  return occurence_count.most_common(1)[0][0] 


def unix_time_to_readable_time(unix_time): 
  """
  Converts unix time to a readable time str. Unix time is just an int that 
  represents some time. Often used by reddit (praw).  

  ARGS:
    List: unix time.  

  RETURNS: 
    A readable time str.
  """
  return dt.datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')





