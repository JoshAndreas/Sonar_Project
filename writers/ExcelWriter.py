from .ExcelOpenPyxl import ExcelOpenPyxl


class Font:
  TYPE_NAME = "Font"

  def __init__(self, name="Calibri", size=11, bold=False, italic=False, color="FF000000"):
    self.name = name
    self.size = size
    self.bold = bold
    self.italic = italic
    self.color = color

  def __str__(self) -> str:
    return f"{self.TYPE_NAME}({self.name},{self.size},{self.bold},{self.italic},{self.color})"


class Alignment:
  TYPE_NAME = "Alignment"

  def __init__(self, horizontal="general", vertical="bottom", text_rotation=0, indent=0):
    self.horizontal = horizontal
    self.vertical = vertical
    self.text_rotation = text_rotation
    self.indent = indent

  def __str__(self) -> str:
    return f"{self.TYPE_NAME}({self.horizontal},{self.vertical},{self.text_rotation},{self.indent})"


class PatternFill:
  TYPE_NAME = "PatternFill"

  def __init__(self, fill_type="solid", start_color=None, end_color=None):
    self.fill_type = fill_type
    self.start_color = start_color
    self.end_color = end_color

  def __str__(self) -> str:
    return f"{self.TYPE_NAME({self.fill_type},{self.start_color},{self.end_color})}"


class ExcelWriter:
  writer = None
  #
  # WORKBOOK METHODS
  #

  def __init__(self, excel_writer_pkg):
    self.writer = self.__factory(excel_writer_pkg)

  def __factory(self, excel_writer_pkg="None"):
    excel_writers = {"openpyxl": ExcelOpenPyxl}
    return excel_writers[excel_writer_pkg]()

  def create_workbook(self, workbook_file_name):
    return self.writer.create_workbook(workbook_file_name)

  def open_workbook(self, workbook_file_name):
    return self.writer.open_workbook(workbook_file_name)

  def close_workbook(self, workbook):
    self.writer.close_workbook(workbook)

  def add_worksheet(self, workbook, worksheet_name):
    return self.writer.add_worksheet(workbook, worksheet_name)

  def delete_worksheet(self, workbook, worksheet_name):
    self.writer.delete_worksheet(workbook, worksheet_name)

  def exist_worksheet(self, workbook, worksheet_name):
    return True if worksheet_name in workbook.sheetnames else False

  def get_worksheet_by_name(self, workbook, worksheet_name):
    return self.writer.get_worksheet_by_name(workbook, worksheet_name)

  def add_format(self, workbook, format):
    return self.writer.add_format(workbook, format)

  def autofit_columns(self, worksheet):
    self.writer.autofit_columns(worksheet)

  def filter_columns(self, worksheet, column_range):
    self.writer.filter_columns(worksheet, column_range)

  def write(self, worksheet, row_index, col_index, data, style=None):
    self.writer.write(worksheet, row_index, col_index, data, style)

  def write_number(self, worksheet, row_index, col_index, data, number_format=None, style=None):
    self.writer.write_number(worksheet, row_index, col_index, data, number_format, style)

  def register_style(self, workbook, style_name, **kwargs):
    self.writer.register_style(workbook, style_name, **kwargs)
