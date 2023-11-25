from typing import Union
from simple_history.manager import HistoricalQuerySet
from simple_history.models import ModelDelta


def get_history_deltas(historical_records) -> "list[ModelDelta]":
    """
    Process a models HistoricalQuerySet to calculate
    delta between old and new changes
    """
    deltas = []
    if historical_records is not None and id:
        last = historical_records.first()
        for _ in range(historical_records.count()):
            new_record, old_record = last, last.prev_record
            if old_record is not None:
                delta = new_record.diff_against(old_record)
                deltas.append(delta)
                last = old_record
    return deltas


def extract_delta_details(changes: "list[ModelDelta]") -> "list[dict]":
    """
    extract changed information of model object using ModelDelta.
    """
    result = []
    record = {}

    for change in changes:
        if len(change.changed_fields) > 0:
            for change_by_id in change.changes:
                record.update({
                    "id": change.new_record.history_id,
                    "history_date": change.new_record.history_date,
                    "field": change_by_id.field,
                    "old_value": getattr(change_by_id, 'old', None),
                    "new_value": change_by_id.new,
                    "history_user": getattr(
                        change.new_record.history_user,
                        'username',
                        None
                    )
                })
                result.append(record)
                record = {}

    return result


def api_get_history(history: HistoricalQuerySet) -> list[dict]:
    """
    query history table for a given employee and returns queryset
    of historical records.
    """
    changes = get_history_deltas(history)
    result = extract_delta_details(changes)
    return result

def generate_unique_identifier(model_name: str, id: Union[str, int]) -> str:
    prefix_mapping = {
        "Employee": "EMP-",
        "Hardware": "HW-",
        "Laptop": "LAP-",
        "Mobile": "MOB-",
        "HardwareAssignment": "HA-"
    }
    prefix = prefix_mapping.get(model_name, "")
    return f"{prefix}{id:04d}"
