"""Deployment orchestration in temporary directories with injected callbacks; never the VPS."""
import hashlib
from pathlib import Path
import importlib.util
import stat
import pytest
spec=importlib.util.spec_from_file_location('otp_deploy',Path(__file__).resolve().parents[1]/'deployment/deploy_otp_fix.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
Deployment,DeploymentError=module.Deployment,module.DeploymentError

@pytest.fixture
def setup(tmp_path):
    original=b'# isolated original\n';patched=b'# isolated patched\n'
    target=tmp_path/'auth_api.py';target.write_bytes(original);target.chmod(0o640)
    candidate=tmp_path/'candidate.py';candidate.write_bytes(patched)
    backups=tmp_path/'backups';backups.mkdir(mode=0o700)
    calls=[]
    deploy=Deployment(target,backups,candidate,hashlib.sha256(original).hexdigest(),hashlib.sha256(patched).hexdigest(),lambda:calls.append('preflight'),lambda:calls.append('restart'),lambda:True)
    return deploy,original,patched,calls


def test_apply_backup_metadata_and_idempotent_repeat(setup):
    deploy,original,patched,calls=setup
    deploy.apply()
    assert deploy.target.read_bytes()==patched
    backup=list(deploy.backups.glob('*.py'));assert len(backup)==1
    assert backup[0].read_bytes()==original
    assert stat.S_IMODE(backup[0].stat().st_mode)==0o600
    assert stat.S_IMODE(deploy.target.stat().st_mode)==0o640
    assert calls.count('restart')==1
    deploy.apply();assert calls.count('restart')==1
    assert len(list(deploy.backups.glob('*.py')))==1


def test_dependency_failure_cannot_change_source(setup):
    deploy,original,_,calls=setup
    def fail():raise DeploymentError('Synthetic preflight failure')
    deploy.preflight=fail
    with pytest.raises(DeploymentError):deploy.apply()
    assert deploy.target.read_bytes()==original and calls==[]
    assert list(deploy.backups.iterdir())==[]


def test_health_failure_rolls_back_and_restarts_original(setup):
    deploy,original,_,calls=setup
    states=iter([True,False,True]);deploy.healthy=lambda:next(states)
    with pytest.raises(DeploymentError,match='original source restored'):deploy.apply()
    assert deploy.target.read_bytes()==original
    assert calls.count('restart')==2


def test_failed_restart_triggers_rollback(setup):
    deploy,original,_,calls=setup
    def restart():
        calls.append('restart')
        if calls.count('restart')==1:raise DeploymentError('Synthetic restart failure')
    deploy.restart=restart
    with pytest.raises(DeploymentError,match='original source restored'):deploy.apply()
    assert deploy.target.read_bytes()==original and calls.count('restart')==2


def test_drift_and_candidate_tamper_are_refused(setup):
    deploy,original,_,calls=setup
    deploy.target.write_bytes(b'# unrelated source\n')
    with pytest.raises(DeploymentError,match='Source drift'):deploy.apply()
    assert calls==[]
    deploy.target.write_bytes(original);deploy.candidate.write_bytes(b'# tampered candidate\n')
    with pytest.raises(DeploymentError,match='Candidate'):deploy.apply()
    assert deploy.target.read_bytes()==original and calls==[]


def test_unhealthy_predeployment_service_cannot_change_source(setup):
    deploy,original,_,calls=setup;deploy.healthy=lambda:False
    with pytest.raises(DeploymentError,match='Predeployment'):deploy.apply()
    assert deploy.target.read_bytes()==original
    assert list(deploy.backups.iterdir())==[] and 'restart' not in calls


def test_explicit_rollback_checks_backup_and_is_idempotent(setup):
    deploy,original,_,calls=setup;deploy.apply()
    backup=next(deploy.backups.glob('*.py'))
    deploy.rollback(backup);assert deploy.target.read_bytes()==original
    assert calls.count('restart')==2
    deploy.rollback(backup);assert calls.count('restart')==2


def test_rollback_refuses_backup_outside_protected_directory(setup,tmp_path):
    deploy,original,patched,calls=setup;deploy.apply()
    outside=tmp_path/'outside.py';outside.write_bytes(original)
    with pytest.raises(DeploymentError,match='verified original backup'):deploy.rollback(outside)
    assert deploy.target.read_bytes()==patched and calls.count('restart')==1


def test_symlink_target_cannot_be_overwritten(setup,tmp_path):
    deploy,original,_,calls=setup
    real=tmp_path/'actual.py';real.write_bytes(original)
    deploy.target.unlink();deploy.target.symlink_to(real)
    with pytest.raises(DeploymentError,match='regular file'):deploy.apply()
    assert real.read_bytes()==original and calls==[]


def test_candidate_change_during_preflight_cannot_replace_target(setup):
    deploy,original,_,calls=setup
    deploy.preflight=lambda:deploy.candidate.write_bytes(b'# unexpected change\n')
    with pytest.raises(DeploymentError,match='Candidate changed'):deploy.apply()
    assert deploy.target.read_bytes()==original
    assert list(deploy.backups.iterdir())==[] and calls==[]
