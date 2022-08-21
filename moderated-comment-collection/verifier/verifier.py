"""
Original author: Joon Sung Park, Stanford University 
Last updated: December 15, 2020
"""
import praw
import boto3
import os

from datetime import date, datetime, timedelta

from global_methods import *
from global_variables import * 
from utils import *


def clean_up_temp_all_folder(outfile):
  date_folder_name = "/".join(outfile.split("/")[:2])
  os.remove(outfile)


def date_and_offset_key_reconstruction(file_date, file_offset): 
  return file_date.strftime("%m_%d_%y__") + str(file_offset) + ".csv"


def get_curr_s3_all_comment_bank_file_key(s3client): 
  response = s3client.list_objects_v2(Bucket=S3_BUCKET,
                                      Prefix ='temp_all_comment_bank/',
                                      MaxKeys=100)['Contents']
  
  response_date_and_offset = []
  for i in response: 
    i = i["Key"]
    file_date = i.split("/")[-1].split("__")[0]
    file_date = datetime.strptime(file_date, "%m_%d_%y").date()
    file_offset = int(i.split("/")[-1].split("__")[1].split(".")[0])

    response_date_and_offset += [[file_date, file_offset]]

  response_date_and_offset.sort()
  for i in response_date_and_offset: 
    file_date = i[0]
    file_offset = i[1]
    if file_date == (date.today() - timedelta(days=1)): 
      if file_offset % ALL_VERIFIER_COUNT == CURR_VERIFIER_ID: 
        key = date_and_offset_key_reconstruction(file_date, file_offset)
        return "temp_all_comment_bank/" + key

  return False


def download_file_from_s3(s3, key): 
  s3.Bucket(S3_BUCKET).download_file(key, key)


def delete_file_from_s3(s3, key): 
  s3.Object(S3_BUCKET, key).delete()


def write_file_to_s3(s3, key): 
  s3.meta.client.upload_file(key, S3_BUCKET, key)


def verify(s3, reddit, key): 
  head, rows = read_file_to_list(key, header=True)
  all_verified_removed_rows = []

  for row in rows: 
    comment_id = row[1]
    curr_comment = reddit.comment(comment_id).body
    if ("[removed]" in curr_comment 
          or '["removed"]' in curr_comment
          or "['removed']" in curr_comment):
       all_verified_removed_rows += [row]

  verified_key = "temp_verified_comment_bank/" + key.split("/")[-1]
  write_list_of_list_to_csv(all_verified_removed_rows, verified_key)

  write_file_to_s3(s3, verified_key)

  clean_up_temp_all_folder(key)
  clean_up_temp_all_folder(verified_key)


def verifier_server(DEBUG=False): 
  """
  We assume that our collector has streamed and collected the Reddit data of
  interest in our S3 folder. We now need to verify which of those are actually
  "removed" -- that is, moderated by the content moderators on Reddit. 

  Our strategy here is as follows: 
    A) Retrieve the saved files from AWS S3 bucket. 
    B) We look at the retrieved data row by row, and actualyl call on the
       Reddit server to see if they were replaced with a "[removed]" tag, 
       which signifies that the content was removed.
    C) We save the content of the [removed] rows in our storage. 

  Note that this verification stage is computationally much more expensive. So
  where we only used one server for the collector, we are better off 
  instantiating more than one servers as verifiers working in parallel if we
  were to verify at the same pace as we are collecting these data. This 
  paralleliazation step is implemented by the CURR_VERIFIER_ID variable 
  in the utils.py file. Set ALL_VERIFIER_COUNT to the number of the max
  verifier server instance, and increment CURR_VERIFIER_ID as you 
  instantiate a new server.

  Args:
    DEBUG: If True, we do not connect to AWS S3 bucket. 

  RETURNS: 
    None
  """
  # Setting up the AWS S3 instance and Reddit's praw instance.  
  s3client = boto3.client("s3",
                    aws_access_key_id=AWS_ACCESS_KEY, 
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
  s3 = boto3.resource('s3', 
                      aws_access_key_id=AWS_ACCESS_KEY, 
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
  reddit = praw.Reddit(client_id=PRAW_CLIENT_ID,
                       client_secret=PRAW_CLIENT_SECRET,
                       user_agent=PRAW_USER_AGENT)

  while True:
    # This is the current data file of interest that we will retrieve from S3.
    curr_s3_all_comment_bank_file_key = get_curr_s3_all_comment_bank_file_key(s3client)
    # And this is where we verify: 
    if curr_s3_all_comment_bank_file_key:
      # Note that after we download the file from S3, we delete it from it. 
      # This is an optimization step so you don't have a ton of data piling 
      # on your S3 server, which could add up the maintenance cost. But if you
      # have the fund and want to retain all the data, you do not actually 
      # have to delete the files. 
      download_file_from_s3(s3, curr_s3_all_comment_bank_file_key)
      delete_file_from_s3(s3, curr_s3_all_comment_bank_file_key)
      verify(s3, reddit, curr_s3_all_comment_bank_file_key)
    else: 
      break 

  
if __name__ == '__main__':
  verifier_server(DEBUG=False)
 




















