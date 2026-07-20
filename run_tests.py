import importlib
import inspect
import traceback
import sys

import pkgutil

# Discover all test_*.py modules under the tests package
TEST_MODULES = []
for finder, name, ispkg in pkgutil.iter_modules(["tests"]):
    if name.startswith("test_"):
        TEST_MODULES.append(f"tests.{name}")

def run():
    total = 0
    failed = 0
    for mod_name in TEST_MODULES:
        try:
            mod = importlib.import_module(mod_name)
        except Exception:
            print(f"FAILED to import {mod_name}")
            traceback.print_exc()
            failed += 1
            continue

        for name, obj in inspect.getmembers(mod, inspect.isfunction):
            if name.startswith("test_"):
                total += 1
                try:
                    obj()
                    print(f"PASS: {mod_name}.{name}")
                except AssertionError:
                    failed += 1
                    print(f"FAIL: {mod_name}.{name} (AssertionError)")
                    traceback.print_exc()
                except Exception:
                    failed += 1
                    print(f"FAIL: {mod_name}.{name} (Exception)")
                    traceback.print_exc()

    print(f"\nRan {total} tests: {total-failed} passed, {failed} failed")
    if failed:
        sys.exit(1)

if __name__ == "__main__":
    run()
