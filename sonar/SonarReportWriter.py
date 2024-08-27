import os
from datetime import date
from utils.JsonFileHandler import JsonFileHandler
from writers.ExcelWriter import ExcelWriter, Font
from writers.BuiltinStyles import BuiltinStyles
import sonar.Constants as const


class SonarReportWriter:
    COL_START_INDEX_TO_POPULATE_METRICS = 4

    NUM_FORMAT_FLOAT = "0.0"
    NUM_FORMAT_PERCENTAGE = "0.00%"
    NUM_FORMAT_INTEGER = "0"
    NUM_FORMAT_MILLISECONDS = "0s"
    NUM_FORMAT_DATETIME = "dd/mm/yyyy hh:mm:ss"
    NUM_FORMAT_DATE = "dd/mm/yyyy"

    STYLE_HEADER = "header"

    def __init__(self, config_file_name):
        self.config = JsonFileHandler.read_from_file(config_file_name)
        project_metrics_file_name = self.config[const.CONFIG_METRICS_MAPPING_OUTPUT]
        self.data = JsonFileHandler.read_from_file(project_metrics_file_name)
        self.excelWriter = ExcelWriter("openpyxl")
        self.metrics_definition = self.config[const.CONFIG_METRICS]
        self.report_file_name = self.config[const.CONFIG_REPORT_FILE_NAME]

    def write_report(self):
        if os.path.isfile(self.report_file_name):
            workbook = self.excelWriter.open_workbook(self.report_file_name)
        else:
            workbook = self.excelWriter.create_workbook(self.report_file_name)

        # Register Styles
        font = Font(bold=True, color="00FF0000")
        self.excelWriter.register_style(workbook, self.STYLE_HEADER, font=font)

        # Create Worksheet
        today = date.today()
        worksheet_name = today.strftime("%Y%m%d")
        exists = self.excelWriter.exist_worksheet(workbook, worksheet_name)
        if exists:
            self.excelWriter.delete_worksheet(workbook, worksheet_name)
        worksheet = self.excelWriter.add_worksheet(workbook, worksheet_name)

        # Delete default Worksheet
        default_sheet = "Sheet"
        exists = self.excelWriter.exist_worksheet(workbook, default_sheet)
        if exists:
            self.excelWriter.delete_worksheet(workbook, default_sheet)

        self.__fill_worksheet(worksheet)
        self.excelWriter.filter_columns(worksheet, "A1:AA500")
        self.excelWriter.autofit_columns(worksheet)
        self.excelWriter.close_workbook(workbook)

    def __fill_worksheet(self, worksheet):
        col_index = self.COL_START_INDEX_TO_POPULATE_METRICS
        row_index = 2
        is_header_created = False

        if not isinstance(self.data, list):
            raise ValueError("Error given metric data. No array.")

        for el in self.data:
            for metric in self.metrics_definition:
                metric_key = metric.get(const.METRICS_KEY)
                metric_threshold = metric.get(const.METRICS_THRESHOLD)

                if not is_header_created:
                    # Create header
                    self.excelWriter.write(worksheet, 1, 1, "Project Name", self.STYLE_HEADER)
                    self.excelWriter.write(worksheet, 1, 2, "Belongs To", self.STYLE_HEADER)
                    self.excelWriter.write(worksheet, 1, 3, "Production", self.STYLE_HEADER)
                    self.excelWriter.write(worksheet, 1, 4, "Reliability Rating", self.STYLE_HEADER)
                    self.excelWriter.write(worksheet, 1, 5, "Security Rating", self.STYLE_HEADER)
                    self.excelWriter.write(worksheet, 1, 6, "Maintainability Rating", self.STYLE_HEADER)
                    self.excelWriter.write(worksheet, 1, 7, "Line Coverage (%)", self.STYLE_HEADER)
                    self.excelWriter.write(worksheet, 1, 8, "Quality Gate Status", self.STYLE_HEADER)
                    self.excelWriter.write(worksheet, 1, 9, "Reliability Remediation Effort (min)", self.STYLE_HEADER)
                    self.excelWriter.write(worksheet, 1, 10, "Date of Last Commit (dd/mm/yyyy)", self.STYLE_HEADER)
                    self.excelWriter.write(worksheet, 1, 11, "NC LOC (loc)", self.STYLE_HEADER)
                    self.excelWriter.write(worksheet, 1, 12, "Duplicated Lines", self.STYLE_HEADER)
                    is_header_created = True

                # Check if the metric key exists in the element el
                if metric_key not in el:
                    print(f"Warning: Metric '{metric_key}' not found for project '{el.get(const.K_NAME, 'unknown')}'. Skipping...")
                    col_index += 1
                    continue

                # Handle the metric based on its type
                match metric.get(const.METRICS_TYPE, "").upper():
                    case "INT":
                        self.excelWriter.write_number(
                            worksheet,
                            row_index,
                            col_index,
                            int(el[metric_key]),
                            number_format=self.NUM_FORMAT_INTEGER,
                        )
                    case "LEVEL":
                        self.excelWriter.write(worksheet, row_index, col_index, el[metric_key])
                    case "MILLISEC":
                        ms = int(el[metric_key])
                        date_from_timestamp = date.fromtimestamp(ms / 1000.0)
                        self.excelWriter.write_number(
                            worksheet,
                            row_index,
                            col_index,
                            date_from_timestamp,
                            number_format=self.NUM_FORMAT_DATE,
                        )
                    case "PERCENT":
                        # Convert the metric value to a float
                        metric_value = float(el[metric_key])

                        # If the value is greater than 1, it's likely not in percentage form, so divide by 100
                        if metric_value > 1:
                            metric_value /= 100

                        # Format the percentage value as a string with a "%" symbol
                        percentage_string = f"{metric_value * 100:.1f}%"

                        # Write the percentage string to the worksheet directly
                        if metric_threshold:
                            if metric_value >= metric_threshold:
                                self.excelWriter.write(
                                    worksheet,
                                    row_index,
                                    col_index,
                                    percentage_string,  # Manually formatted percentage with %
                                    style=BuiltinStyles.GOOD
                                )
                            else:
                                self.excelWriter.write(
                                    worksheet,
                                    row_index,
                                    col_index,
                                    percentage_string,  # Manually formatted percentage with %
                                    style=BuiltinStyles.BAD
                                )
                        else:
                            self.excelWriter.write(
                                worksheet,
                                row_index,
                                col_index,
                                percentage_string  # Manually formatted percentage with %
                            )

                    case "PERCENTS":
                        # Convert the metric value to a float
                        metric_value = float(el[metric_key])

                        # If the value is greater than 1, it's likely not in percentage form, so divide by 100
                        if metric_value > 1:
                            metric_value /= 100

                        # Format the percentage value as a string with a "%" symbol
                        percentage_string = f"{metric_value * 100:.1f}%"

                        # Write the percentage string to the worksheet directly
                        if metric_threshold:
                            if metric_value >= metric_threshold:
                                self.excelWriter.write(
                                    worksheet,
                                    row_index,
                                    col_index,
                                    percentage_string,  # Manually formatted percentage with %
                                    style=BuiltinStyles.BAD
                                )
                            else:
                                self.excelWriter.write(
                                    worksheet,
                                    row_index,
                                    col_index,
                                    percentage_string,  # Manually formatted percentage with %
                                    style=BuiltinStyles.GOOD
                                )
                        else:
                            self.excelWriter.write(
                                worksheet,
                                row_index,
                                col_index,
                                percentage_string  # Manually formatted percentage with %
                            )

                    case "RATING":
                        rating_number = int(float(el[metric_key]))
                        rating = const.SONAR_RATING_MAPPING[rating_number]
                        if metric_threshold:
                            if metric_threshold >= rating:
                                self.excelWriter.write_number(
                                    worksheet,
                                    row_index,
                                    col_index,
                                    rating,
                                    number_format=self.NUM_FORMAT_INTEGER,
                                    style=BuiltinStyles.GOOD,
                                )
                            else:
                                self.excelWriter.write_number(
                                    worksheet,
                                    row_index,
                                    col_index,
                                    rating,
                                    number_format=self.NUM_FORMAT_INTEGER,
                                    style=BuiltinStyles.BAD,
                                )
                        else:
                            self.excelWriter.write_number(
                                worksheet,
                                row_index,
                                col_index,
                                rating,
                                number_format=self.NUM_FORMAT_INTEGER,
                            )
                    case "WORK_DURATION":
                        self.excelWriter.write_number(
                            worksheet,
                            row_index,
                            col_index,
                            int(el[metric_key]),
                            number_format=self.NUM_FORMAT_INTEGER,
                        )
                    case _:
                        self.excelWriter.write(worksheet, row_index, col_index, el[metric_key])

                col_index += 1

            # Write Sonar Project Name
            self.excelWriter.write(
                worksheet,
                row_index,
                1,
                el.get(const.K_NAME, "Unknown Project"),
            )

            # Write to which team the Sonar Project belongs, if any
            self.excelWriter.write(
                worksheet,
                row_index,
                2,
                el.get(const.K_BELONGS, "unknown"),
            )

            # Write if this is a production repository of the team
            self.excelWriter.write(
                worksheet,
                row_index,
                3,
                bool(el.get(const.K_IS_PROD, False)),
            )

            col_index = self.COL_START_INDEX_TO_POPULATE_METRICS
            row_index+=1