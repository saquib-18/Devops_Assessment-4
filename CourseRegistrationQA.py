from CourseRegistration import CourseRegistration

c = CourseRegistration()

tests = [
    ("Valid registration", c.register("DBMS", ["Programming"]) == "Registration successful"),
    ("Missing prerequisite", c.register("AI", []) == "Missing prerequisite"),
    ("Duplicate registration", c.register("DBMS", ["Programming"]) == "Duplicate registration"),
    ("Invalid course", c.register("XYZ", []) == "Invalid course")
]

for name, result in tests:
    print(f"{name:<25}: {'PASSED' if result else 'FAILED'}")

print("Total credits:", c.credits())