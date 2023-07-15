# notion-api-automation

Here are some useful scripts to automate notion and interact with it programmatically.

It's really random as of this writing so it's not easy to navigate currently but feel free to pick through the scripts for ideas on how you can automate notion using python. 


## Recurring tasks

The recurring_tasks.py is the main script that will copy items from one database and place them in another. 

The first database should be the one that is set up with the recurring tasks that you want with a table structure that has the following properties: 

1) Task Name
2) Day of Week (Multi-select with the days of the week) 
3) Day of Month (Multi-select with numbers 1-28 to represent each day of a month) 


Once you have that database, you can set up a new database that is your main task tracking database. This is where you would list out all of your tasks that are one-off tasks. 

Then, set up the recurring_tasks.py script to run every day at whatever time you would like (using whatever method of recurring jobs you want, I use crontab running on an old linux at my house). Make sure to set up a new application through notion so that you can grant access to your particular machine that is running the jobs. I wont get too into those details, as that is more about setting up a developer account with notion and setting up your API Keys. 

