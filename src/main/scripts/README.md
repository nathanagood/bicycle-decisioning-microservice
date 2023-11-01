# Utilities and tools for working with IBM ADS

## get_and_install_maven_libs.py

This Python script will download the JARs necessary for developing with IBM
Automation Decison Services (ADS) and install them--using 
`mvn deploy:deploy-file`--into the Maven repository you've specified. 

Before running the `get_and_install_maven_libs.py` script, make sure to set
the environment variables as shown here:

| Variable Name | Value |
| ------------- | ----------- |
| `IBM_ADS_BASE_URL` | The base URL of the ADS console. |
| `ZEN_USER` | The user for ADS |
| `ZEN_API_KEY` | An API key for the user. See https://www.ibm.com/docs/en/cloud-paks/cp-biz-automation/23.0.1?topic=access-using-zen-api-key-authentication |
| `ADS_MAVEN_REPO_ID` | The repository ID of the Maven repository into which the artifacts are installed. See https://www.ibm.com/docs/en/ads/23.0.1?topic=environment-deploying-maven-repository |
| `ADS_MAVEN_REPO_URL` | The URL of the Maven repository. |

This, of course, assumes some knowledge of Maven repositories and configuring
them, including configuring authentication.
