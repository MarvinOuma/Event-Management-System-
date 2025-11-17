from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
from models import User, Venue, Event, Ticket, Payment, Feedback

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# In-memory storage (replace with database in production)
users = {
    1: User(1, "Admin User", "admin@example.com", "admin123", "Admin"),
    2: User(2, "John Organizer", "organizer@example.com", "org123", "Organizer"),
    3: User(3, "Jane Attendee", "attendee@example.com", "att123", "Attendee")
}
venues = {}
events = {}
tickets = {}

@app.route('/')
def home():
    return render_template('index.html', events=list(events.values()))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        for user in users.values():
            if user.login(email, password):
                session['user_id'] = user.user_id
                session['role'] = user.role
                flash(f'Welcome {user.name}!')
                return redirect(url_for('dashboard'))
        
        flash('Invalid credentials!')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!')
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = users[session['user_id']]
    role = session['role']
    
    if role == 'Admin':
        return render_template('admin_dashboard.html', user=user, users=users, events=events)
    elif role == 'Organizer':
        user_events = [e for e in events.values() if e.organizer.user_id == user.user_id]
        return render_template('organizer_dashboard.html', user=user, events=user_events)
    else:  # Attendee
        user_tickets = [t for t in tickets.values() if t.user and t.user.user_id == user.user_id]
        return render_template('attendee_dashboard.html', user=user, tickets=user_tickets)

@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if 'user_id' not in session or session['role'] not in ['Admin', 'Organizer']:
        flash('Access denied!')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date_str = request.form['date']
        location = request.form['location']
        
        venue = Venue(len(venues) + 1, location, location, 1000)
        venues[venue.venue_id] = venue
        
        organizer = users[session['user_id']]
        event_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
        event = Event(len(events) + 1, title, description, event_date, location, venue, organizer)
        event.create_event()
        events[event.event_id] = event
        
        flash('Event created successfully!')
        return redirect(url_for('dashboard'))
    
    return render_template('create_event.html')

@app.route('/event/<int:event_id>')
def event_detail(event_id):
    event = events.get(event_id)
    if not event:
        flash('Event not found!')
        return redirect(url_for('home'))
    return render_template('event_detail.html', event=event)

@app.route('/book_ticket/<int:event_id>', methods=['POST'])
def book_ticket(event_id):
    if 'user_id' not in session:
        flash('Please login to book tickets!')
        return redirect(url_for('login'))
    
    event = events.get(event_id)
    if not event:
        flash('Event not found!')
        return redirect(url_for('home'))
    
    ticket_type = request.form['ticket_type']
    price = 75.0 if ticket_type == 'Regular' else 150.0
    
    attendee = users[session['user_id']]
    ticket = Ticket(len(tickets) + 1, ticket_type, price, event)
    ticket.book_ticket(attendee)
    tickets[ticket.ticket_id] = ticket
    
    payment = Payment(len(tickets), price, datetime.now(), "Paid", ticket)
    payment.make_payment()
    
    flash(f'{ticket_type} ticket booked successfully!')
    return redirect(url_for('dashboard'))

@app.route('/manage_users')
def manage_users():
    if 'user_id' not in session or session['role'] != 'Admin':
        flash('Admin access required!')
        return redirect(url_for('login'))
    return render_template('manage_users.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)