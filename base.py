#Imports
import pandas as pd
import re
import string
import matplotlib.pyplot as plt
import seaborn as sns

#Import helper functions
from instagram_utils import find_person, print_conversation, cleaned, frequency_analysis, frequency_plot

#Set my_username as your instagram username
my_username = 'hrushikeshrv'
#Pass pd.read_json() the full path to the messages.json file in your instagram data
#For example - C://Users/.../Instagram_Data-20200629T20118Z-001/Data/username_date_part_1/messages.json
dms = pd.read_json('C:/Users/Hrush/Downloads/hrushikeshrv_20200722_part_1/messages.json')

#Enter the account name you want to analyze your history with
person = 'amrunikothadia'

posts_sent, posts_recieved, photos_sent, photos_recieved = print_conversation(person, my_username, dms, True)
frequency_plot(person, dms, 3)
frequency_plot(person, dms, 6)
frequency_analysis(person, dms)