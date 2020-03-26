# TruSTAR Covid-19 report downloader

This is a simple Python script that will let you download the [COVID-19](https://www.trustar.co/blog/covid-19-impact-community-response)
intelligence reports into a local directory.

## Getting Started

In order for the script to run successfully, please make sure you have

- Python 3.x installed on your computer
- Credentials to the TruSTAR Platform (you can request them [here](https://www.trustar.co/en/covid-19))
- Your API Key and Secret (they can be obtained from your profile. This [support article](https://support.trustar.co/article/9u4paxdtdj-api) explains how)

## Step by step guide

1. Clone or download this repository

2. Install a "virtual environment" for it.

    ```commandline
    python3 -m venv venv
    ```

3. Activate your virtual environment

    ```commandline
    source venv/bin/activate
    ```

4. Use `pip` (or `pip3`) to install the dependencies required for this script to run

    ```commandline
    pip install --upgrade pip
    pip install -r requirements.txt
   ```

5. Set up a configuration directory and a configuration file. Review [TruSTAR SDK](https://docs.trustar.co/sdk/index.html) documentation for more information about this

    ```commandline
    mkdir config_file/private
    cp config_file/example/trustar.conf.spec config_file/private/trustar.conf
    ```

6. Copy your API key and secret into the file you just created

7. Run the script

    ```commandline
    python3 src/exe/covid_enclave_downloader.py
    ```

8. You'll find the downloaded reports in JSON format in the `./output` directory. Reports will be stored with the name `[updated_timestap]_[title]_[guid].json`

### Notes

1. If you run the script more then once, report files will be overwritten. 

2. This script will download all reports from the enclave every  time it runs.
    
3. The user whose API credentials are used needs to have "View" access to the `COVID-19` enclave. This is the case by default.

4. You need to run the script with enough permissions to write files into your file system.

5. This script is easily adaptable to be run periodically. Reach out to `support@trustar.co` if you have questions.
