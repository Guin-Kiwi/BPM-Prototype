"""Dependency-free request isolation and structural response validation."""
import json
import math


def build_user_payload(request, classes):
    if not isinstance(request, dict) or set(request) != {'scores', 'farmer_note', 'weather'}:
        raise ValueError('request must contain only scores, farmer_note and weather')
    scores = request['scores']
    if not isinstance(scores, list) or len(scores) != len(classes) or not classes or len(set(classes)) != len(classes):
        raise ValueError('invalid candidate scores or classes')
    if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) or not 0 <= x <= 1 for x in scores) or abs(sum(scores) - 1) > 0.000001:
        raise ValueError('invalid score distribution')
    note = request['farmer_note']
    if note is not None and (not isinstance(note, str) or len(note) > 2000):
        raise ValueError('invalid note')
    weather = request['weather']
    if weather is not None and not isinstance(weather, dict):
        raise ValueError('invalid weather')
    payload = json.dumps({'candidates': [{'name': name, 'score': score} for name, score in zip(classes, scores)], 'farmer_note': note, 'weather': weather}, ensure_ascii=False, allow_nan=False, separators=(',', ':'))
    if '<|' in payload or len(payload.encode()) > 12000:
        raise ValueError('invalid or oversized payload')
    return payload


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate key')
        result[key] = value
    return result


def validate_response(raw, classes, request):
    if not isinstance(raw, str) or len(raw.encode('utf-8')) > 4096:
        return ['output exceeds size limit or is not text']
    try:
        value = json.loads(raw, object_pairs_hook=_unique_object, parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite number')))
    except (ValueError, TypeError):
        return ['invalid JSON or duplicate key']
    keys = {'schema_version', 'suspected_issue', 'warning', 'note_relation', 'limitations', 'weather_used'}
    if not isinstance(value, dict) or set(value) != keys:
        return ['incorrect fields']
    errors = []
    if value['schema_version'] != 'uc002-interpretation-1': errors.append('schema_version')
    if value['suspected_issue'] not in [*classes, 'unknown']: errors.append('suspected_issue')
    if value['warning'] not in ['none', 'insufficient_evidence', 'unsupported_issue', 'unknown']: errors.append('warning')
    if value['note_relation'] not in ['consistent', 'contradictory', 'not_provided', 'unknown']: errors.append('note_relation')
    note = request['farmer_note']
    if (not note or not note.strip()) != (value['note_relation'] == 'not_provided'): errors.append('note_relation does not match input')
    limitations = value['limitations']
    if not isinstance(limitations, list) or not 1 <= len(limitations) <= 4 or any(not isinstance(x, str) or not x.strip() or len(x) > 200 for x in limitations): errors.append('limitations')
    if type(value['weather_used']) is not bool or (request['weather'] is None and value['weather_used'] is not False): errors.append('weather_used')
    return errors
