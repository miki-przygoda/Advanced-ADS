"""
This module imports Task 1's loader + index builder and exposes a minimal,
stable API for the rest of the team.

Public functions:
    init_index(force: bool = False) -> None
    is_operational(name: str) -> bool
    get_station_id(name: str) -> int | None
    get_station_name(station_id: int) -> str | None

Notes:
- Uses the CLRS hashtable built by task1.module_wrapper.
- Assumes station lookup keys are the normalised station names.
"""

from __future__ import annotations
from typing import Optional, Tuple, List

from task1.data_extract import read_csv_file
from task1.module_wrapper import build_index_from_rows


def _norm(s: str) -> str:
    """Normalise a station name exactly like Task 1 (trim, collapse spaces, casefold)."""
    return " ".join((s or "").strip().split()).casefold()

def _unwrap(node_or_obj):
    """If the CLRS search returns a linked-list node, unwrap its .data; otherwise return the object."""
    return getattr(node_or_obj, "data", node_or_obj)

_HT = None
_BY_ID: List[object] | None = None


def init_index(force: bool = False) -> None:
    """Build the global index once (idempotent). Call before using other functions."""
    global _HT, _BY_ID
    if _HT is not None and _BY_ID is not None and not force:
        return
    station_rows, edge_rows = read_csv_file()
    _HT, _BY_ID = build_index_from_rows(station_rows, edge_rows)


def is_operational(name: str) -> bool:
    """True if the station exists in the index and is active."""
    if _HT is None or _BY_ID is None:
        init_index()
    hit = _HT.search(_norm(name))
    if hit is None:
        return False
    rec = _unwrap(hit)
    return getattr(rec, "active", True)

def get_station_id(name: str) -> Optional[int]:
    """Return the integer station id for a given name, or None if not found or inactive."""
    if _HT is None or _BY_ID is None:
        init_index()
    hit = _HT.search(_norm(name))
    if hit is None:
        return None
    rec = _unwrap(hit)
    if not getattr(rec, "active", True):
        return None
    return getattr(rec, "id", None)

def get_station_name(station_id: int) -> Optional[str]:
    """Return the station name for a given id, or None if out of range or inactive."""
    if _BY_ID is None or _HT is None:
        init_index()
    if station_id < 0 or station_id >= len(_BY_ID):
        return None
    rec = _BY_ID[station_id]
    if not getattr(rec, "active", True):
        return None
    return getattr(rec, "name", None)


def activate_station(name: str) -> bool:
    """Activate a station. Returns True if successful, False if station not found."""
    if _HT is None or _BY_ID is None:
        init_index()
    hit = _HT.search(_norm(name))
    if hit is None:
        return False
    rec = _unwrap(hit)
    rec.active = True
    return True


def deactivate_station(name: str) -> bool:
    """Deactivate a station. Returns True if successful, False if station not found."""
    if _HT is None or _BY_ID is None:
        init_index()
    hit = _HT.search(_norm(name))
    if hit is None:
        return False
    rec = _unwrap(hit)
    rec.active = False
    return True

def is_station_active(name: str) -> bool:
    """Return True if the station exists and is active, False otherwise."""
    if _HT is None or _BY_ID is None:
        init_index()
    hit = _HT.search(_norm(name))
    if hit is None:
        return False
    rec = _unwrap(hit)
    return getattr(rec, "active", True)


def insert_station(name: str) -> int:
    """Insert a new station. Returns the station ID if successful, -1 if station already exists."""
    if _HT is None or _BY_ID is None:
        init_index()
    
    if is_operational(name):
        return -1
    
    from task1.module_wrapper import StationRecord
    new_id = len(_BY_ID)
    rec = StationRecord(name=name, id_=new_id)
    
    _HT.insert(rec)
    _BY_ID.append(rec)
    
    return new_id


def delete_station_by_name(name: str) -> bool:
    """
    Delete a station by name. Returns True if successful, False if station not found.
    Note: This is a soft delete - sets active=False rather than removing from data structures.
    """
    if _HT is None or _BY_ID is None:
        init_index()
    
    hit = _HT.search(_norm(name))
    if hit is None:
        return False
    
    rec = _unwrap(hit)
    rec.active = False
    return True



def create_edge(a_name: str, b_name: str, time_minutes: int, line: str | None = None, create_missing: bool = False) -> bool:
    """
    Create (or update) an undirected edge between two stations.

    Behavior:
    - If both stations exist, updates their neighbor maps symmetrically.
    - If an edge already exists, keeps the smaller travel time.
    - If `line` is provided, adds it to both stations' `lines` sets.
    - If a station is missing and `create_missing` is True, it will be created.

    Returns True on success, False if stations are missing (and not created) or time is invalid.
    """
    if _HT is None or _BY_ID is None:
        init_index()

    # Validate time
    try:
        t = int(time_minutes)
    except Exception:
        return False
    if t < 0:
        return False

    # Lookup stations
    hit_a = _HT.search(_norm(a_name))
    hit_b = _HT.search(_norm(b_name))

    # Optionally create missing stations
    if hit_a is None and create_missing:
        insert_station(a_name)
        hit_a = _HT.search(_norm(a_name))
    if hit_b is None and create_missing:
        insert_station(b_name)
        hit_b = _HT.search(_norm(b_name))

    if hit_a is None or hit_b is None:
        return False

    ra = _unwrap(hit_a)
    rb = _unwrap(hit_b)

    # Record line membership
    if line:
        ra.lines.add(line)
        rb.lines.add(line)

    # Update neighbors symmetrically (keep min time)
    prev = ra.neighbors.get(rb.id)
    if prev is None or t < prev[0]:
        ra.neighbors[rb.id] = (t, line)

    prev = rb.neighbors.get(ra.id)
    if prev is None or t < prev[0]:
        rb.neighbors[ra.id] = (t, line)

    return True


def get_edge_info(a_name: str, b_name: str):
    """
    Return (time_minutes, line) for the edge a-b if present; otherwise None.
    Uses the global index; builds it on first use.
    """
    if _HT is None or _BY_ID is None:
        init_index()

    hit_a = _HT.search(_norm(a_name))
    hit_b = _HT.search(_norm(b_name))
    if hit_a is None or hit_b is None:
        return None
    ra = _unwrap(hit_a)
    rb = _unwrap(hit_b)
    return ra.neighbors.get(rb.id)


def get_total_station_count() -> int:
    """Return the number of active stations in the global index."""
    if _HT is None or _BY_ID is None:
        init_index()
    return sum(1 for rec in _BY_ID if getattr(rec, "active", True))


def get_all_stations() -> list[tuple[int, str]]:
    """Return a list of (id, name) for all active stations in the global index."""
    if _HT is None or _BY_ID is None:
        init_index()
    return [(rec.id, rec.name) for rec in _BY_ID if getattr(rec, "active", True)]

__all__ = [
    "init_index",
    "is_operational",
    "get_station_id",
    "get_station_name",
    "activate_station",
    "deactivate_station",
    "insert_station",
    "delete_station_by_name",
    "create_edge",
    "get_edge_info",
    "get_total_station_count",
    "get_all_stations",
]
