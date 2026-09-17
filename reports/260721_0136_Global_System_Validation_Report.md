# Global E2E and CI/CD Validation Report
**Date:** 2026-07-21 01:12:05

| Repository | Local E2E Tests | Git Push | CI/CD Status |
|------------|-----------------|----------|--------------|
| Dental_000 | Skipped | Success | FAIL |
| Dental_001 | Pass | Success | FAIL |
| Dental_002 | FAIL | Success | FAIL |
| Dental_003 | Pass | Success | Pass |
| Dental_004 | FAIL | Success | FAIL |
| Dental_005 | FAIL | Success | FAIL |
| Dental_006 | Pass | Success | FAIL |
| Dental_007 | Pass | Success | FAIL |
| Dental_008 | Pass | FAIL | Skipped |
| Dental_009 | Pass | Success | Pass |
| Dental_010 | Pass | Success | Pass |
| Dental_011 | Pass | Success | FAIL |
| Dental_012 | Pass | Success | FAIL |
| Dental_013 | Pass | Success | FAIL |
| Dental_014 | Pass | FAIL | Skipped |
| Dental_Panoramic_Reader | Pass | Success | Pass |

## Dental_000
**Local Tests:** Skipped
**Push:** Push successful
**CI/CD:** CI/CD FAILED

## Dental_001
**Local Tests:** Pass
**Push:** Push successful
**CI/CD:** CI/CD FAILED

## Dental_002
**Local Tests:** FAIL
**Push:** Push successful
**CI/CD:** CI/CD FAILED
```text

=================================== ERRORS ====================================
________________ ERROR collecting tests/tests_002/test_core.py ________________
ImportError while importing test module 'D:\Github\Dental_000\tests\tests_002\test_core.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.11_3.11.2544.0_x64__qbz5n2kfra8p0\Lib\importlib\__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
C:\Users\chema\Github\Dental_000\tests\tests_002\test_core.py:10: in <module>
    ???
E   ModuleNotFoundError: No module named 'dentex_caries'
=========================== short test summary info ===========================
ERROR tests/tests_002/test_core.py
!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
1 error in 0.21s

```

## Dental_003
**Local Tests:** Pass
**Push:** Push successful
**CI/CD:** CI/CD SUCCESS

## Dental_004
**Local Tests:** FAIL
**Push:** Push successful
**CI/CD:** CI/CD FAILED
```text

=================================== ERRORS ====================================
______________ ERROR collecting tests/tests_004/test_dataset.py _______________
ImportError while importing test module 'D:\Github\Dental_000\tests\tests_004\test_dataset.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.11_3.11.2544.0_x64__qbz5n2kfra8p0\Lib\importlib\__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
C:\Users\chema\Github\Dental_000\tests\tests_004\test_dataset.py:12: in <module>
    ???
E   ModuleNotFoundError: No module named 'pano_clear'
_______________ ERROR collecting tests/tests_004/test_device.py _______________
ImportError while importing test module 'D:\Github\Dental_000\tests\tests_004\test_device.py'.
Hint: make sure your test modules/packages have valid Python names.
Trace
```

## Dental_005
**Local Tests:** FAIL
**Push:** Push successful
**CI/CD:** CI/CD FAILED
```text
F                                                                        [100%]
================================== FAILURES ===================================
________________________________ test_imports _________________________________

>   ???
E   ModuleNotFoundError: No module named 'alphadent'

C:\Users\chema\Github\Dental_000\tests\tests_005\test_imports.py:21: ModuleNotFoundError

During handling of the above exception, another exception occurred:

>   ???
E   Failed: Import failed: No module named 'alphadent'

C:\Users\chema\Github\Dental_000\tests\tests_005\test_imports.py:32: Failed
=========================== short test summary info ===========================
FAILED tests/tests_005/test_imports.py::test_imports - Failed: Import failed:...
1 failed in 1.65s

```

## Dental_006
**Local Tests:** Pass
**Push:** Push successful
**CI/CD:** CI/CD FAILED

## Dental_007
**Local Tests:** Pass
**Push:** Push successful
**CI/CD:** CI/CD Timeout

## Dental_008
**Local Tests:** Pass
**Push:** Push failed: remote: error: Trace: 7e1e97f83b69c9fdee478d938e6a0e938189f5510e3e2d7a05f0aaaedc2901c6        
remote: error: See https://gh.io/lfs for more information.        
remote: error: File models/best.onnx is 104.20 MB; this exceeds GitHub's file size limit of 100.00 MB        
remote: error: GH001: Large files detected. You may want to try Git Large File Storage - https://git-lfs.github.com.        
To https://github.com/HyunchanAn/Dental_008.git
 ! [remote rejected] HEAD -> main (pre-receive hook declined)
error: failed to push some refs to 'https://github.com/HyunchanAn/Dental_008.git'

**CI/CD:** Skipped due to push failure

## Dental_009
**Local Tests:** Pass
**Push:** Push successful
**CI/CD:** CI/CD SUCCESS

## Dental_010
**Local Tests:** Pass
**Push:** Push successful
**CI/CD:** CI/CD SUCCESS

## Dental_011
**Local Tests:** Pass
**Push:** Push successful
**CI/CD:** CI/CD Timeout

## Dental_012
**Local Tests:** Pass
**Push:** Push successful
**CI/CD:** CI/CD Timeout

## Dental_013
**Local Tests:** Pass
**Push:** Push successful
**CI/CD:** CI/CD Timeout

## Dental_014
**Local Tests:** Pass
**Push:** Push failed: error: The destination you provided is not a full refname (i.e.,
starting with "refs/"). We tried to guess what you meant by:

- Looking for a ref that matches 'HEAD' on the remote side.
- Checking if the <src> being pushed ('HEAD')
  is a ref in "refs/{heads,tags}/". If so we add a corresponding
  refs/{heads,tags}/ prefix on the remote side.

Neither worked, so we gave up. You must fully qualify the ref.
hint: The <src> part of the refspec is a commit object.
hint: Did you mean to create a new branch by pushing to
hint: 'HEAD:refs/heads/HEAD'?
error: failed to push some refs to 'https://github.com/HyunchanAn/Dental_014.git'

**CI/CD:** Skipped due to push failure

## Dental_Panoramic_Reader
**Local Tests:** Pass
**Push:** Push successful
**CI/CD:** CI/CD SUCCESS
