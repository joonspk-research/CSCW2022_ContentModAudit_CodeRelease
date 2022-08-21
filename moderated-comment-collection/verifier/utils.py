"""
Original author: Joon Sung Park, Stanford University 
Last updated: December 15, 2020
"""
import praw
import boto3

from global_methods import *
from global_variables import * 

# Note: See verifier.py documentation. CURR_VERIFIER_ID and ALL_VERIFIER_COUNT
#       are used to enable parallelization of multiple verifiers.
# (MAX is ALL_VERIFIER_COUNT - 1)
CURR_VERIFIER_ID = 0
# CURR_VERIFIER_ID = 1
# CURR_VERIFIER_ID = 2

ALL_VERIFIER_COUNT = 3 

ALL_ACTIVE_SUBREDDITS_STR = "+".join(ALL_ACTIVE_SUBREDDITS)

# NOTE: You need to fill in <*> with your bucket name, key, ID, etc.  
S3_BUCKET = "<YOUR S3 BUCKET NAME>" 

AWS_ACCESS_KEY = "<YOUR ACCESS KEY>"
AWS_SECRET_ACCESS_KEY = "<YOUR SECRET ACCESS KEY>"

PRAW_CLIENT_ID = "<YOUR PRAW CLIENT ID>"
PRAW_CLIENT_SECRET = "<YOUR PRAW CLIENT SECRET KEY>"
PRAW_USER_AGENT = "User-Agent: android:com.example.myredditapp:v1.2.3 (by /u/Jealous-Escape-4507)"