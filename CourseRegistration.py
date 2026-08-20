class CourseRegistration:
    courses = {
        "DBMS": (4, "Programming"),
        "AI": (4, "Data Structures"),
        "ML": (3, "Statistics"),
        "Cloud": (3, "Networking")
    }

    def __init__(self):
        self.registered = []

    def register(self, course, prerequisites):
        if course not in self.courses:
            return "Invalid course"
        if course in self.registered:
            return "Duplicate registration"

        credit, req = self.courses[course]

        if req and req not in prerequisites:
            return "Missing prerequisite"

        if sum(self.courses[c][0] for c in self.registered) + credit > 8:
            return "Credit limit exceeded"

        self.registered.append(course)
        return "Registration successful"

    def credits(self):
        return sum(self.courses[c][0] for c in self.registered)