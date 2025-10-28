import sys
import os
import csv

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def _is_number(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False


def read_csv_file(debug=False):

    """
    Data is formated as follows:
    station_rows: list of list each containing ["StationRow", line, station]
    e.g. ['StationRow', 'Bakerloo', 'Harrow & Wealdstone']
    edge_rows: list of list each containing ["EdgeRow", line, a, b, t] - t (numeric text)
    e.g. ['EdgeRow', 'Bakerloo', 'Harrow & Wealdstone', 'Kenton', '2']

    if debug:
        It will dump the data to console to sanity check the data.
        Otherwise it will just return the data in their coresponding lists - StationRows, EdgeRows.
    """

    # Dynamically find the CSV file relative to project root (works on all machines)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(project_root, 'task2', 'Weighted_test_data.csv')
    
    # Initialize lists to avoid UnboundLocalError
    StationRows = []
    EdgeRows = []
    
    try:
        with open(csv_path, 'r', encoding='utf-8', newline='') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader, start=1):
                cells = [c.strip() for c in row]

                if not any(cells):
                    continue

                if len(cells) >= 2 and cells[1] != "":
                    line = cells[0] or "Missing Line"
                    station = cells[1]
                    if len(cells) < 4 or (len(cells) >= 4 and cells[2] == "" and (len(cells) < 4 or cells[3] == "")):
                        StationRows.append(["StationRow", line, station])
                        continue

                if len(cells) >= 4 and cells[1] != "" and cells[2] != "" and _is_number(cells[3]):
                    line = cells[0] or "Missing Line"
                    a, b, t = cells[1], cells[2], cells[3]
                    EdgeRows.append(["EdgeRow", line, a, b, t])
                    continue

    except Exception as e:
        print(e)

    if not debug:
        return StationRows, EdgeRows
    else:
        print("Data extracted successfully")
        print("StationRows: \n", StationRows)
        print("EdgeRows: \n", EdgeRows)
        return StationRows, EdgeRows
