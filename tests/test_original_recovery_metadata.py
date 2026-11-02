"""Public recovery metadata integrity; never imports or executes recovered HTML."""
import collections
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/original-recovery'
def read(name):
    return json.loads((BASE / name).read_text())

def test_feature_classifications_and_dimensions():
    data = read('FEATURE_MATRIX.json')
    assert len({f['id'] for f in data['features']}) == len(data['features'])
    assert dict(collections.Counter(f['implementation_status'] for f in data['features'])) == data['summary']
    required = {'original_source_availability', 'current_runtime_activation', 'preservation_completeness', 'test_verification_status', 'security_review_status', 'schema_inputs', 'schema_outputs', 'evidence_references'}
    assert all(required <= f.keys() for f in data['features'])
    assert all(f['implementation_status'] != 'ACTIVE' for f in data['features'])

def test_financial_findings_are_separate_from_ui_labels():
    features = read('FEATURE_MATRIX.json')['features']
    by_name = {f['feature_name']: f for f in features}
    assert by_name['Dedicated bank OTP extraction']['implementation_status'] == 'UI_ONLY'
    assert by_name['UPI transaction recognition']['implementation_status'] == 'NOT_IMPLEMENTED'
    assert by_name['Card metadata and credential parsing']['private_review_reference']
    assert all(f['security_review_status'].startswith('STATIC_REVIEW_ONLY') for f in features if f['category'] == 'financial')

def test_artifact_identity_is_not_normalized_into_false_authenticity():
    files = {f['file']: f for f in read('RECOVERY_MANIFEST.json')['files']}
    assert sum(f['historical_exact_match'] for f in files.values()) == 3
    assert files['4-index.html']['sha256'] == files['2-200.html']['sha256']
    assert files['4-index.html']['normalized_lf_sha256'] != files['4-index.html']['historical_sha256']
    assert not files['4-index.html']['historical_exact_match']

def test_safe_public_configs_match_original_hashes():
    for f in read('RECOVERY_MANIFEST.json')['files']:
        if f['public_source_path']:
            assert hashlib.sha256((ROOT / f['public_source_path']).read_bytes()).hexdigest() == f['sha256']
        else:
            assert f['file'] not in {'1-surgeignore', '3-CNAME'}

def test_function_graph_metadata_references_valid_nodes():
    index = read('FUNCTION_INDEX.json')
    graph = read('DEPENDENCY_GRAPH.json')
    assert sum(len(a['functions']) for a in index['artifacts']) == index['functions_total']
    for artifact, calls in zip(index['artifacts'], graph['artifacts']):
        assert artifact['file'] == calls['file']
        ids = {f['id'] for f in artifact['functions']}
        assert len(ids) == len(artifact['functions'])
        assert all(e['from'] in ids for e in calls['edges'])
        assert all(e['to'] in ids for e in calls['edges'] if e['kind'] == 'contains')
        assert all(f['start_line'] <= f['end_line'] and len(f['source_line_slice_sha256']) == 64 for f in artifact['functions'])

def test_no_source_bodies_or_credentials_in_public_graph():
    # Explicit metadata schema: any accidental AST/body export is a publication failure.
    graph = read('DEPENDENCY_GRAPH.json')
    assert all(set(a) <= {'file', 'scripts_parsed', 'edges', 'application_calls', 'application_variables', 'application_schema_property_names'} for a in graph['artifacts'])
    index = read('FUNCTION_INDEX.json')
    assert all('body' not in f and 'code' not in f for a in index['artifacts'] for f in a['functions'])

def test_ui_storage_timer_anchors_reference_function_index():
    index = {a['file']: a for a in read('FUNCTION_INDEX.json')['artifacts']}
    for artifact in read('UI_STORAGE_TIMER_INDEX.json')['artifacts']:
        ids = {f['id'] for f in index[artifact['file']]['functions']}
        for record in artifact['event_bindings'] + artifact['storage_calls'] + artifact['timers'] + artifact['jsx_elements']:
            assert record['line'] > 0
            assert record.get('owner_function') is None or record['owner_function'] in ids
        assert all(r['inline_function'] is None or r['inline_function'] in ids for r in artifact['event_bindings'])
