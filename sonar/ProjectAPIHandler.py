import os
import requests
from requests.auth import HTTPBasicAuth
from utils.JsonFileHandler import JsonFileHandler
from dotenv import load_dotenv
import sonar.Constants as const


load_dotenv()
SONAR_AUTH_TOKEN = os.getenv("SONAR_AUTH_TOKEN")


class ProjectAPIHandler:
  def __parse_response_data(self, response_data, project_key_data):
    if const.K_COMPONENTS not in response_data:
      raise KeyError(f"Could not find {const.K_COMPONENTS} key in {response_data}")

    if len(response_data[const.K_COMPONENTS]) <= 0:
      return None

    for component in response_data[const.K_COMPONENTS]:
      # create own output
      project = {}
      project[const.K_KEY] = component[const.K_KEY]
      project[const.K_NAME] = component[const.K_NAME]
      project_key_data.append(project)

    return project_key_data

  def __call_api(self, api_url, auth_token):
    try:
      response = requests.get(
        api_url,
        auth=HTTPBasicAuth(auth_token, ""),
      )

      if response.status_code != 200:
        print(
          "Failed to fetch projects or components. Status code:",
          response.status_code,
          response.json(),
        )

      response_data = response.json()
      data = []
      data = self.__parse_response_data(response_data, data)
      return data

    except requests.RequestException as e:
      print("Error", e)

  def get_projects(self, config_file_name):
    project_keys = []

    config = JsonFileHandler.read_from_file(config_file_name)
    sonar_url = config[const.SONAR_URL]

    for index in range(1, const.MAX_PAGES):
      url = f"{sonar_url}{const.SONAR_PROJECT_API_ENDPOINT}&p={index}"
      data = self.__call_api(url, SONAR_AUTH_TOKEN)

      if data:
        project_keys = project_keys + data
      else:
        break

    project_keys_output = config[const.SONAR_PROJECT_KEYS_OUTPUT]
    JsonFileHandler.dump_to_file(project_keys_output, project_keys, True)
