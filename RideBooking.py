class RideBooking:
    rates = {"Bike": 20, "Sedan": 40, "SUV": 60, "Premium": 100}
    drivers = {"Bike": True, "Sedan": True, "SUV": True, "Premium": True}

    def book(self, customer, pickup, drop, distance, passengers,
             vehicle, hour, discount=0):
        if distance <= 0:
            raise ValueError("Invalid distance")
        if vehicle not in self.rates:
            raise ValueError("Invalid vehicle")
        if passengers <= 0 or passengers > 6:
            raise ValueError("Invalid passenger count")
        if hour < 0 or hour > 23:
            raise ValueError("Invalid booking time")
        if not self.drivers.get(vehicle, False):
            raise ValueError("Driver unavailable")

        base = self.rates[vehicle]
        fare = base + distance * 10
        if 17 <= hour <= 20:
            fare *= 1.25
        if hour >= 22 or hour < 6:
            fare *= 1.15
        fare += max(0, passengers - 1) * 20
        fare -= min(fare * discount / 100, fare)

        return round(fare, 2), vehicle