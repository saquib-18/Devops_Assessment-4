class ICUAllocation:
    def __init__(self, beds):
        self.beds = beds
        self.patients = {}
        self.waiting = []

    def add_patient(self, pid, age, oxygen, heart, bp, temp,
                    conditions="", emergency=False):
        if pid in self.patients:
            raise ValueError("Duplicate patient ID")
        if not 0 <= oxygen <= 100:
            raise ValueError("Invalid oxygen level")
        if not 30 <= heart <= 200:
            raise ValueError("Invalid heart rate")

        score = (100 - oxygen) + abs(heart - 75) + max(0, 120 - bp)
        if conditions:
            score += 10

        if emergency:
            priority = "CRITICAL"
            score += 100
        elif score >= 80:
            priority = "CRITICAL"
        elif score >= 50:
            priority = "HIGH"
        elif score >= 25:
            priority = "MEDIUM"
        else:
            priority = "LOW"

        self.patients[pid] = {"score": score, "priority": priority}

        if self.beds > 0:
            self.beds -= 1
            return f"{priority}: ICU bed allocated"
        self.waiting.append(pid)
        return f"{priority}: Added to waiting list"

    def get_priority(self, pid):
        return self.patients[pid]["priority"]