import openpyxl


def get_rows() -> list[list[str]]:
    book = openpyxl.load_workbook('admin/MenuSheets.xlsx', read_only=True)
    sheet = book.active
    values = [[e for e in row] for row in sheet.values]
    book.close()

    return values
