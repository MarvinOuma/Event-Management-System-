from datetime import datetime
from models import User, Venue, Event, Ticket, Payment, Feedback

def main():
    # Create users
    organizer = User(1, "John Doe", "john@example.com", "password123", "Organizer")
    attendee = User(2, "Jane Smith", "jane@example.com", "password456", "Attendee")
    
    # Create venue
    venue = Venue(1, "Convention Center", "123 Main St", 1000)
    
    # Create event
    event_date = datetime(2024, 6, 15, 18, 0)
    event = Event(1, "Tech Conference", "Annual tech conference", event_date, "Downtown", venue, organizer)
    event.create_event()
    
    # Create tickets
    vip_ticket = Ticket(1, "VIP", 150.0, event)
    regular_ticket = Ticket(2, "Regular", 75.0, event)
    
    # Book ticket
    vip_ticket.book_ticket(attendee)
    
    # Make payment
    payment = Payment(1, 150.0, datetime.now(), "Pending", vip_ticket)
    payment.make_payment()
    
    # Submit feedback
    feedback = Feedback(1, 5, "Great event!", attendee, event)
    feedback.submit_feedback()
    
    # Display results
    print(f"Event: {event.title}")
    print(f"Organizer: {organizer.name}")
    print(f"Venue: {venue.name} (Capacity: {venue.capacity})")
    print(f"Tickets booked: {len(event.tickets)}")
    print(f"Payment status: {payment.status}")
    print(f"Feedback rating: {feedback.rating}/5")

if __name__ == "__main__":
    main()