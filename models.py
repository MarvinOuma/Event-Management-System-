from datetime import datetime
from typing import List, Optional

class User:
    def __init__(self, user_id: int, name: str, email: str, password: str, role: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.role = role  # "Organizer" or "Attendee"
        self.events: List['Event'] = []
        self.tickets: List['Ticket'] = []
        self.feedbacks: List['Feedback'] = []

    def login(self, email: str, password: str) -> bool:
        return self.email == email and self.password == password

    def register(self) -> bool:
        return True

    def update_profile(self, name: str = None, email: str = None):
        if name: self.name = name
        if email: self.email = email

class Venue:
    def __init__(self, venue_id: int, name: str, address: str, capacity: int):
        self.venue_id = venue_id
        self.name = name
        self.address = address
        self.capacity = capacity
        self.events: List['Event'] = []

    def check_availability(self, date: datetime) -> bool:
        return not any(event.date.date() == date.date() for event in self.events)

class Event:
    def __init__(self, event_id: int, title: str, description: str, date: datetime, location: str, venue: Venue, organizer: User):
        self.event_id = event_id
        self.title = title
        self.description = description
        self.date = date
        self.location = location
        self.venue = venue
        self.organizer = organizer
        self.tickets: List['Ticket'] = []
        self.feedbacks: List['Feedback'] = []

    def create_event(self) -> bool:
        if self.venue.check_availability(self.date):
            self.venue.events.append(self)
            self.organizer.events.append(self)
            return True
        return False

    def update_event(self, title: str = None, description: str = None, date: datetime = None):
        if title: self.title = title
        if description: self.description = description
        if date: self.date = date

    def cancel_event(self) -> bool:
        self.venue.events.remove(self)
        return True

class Ticket:
    def __init__(self, ticket_id: int, ticket_type: str, price: float, event: Event):
        self.ticket_id = ticket_id
        self.ticket_type = ticket_type  # "VIP", "Regular"
        self.price = price
        self.event = event
        self.user: Optional[User] = None
        self.payment: Optional['Payment'] = None

    def book_ticket(self, user: User) -> bool:
        self.user = user
        user.tickets.append(self)
        self.event.tickets.append(self)
        return True

    def cancel_ticket(self) -> bool:
        if self.user:
            self.user.tickets.remove(self)
        return True

class Payment:
    def __init__(self, payment_id: int, amount: float, payment_date: datetime, status: str, ticket: Ticket):
        self.payment_id = payment_id
        self.amount = amount
        self.payment_date = payment_date
        self.status = status  # "Paid", "Pending"
        self.ticket = ticket
        ticket.payment = self

    def make_payment(self) -> bool:
        self.status = "Paid"
        return True

    def refund_payment(self) -> bool:
        self.status = "Refunded"
        return True

class Feedback:
    def __init__(self, feedback_id: int, rating: int, comment: str, user: User, event: Event):
        self.feedback_id = feedback_id
        self.rating = rating
        self.comment = comment
        self.user = user
        self.event = event

    def submit_feedback(self) -> bool:
        self.user.feedbacks.append(self)
        self.event.feedbacks.append(self)
        return True