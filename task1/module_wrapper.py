from task1.data_extract import read_csv_file
from clrsPython.Chapter11.chained_hashtable import ChainedHashTable

def norm(s: str) -> str:
    """Normalise strings for key lookup."""
    return " ".join((s or "").strip().split()).casefold()


class StationRecord:
    """
    Container stored in the CLRS hashtable.
    No data-structure logic here — just attributes.

    Attributes:
        key - normalised station name (lookup key)
        id - enumerated index of the station
        name - original station name
        lines - set of line names this station belongs to
        neighbors - dict: neighbor_id - (time_minutes:int, line_name:str|None)
        active - boolean indicating if the station is active/operational
    """
    __slots__ = ("key", "id", "name", "lines", "neighbors", "active")

    def __init__(self, name: str, id_: int):
        self.key = norm(name)
        self.id = id_
        self.name = name
        self.lines = set()
        self.neighbors = {}
        self.active = True


def _unwrap(node_or_obj):
    """If the CLRS search returns a linked-list node, unwrap its .data."""
    return getattr(node_or_obj, "data", node_or_obj)


def build_index_from_rows(station_rows, edge_rows):
    """
    Build the station index in two passes using the CLRS ChainedHashTable.

    Args:
        station_rows: List["StationRow", line, station]
        edge_rows: List["EdgeRow", line, a, b, t] (t is numeric text)

    Returns:
        hashtable: CLRS table keyed by normalised name - StationRecord
        records_by_id: List[StationRecord] indexed by station id
    """
    ht = ChainedHashTable(m=1021, get_key_func=lambda x: x.key)
    records_by_id = []

    def get_or_create(station_name: str) -> StationRecord:
        k = norm(station_name)
        found = ht.search(k)
        if found is not None:
            return _unwrap(found)
        rec = StationRecord(name=station_name, id_=len(records_by_id))
        ht.insert(rec)
        records_by_id.append(rec)
        return rec

    for tag, line, station in station_rows:
        rec = get_or_create(station)
        if line:
            rec.lines.add(line)

    for tag, line, a, b, t in edge_rows:
        try:
            time_min = int(float(t))
        except ValueError:
            continue

        ra = get_or_create(a)
        rb = get_or_create(b)

        if line:
            ra.lines.add(line)
            rb.lines.add(line)

        prev = ra.neighbors.get(rb.id)
        if prev is None or time_min < prev[0]:
            ra.neighbors[rb.id] = (time_min, line)

        prev = rb.neighbors.get(ra.id)
        if prev is None or time_min < prev[0]:
            rb.neighbors[ra.id] = (time_min, line)

    return ht, records_by_id
