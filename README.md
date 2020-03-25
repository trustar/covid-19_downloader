# covid-19_downloader
A short script to download reports from the covid enclave to json 
files in a local directory. 

Steps: 

    1. Install python 3 on your computer.  
    2. Run "setup.sh".
    3. Follow recommendation 2 (below), if it makes sense with your 
    requirements.     
    4. Make a config file with your API creds and put it in the 
    "private" directory.  Name the file "trustar.conf"
    5. run "covid.sh". 

"setup.sh" will:

    -create a new python virtual environment.
    -activate the new python virtual environment.  
    -install the dependencies listed in requirements.txt into the 
    new virtual environment. 
    -deactivate the new virtual environment. 
    -copy the spec config file to the "private" dir, where the user can
    rename it and enter their API credentials into it. 
    
"covid.sh" will:

    -activate your virtual environment. 
    -update your TruSTAR python sdk. 
    -run the script, directing its output to the "output" dir. 
    -deactivate the virtual environment. 
    
Things to note:

    1. If a report file already exists in the output directory, it
    will be overwritten with what the script downloads on the 
    current run.  
    
    2.  If a report in the unclave is updated and you don't delete
    the reports from "output" directory before running the script 
    again, you will get a second file in the 'output' directory that
    contains the same report.  One file will be the file creted on 
    a previous script-run, the second will be the update to that 
    report.  Recommended best-practice for the general use-case for
    this script is to delete all files from the 'output' directory
    before running the script again. 
    
    3. This script will download all reports in the enclave every 
    time it runs.  It does not keep "state" / "checkpoint" of any
    sort.  
    
Recommendations:

    1. Consider configuring daemon-manager to continuously restart 
    "covid.sh" 30 minutes after it finishes. 

    2. Consider having Station Company Administrator should make 
    a new user account for this script and use that user acocunt's
    API credentials.  See  this docs page:
    
        https://support.trustar.co/article/g7cjc1nv1d-setting-up-a-service-account

    3. Recommend deleting everything from the 'output' directory before
    running the script again.  See "Things to Note" item 2. 
    
DO NOTs: 

    1. Do not start the script in more than 1 process simultaneously.
    Doing this will cause them all to crash.  
    
    2. Do not put this in a cron-job.  Cron will start the script 
    in a second process even if the script is already running in a 
    process and hasn't completed yet.  This will cause all  
    processes running this script to crash. 
    

Permissions:

    1. Station user account. 
    
    The Station user account whose API credentials are used for 
    this script (hopefully, it's a service-type user account IAW 
    Recommendation 2) need to have "view" or greater permissions
    to the COVID-19 enclave.  It does not need any level of 
    access to any other enclave. 
    
    
    2. OS user account. 
    
    The operating system user account used to launch this script will 
    need to be able to read/write/execute files in the directory that 
    this repo resides in.  It writes output to the 'output' directory, 
    and log files to the 'logs' directory. 