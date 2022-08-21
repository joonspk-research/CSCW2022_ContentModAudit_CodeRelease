"""
Original author: Joon Sung Park, Stanford University 
Last updated: December 15, 2020
"""
import praw
import boto3
import os

from datetime import date, datetime

from global_methods import *
from global_variables import * 
from utils import *

def clean_up_temp_all_folder(outfile):
  date_folder_name = "/".join(outfile.split("/")[:2])
  os.remove(outfile)


def get_upload_file_key(file_offset=1): 
  today = date.today().strftime("%m_%d_%y")
  file_key = ("temp_all_comment_bank/" 
              + today + "__"
              + str(file_offset) + ".csv")
  return file_key


def collector_server(DEBUG=False): 
  """
  Streams all content from the subreddits listed in ALL_ACTIVE_SUBREDDITS and
  saves them in a AWS S3 bucket for one day. You likely want to continue on
  the data collection process for longer than a day depending on your 
  research question -- I recommend setting up cron schedule instances on the 
  machine where you are running this collector.
  
  Collector takes the following general steps: 
    A) Streams all content of interested and saves to a local file. 
    B) Once we have the number of rows matching the FILE_SIZE we specified in
       utils.py, we move those rows to our AWS S3 bucket and erase the local 
       files. Note that 

  We are streaming and saving a significant portion of (if not all) of Reddit
  -- this is potentially a lot of data (unless you want to run this code for a
  smaller experient, which you should be able to do with relatively little 
  modification to the code base). So the steps laid out above are important 
  for ensuring that you are not storing an unreasonable amount of data in your
  local server, and the data transfer between your local server and the cloud 
  is not going to over-burden your network. 

  You may want to play with the FILE_SIZE -- if this is higher, you are 
  transferring more data in one batch, but if this is lower, you are 
  transferring less but more often. The optimal number here may depend on your
  network/servers. If not sure, just use 25,000. It worked pretty well for us.

  Args:
    DEBUG: If True, we do not connect to AWS S3 bucket. 

  RETURNS: 
    None
  """
  # Setting up the AWS S3 instance and Reddit's praw instance.  
  s3 = boto3.resource('s3', 
                      aws_access_key_id=AWS_ACCESS_KEY, 
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
  reddit = praw.Reddit(client_id=PRAW_CLIENT_ID,
                       client_secret=PRAW_CLIENT_SECRET,
                       user_agent=PRAW_USER_AGENT)
  file_offset = 1

  # Gets the system date for today. We will finish our data collection if this
  # day ends. 
  collection_date = date.today().strftime("%m_%d_%y")

  # These are the columns of the content we are saving. Reddit's praw (as of 
  # 2020) offers more columns than what we are collecting here, so you should
  # check praw's documentation page to see if there's something you need.
  header = ["subreddit", "comment id", "body", "created utc", "author"]
  curr_file_rows = [header]

  # Main streaming loop. 
  for comment in reddit.subreddit(ALL_ACTIVE_SUBREDDITS_STR).stream.comments():
    curr_row = [comment.subreddit, 
                comment.id, 
                comment.body, 
                comment.created_utc,
                comment.author]
    curr_file_rows += [curr_row]
    today = date.today().strftime("%m_%d_%y")

    # Activates file transfer to S3 when we have FILE_SIZE number of rows or 
    # if we have hit the end of the day.
    if len(curr_file_rows) % FILE_SIZE == 1 or collection_date != today: 
      outfile = get_upload_file_key(file_offset)
      write_list_of_list_to_csv(curr_file_rows, outfile)
      
      if not DEBUG: 
        s3.meta.client.upload_file(outfile, S3_BUCKET, outfile)
        clean_up_temp_all_folder(outfile)

      curr_file_rows = [header]
      file_offset += 1

    # If we hit the end of the day, we break in preparation for the reboot.
    if collection_date != today: 
      break


if __name__ == '__main__':
  collector_server(DEBUG=False)




















