# covid-19_downloader
A short script to download reports from the covid enclave to json 
files in a local directory. 

Steps: 

    1. Install python 3 on your computer.  
    2. Run "setup.sh".
    3. Follow recommendation 2, if it makes sense with your 
    requirements. 
    4. Get the config file template from the Python SDK docs: 
    
        https://docs.trustar.co/sdk/TruStar/index.html
    
    5. Make a config file with your API creds and put it in the 
    "private" directory.  Name the file "trustar.conf"
    
    6. run "covid.sh". 

"setup.sh" will:

    -create a new python virtual environment.
    -activate the new python virtual environment.  
    -install the dependencies listed in requirements.txt into the 
    new virtual environment. 
    -deactivate the new virtual environment. 
    
"covid.sh" will:

    -activate your virtual environment. 
    -update your TruSTAR python sdk. 
    -run the script, directing its output to the "output" dir. 
    -deactivate the virtual environment. 
    
Things to note:

    1. If a report file already exists in the output directory, it
    will be overwritten with what the script downloads on the 
    current run.  This keeps the reports in the output dir 
    up-to-date with the most-current version in the COVID-19 
    enclave. 
    
    2. This script will download all reports in the enclave every 
    time it runs.  It does not keep "state" / "checkpoint" of any
    sort.  
    
Recommendations:

    1. Consider configuring daemon-manager to continuously restart 
    "covid.sh" 30 minutes after it finishes. 

    2. Consider having Station Company Administrator should make 
    a new user account for this script and use that user acocunt's
    API credentials.  See  this docs page:
    
        https://support.trustar.co/article/g7cjc1nv1d-setting-up-a-service-account

    
DO NOTs: 

    1. Do not start the script in more than 1 process simultaneously.
    Doing this will cause them all to crash.  
    
    2. Do not put this in a cron-job.  Cron will start the script 
    in a second process even if the script is already running in a 
    process and hasn't completed yet.  This will cause all  
    processes running this script to crash. 
    

Permissions:

    The Station user account whose API credentials are used for 
    this script (hopefully, it's a service-type user account IAW 
    Recommendation 2) need to have "view" or greater permissions
    to the COVID-19 enclave.  It does not need any level of 
    access to any other enclave. 