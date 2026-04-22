def check_availability(doctor, date):
    # fake data for now
    return ["10:00 AM", "2:00 PM", "4:30 PM"]


def book_appointment(doctor, date, time):
    return f"Appointment booked with {doctor} at {time} on {date}"


def cancel_appointment():
    return "Your appointment has been cancelled"