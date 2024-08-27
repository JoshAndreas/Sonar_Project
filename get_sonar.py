from sonar.ProjectAPIHandler import ProjectAPIHandler
from sonar.MetricAPIHandler import MetricAPIHandler
from sonar.ProjectTeamMapper import ProjectTeamMapper
from sonar.SonarReportWriter import SonarReportWriter


def run():
  print("## SONAR REPORTING START ##")
  #projectAPIHandler = ProjectAPIHandler()
  #metricAPIHandler = MetricAPIHandler()
  print(">> Grab project keys in Sonar")
  #projectAPIHandler.get_projects("config.json")
  print(">> Grab metrics for all project keys")
  #metricAPIHandler.get_metrics("config.json")
  #projectTeamMapper = ProjectTeamMapper("config.json")
  print(">> Check with project belong to which team")
  print(">> Check which project is running in PROD")
  #projectTeamMapper.check_project_keys_for_teams(is_print_output=False)
  #projectTeamMapper.write_mapping()
  print(">> Write Report")
  sonarReportWriter = SonarReportWriter("config.json")
  sonarReportWriter.write_report()
  print("## SONAR REPORTING COMPLETE ##")


run()
