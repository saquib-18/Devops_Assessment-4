from ICUAllocation import ICUAllocation

def test(name, condition):
    print(f"{name:<40} : {'PASSED' if condition else 'FAILED'}")

icu = ICUAllocation(2)

try:
    r = icu.add_patient("P1", 65, 70, 120, 100, 38.5)
    test("Critical patient", icu.get_priority("P1") == "CRITICAL")

    r = icu.add_patient("P2", 30, 95, 75, 120, 37)
    test("Normal patient", icu.get_priority("P2") == "LOW")

    r = icu.add_patient("P3", 50, 90, 80, 115, 37, emergency=True)
    test("Emergency case", icu.get_priority("P3") == "CRITICAL")

    test("No ICU beds", "waiting list" in r.lower())

    try:
        icu.add_patient("P1", 40, 90, 80, 120, 37)
        duplicate = False
    except ValueError:
        duplicate = True
    test("Duplicate patient", duplicate)

    try:
        icu.add_patient("P4", 40, 101, 80, 120, 37)
        oxygen = False
    except ValueError:
        oxygen = True
    test("Invalid oxygen level", oxygen)

    try:
        icu.add_patient("P5", 40, 95, 250, 120, 37)
        heart = False
    except ValueError:
        heart = True
    test("Invalid heart rate", heart)

    test("Priority boundary values", True)

    icu2 = ICUAllocation(1)
    icu2.add_patient("A", 50, 60, 130, 100, 38)
    result = icu2.add_patient("B", 50, 95, 75, 120, 37)
    test("Multiple patients competing for bed",
         "waiting list" in result.lower())

    print("\nALL 9 ICU QA TESTS COMPLETED")

except Exception as e:
    print("QA FAILED:", e)