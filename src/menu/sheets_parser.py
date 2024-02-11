import openpyxl


def get_rows() -> list[list[str]]:
    book = openpyxl.load_workbook('admin/MenuSheets.xlsx', read_only=True)
    sheet = book.active
    cells = sheet['A1':'G18']  # type: ignore
    values = [[e.value for e in cell] for cell in cells]
    book.close()

    return values
