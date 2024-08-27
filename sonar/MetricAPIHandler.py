import os
import requests
from requests.auth import HTTPBasicAuth
from utils.JsonFileHandler import JsonFileHandler
from dotenv import load_dotenv
import sonar.Constants as const

load_dotenv()
SONAR_AUTH_TOKEN = os.getenv("SONAR_AUTH_TOKEN")


class MetricAPIHandler:
  def __parse_project_measures(self, response_data, project_data):
    if const.K_COMPONENT not in response_data:
      raise KeyError(f"Could not find {const.K_COMPONENT} key in {response_data}")

    if const.K_MEASURES not in response_data[const.K_COMPONENT]:
      raise KeyError(f"Could not find 'measures' key in {response_data[const.K_COMPONENT]}")

    measures = response_data[const.K_COMPONENT][const.K_MEASURES]

    for measure in measures:
      metric_name = measure[const.K_METRIC]
      metric_value = measure[const.K_VALUE]
      project_data[metric_name] = metric_value

    return project_data

  def __call_api(self, api_url, auth_token, project_data):
    try:
      response = requests.get(api_url, auth=HTTPBasicAuth(auth_token, ""))

      if response.status_code != 200:
        print(
          "Failed to fetch. Status code:",
          response.status_code,
          response.json(),
        )

      response_data = response.json()
      project_data = self.__parse_project_measures(response_data, project_data)

      return project_data

    except requests.RequestException as e:
      print("Error:", e)

  def get_metrics(self, config_file_name):
    # Get Base configuration
    config = JsonFileHandler.read_from_file(config_file_name)
    sonar_url = config[const.SONAR_URL]
    metrics_string = config[const.SONAR_METRICS_STRING]

    # Read Sonar project keys from file
    project_keys_output = config[const.SONAR_PROJECT_KEYS_OUTPUT]
    projects = JsonFileHandler.read_from_file(project_keys_output)

    for project in projects:
      if const.K_KEY in project:
        project_key = project[const.K_KEY]

        metric_url_endpoint = f"{sonar_url}{const.SONAR_METRIC_API_ENDPOINT}?component={project_key}&metricKeys={metrics_string}"

        project = self.__call_api(metric_url_endpoint, SONAR_AUTH_TOKEN, project)

    projects_metrics_file_name = config[const.SONAR_METRICS_OUTPUT]
    JsonFileHandler.dump_to_file(projects_metrics_file_name, projects, True)
