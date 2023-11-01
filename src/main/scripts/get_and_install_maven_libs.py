"""
The purpose of this script is to automate the steps described here:
https://www.ibm.com/docs/en/ads/23.0.1?topic=environment-deploying-maven-repository

This script will get the index.json file, then iterate through each of the JARs
and import them into the provided Maven repository.
"""
import base64
import logging
import os
import subprocess
import tempfile

import requests


def fetch_jars_and_install(ads_url, zen_user, zen_api_key, repo_id, repo_url):
    """
    Gets the JARs from the index.json and installs them into the Maven repository
    """
    index_url = f"{ads_url}/download/index.json"
    logging.debug("Downloading index file %s...", index_url)
    auth = base64.b64encode(f"{zen_user}:{zen_api_key}".encode("utf-8"))

    # pylint: disable=consider-using-f-string
    http_headers = {"Authorization": "ZenApiKey {0}".format(auth.decode("utf-8"))}
    logging.debug("Using %s for auth headers...", http_headers)

    index_response = requests.get(index_url, headers=http_headers, verify=False)
    index_json = index_response.json()
    logging.info("Got HTTP response: %d", index_response.status_code)

    with tempfile.TemporaryDirectory() as temp_dir:
        logging.info(
            "Getting %s JARs into %s directory...",
            len(index_json["resources"]),
            temp_dir,
        )

        for ads_resource in index_json["resources"]:
            jar_name = index_json["resources"][ads_resource]["path"]
            jar_file_url = f"{ads_url}/download/{jar_name}"
            jar_full_path = os.path.join(temp_dir, jar_name)
            logging.info("Getting file %s from %s...", jar_name, jar_file_url)
            jar_file = requests.get(jar_file_url, headers=http_headers, verify=False)
            with open(jar_full_path, "wb") as f:
                f.write(jar_file.content)

            if "pom_path" in index_json["resources"][ads_resource]:
                pom_name = index_json["resources"][ads_resource]["pom_path"]
                pom_file_url = f"{ads_url}/download/{pom_name}"
                pom_full_path = os.path.join(temp_dir, pom_name)
                logging.info("Getting file %s from %s...", pom_name, pom_file_url)
                pom_file = requests.get(
                    pom_file_url, headers=http_headers, verify=False
                )
                with open(pom_full_path, "wb") as f:
                    f.write(pom_file.content)

            # Now we have the file, use Maven to install the file into the repository...
            if "pom_path" in index_json["resources"][ads_resource]:
                # pylint: disable=line-too-long
                # mvn deploy:deploy-file -DpomFile=<POM_FILE> -DrepositoryId=<REPOSITORY_ID> -Durl=<ARTIFACTS_SERVER_URL> -Dfile=<JAR_FILE>
                subprocess.run(
                    [
                        "mvn",
                        "deploy:deploy-file",
                        f"-DpomFile={pom_full_path}",
                        f"-DrepositoryId={repo_id}",
                        f"-Durl={repo_url}",
                        f"-Dfile={jar_full_path}",
                    ]
                )
            else:
                # pylint: disable=line-too-long
                # mvn deploy:deploy-file -DgroupId=<GROUP_ID> -DartifactId=<ARTIFACT_ID> -Dversion=<VERSION> -Dpackaging=jar -DrepositoryId=<REPOSITORY_ID> -Durl=<ARTIFACTS_SERVER_URL> -Dfile=<PATH_TO_JAR_FILE>
                maven_info = index_json["resources"][ads_resource]["maven_coordinates"]
                group_id = maven_info["groupId"]
                artifact_id = maven_info["artifactId"]
                version = maven_info["version"]
                subprocess.run(
                    [
                        "mvn",
                        "deploy:deploy-file",
                        f"-DgroupId={group_id}",
                        f"-DartifactId={artifact_id}",
                        f"-Dversion={version}",
                        "-Dpackaging=jar",
                        f"-DrepositoryId={repo_id}",
                        f"-Durl={repo_url}",
                        f"-Dfile={jar_full_path}",
                    ]
                )


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    is_error = False
    for env_var in [
        "IBM_ADS_BASE_URL",
        "ZEN_USER",
        "ZEN_API_KEY",
        "ADS_MAVEN_REPO_ID",
        "ADS_MAVEN_REPO_URL",
    ]:
        if env_var not in os.environ:
            is_error = True
            logging.error("Environment variable \"%s\" must be defined. " +
                          "Check the README.md for usage.", env_var)

    if is_error:
        logging.fatal("Exiting.")
        exit()

    env_ads_url = os.environ["IBM_ADS_BASE_URL"]
    env_apikey = os.environ["ZEN_API_KEY"]
    env_zen_user = os.environ["ZEN_USER"]
    env_repo_id = os.environ["ADS_MAVEN_REPO_ID"]
    env_repo_url = os.environ["ADS_MAVEN_REPO_URL"]

    fetch_jars_and_install(
        ads_url=env_ads_url,
        zen_user=env_zen_user,
        zen_api_key=env_apikey,
        repo_id=env_repo_id,
        repo_url=env_repo_url,
    )
