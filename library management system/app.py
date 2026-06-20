from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from datetime import date

app = Flask(__name__)

# Database Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',      # Change this to your MySQL username
    'password': 'root', # Change this to your MySQL password
    'database': 'library_db'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# --- Routes ---

@app.route('/')
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Total Books
    cursor.execute("SELECT COUNT(*) FROM books")
    total_books = cursor.fetchone()[0]
    
    # 2. Total Members
    cursor.execute("SELECT COUNT(*) FROM members")
    total_members = cursor.fetchone()[0]

    # 3. Issued Books
    cursor.execute("SELECT COUNT(*) FROM books WHERE status = 'Issued'")
    issued_books = cursor.fetchone()[0]

    # 4. Transactions/Reports (Last 5 issues)
    cursor.execute("""
        SELECT 
            t.issue_date, b.title AS book_title, m.name AS member_name 
        FROM transactions t
        JOIN books b ON t.book_id = b.book_id
        JOIN members m ON t.member_id = m.member_id
        WHERE t.return_date IS NULL
        ORDER BY t.issue_date DESC
        LIMIT 5
    """)
    recent_transactions = cursor.fetchall()
    
    conn.close()

    # The existing index.html route is now the dashboard.
    return render_template('index.html', 
                           total_books=total_books, 
                           total_members=total_members, 
                           issued_books=issued_books,
                           recent_transactions=recent_transactions)

# Remaining routes (books, members, issue_book, return_book) stay the same as before.

@app.route('/books', methods=['GET', 'POST'])
def books():
    # ... (Keep the content of the books route from the previous answer)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        cursor.execute("INSERT INTO books (title, author) VALUES (%s, %s)", (title, author))
        conn.commit()
    
    cursor.execute("SELECT * FROM books ORDER BY title ASC")
    books = cursor.fetchall()
    conn.close()
    return render_template('books.html', books=books)


@app.route('/members', methods=['GET', 'POST'])
def members():
    # ... (Keep the content of the members route from the previous answer)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cursor.execute("INSERT INTO members (name, email) VALUES (%s, %s)", (name, email))
        conn.commit()

    cursor.execute("SELECT * FROM members ORDER BY name ASC")
    members = cursor.fetchall()
    conn.close()
    return render_template('members.html', members=members)


@app.route('/issue', methods=['GET', 'POST'])
def issue_book():
    # ... (Keep the content of the issue_book route from the previous answer)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        book_id = request.form['book_id']
        member_id = request.form['member_id']
        today = date.today()
        
        # Update book status
        cursor.execute("UPDATE books SET status = 'Issued' WHERE book_id = %s", (book_id,))
        # Log transaction
        cursor.execute("INSERT INTO transactions (book_id, member_id, issue_date) VALUES (%s, %s, %s)", (book_id, member_id, today))
        conn.commit()
        return redirect(url_for('books'))

    # Fetch available books and members for dropdowns
    cursor.execute("SELECT * FROM books WHERE status = 'Available' ORDER BY title ASC")
    available_books = cursor.fetchall()
    cursor.execute("SELECT * FROM members ORDER BY name ASC")
    members_list = cursor.fetchall()
    conn.close()
    
    return render_template('issue.html', books=available_books, members=members_list)


@app.route('/return/<int:book_id>')
def return_book(book_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    today = date.today()
    
    # 1. Update book status
    cursor.execute("UPDATE books SET status = 'Available' WHERE book_id = %s", (book_id,))
    # 2. Update transaction record with return date
    cursor.execute("UPDATE transactions SET return_date = %s WHERE book_id = %s AND return_date IS NULL", (today, book_id))
    
    conn.commit()
    conn.close()
    return redirect(url_for('books'))

if __name__ == '__main__':
    app.run(debug=True)