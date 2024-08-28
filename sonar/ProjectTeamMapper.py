from utils.JsonFileHandler import JsonFileHandler
import sonar.Constants as const


class ProjectTeamMapper:
  projects_data = None
  mapping_data = None
  output_file = None

  def __init__(self, config_file_name):
    config = JsonFileHandler.read_from_file(config_file_name)
    project_metrics_file_name = config[const.SONAR_METRICS_OUTPUT]
    project_mapping_file_name = config[const.CONFIG_TEAM_MAPPING]

    self.projects_data = JsonFileHandler.read_from_file(project_metrics_file_name)
    self.mapping_data = JsonFileHandler.read_from_file(project_mapping_file_name)

    self.output_file = config[const.CONFIG_METRICS_MAPPING_OUTPUT]

  def __get_team_mapping_in_data(self, team_name, teams_mapping):
    try:
      return next(
        (item for item in teams_mapping if item[const.K_TEAM] == team_name),
        None,
      )
    except StopIteration:
      raise ValueError

  def __is_repository_in_project_keys(self, repository, team_name, is_production, is_print_output):
    is_found = False
    for index in range(len(self.projects_data)):
      project_key = self.projects_data[index][const.K_NAME]
      if project_key == repository:
        is_found = True
        self.projects_data[index][const.K_BELONGS] = team_name
        if is_production:
          self.projects_data[index][const.K_IS_PROD] = 1
        if is_print_output:
          print(f"{repository} -> {team_name} OK")
        # return is_found
    return is_found

  def __check_project_keys_for_team(self, team_name, team_mapping, is_print_output):
    repositories = None
    repositories_prod = None

    if const.K_REPOS in team_mapping:
      repositories = team_mapping[const.K_REPOS]
      if repositories:
        for repository in repositories:
          is_found = self.__is_repository_in_project_keys(repository, team_name, False, is_print_output)
        if not is_found and is_print_output:
          print(f"{repository} NOTFOUND")

    if const.K_REPOS_PROD in team_mapping:
      repositories_prod = team_mapping[const.K_REPOS_PROD]
      if repositories_prod:
        for repository_prod in repositories_prod:
          is_found = self.__is_repository_in_project_keys(repository_prod, team_name, True, is_print_output)
        if not is_found and is_print_output:
          print(f"{repository_prod} NOTFOUND")

  def check_project_keys_for_team(self, team_name, is_print_output):
    teams_mapping = self.mapping_data[const.K_MAPPING]
    team_mapping = self.__get_team_mapping_in_data(team_name, teams_mapping)

    if team_mapping is None:
      raise Exception(f"{team_name} could not be found in mapping data!")

    self.__check_project_keys_for_team(team_name, team_mapping, is_print_output)

  def check_project_keys_for_teams(self, is_print_output):
    teams_mappings = self.mapping_data[const.K_MAPPING]

    for mapping in teams_mappings:
      team_name = mapping[const.K_TEAM]
      self.check_project_keys_for_team(team_name, is_print_output)

  def write_mapping(self):
    if self.projects_data:
      JsonFileHandler.dump_to_file(self.output_file, self.projects_data, True)
    else:
      print("WARNING: Could not write data, data is empty")
