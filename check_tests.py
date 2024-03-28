import os
import json

def check_test_outputs(n):
    # Load test data
    b2 = json.load(open('swe-bench.json'))
    pass_to_pass = b2[n]['PASS_TO_PASS']
    fail_to_pass = b2[n]['FAIL_TO_PASS']

    # Read the last 100 lines of the test log file
    with open(f'{n}.txt', 'r') as f:
        lines = f.readlines()[-150:]

    if "No module named" in "\n".join(lines):
        return None

    failed = []

    # Check PASS_TO_PASS tests
    for test in pass_to_pass:
        if not any(test.split('::', 1)[-1] in line and ('PASS' in line or (' ok' in line)) for line in lines):
            failed.append(test)

    # Check FAIL_TO_PASS tests
    for test in fail_to_pass:
        if not any(test in line and ('FAIL' in line or 'ERROR' in line) for line in lines):
            #pass
            return False

    if failed:
        #print(f'Failed tests: {failed}')
        return False
    return True

if __name__ == '__main__':
    passed = 0
    failed = 0
    for n in range(100, 146): # (1150, 1220):  # Iterate over the range of n values
    #for n in range(1150, 1220):  # Iterate over the range of n values
        if os.path.exists(f'{n}.txt'):
            result = check_test_outputs(n)
            print(f'Test {n}: {"Passed" if result else ("Skip" if result is None else "Failed")}')
            if result:
                passed += 1
            else:
                failed += (result is False)
    print(f'Passed: {passed}, Failed: {failed}')
    print(f'Pass rate: {passed / (passed + failed) * 100:.2f}%')
