import sqlite3

#opening or creating the database 'bookstore' and creating a cursor object
db = sqlite3.connect('bookstore')
cursor = db.cursor()

############################################### SETTING UP THE TABLE AND INSERTING STARTING DATA ###############################################

#using try/except function to create table called 'books'. Will rollback if the table already exists. 
try:
    cursor.execute('''
    CREATE TABLE books (
        id INTEGER PRIMARY KEY UNIQUE,
        title TEXT,
        author TEXT,
        qty INTEGER
    )
    ''')
    db.commit()
except Exception:
    db.rollback()

books_list = [(3001, 'A Tale of Two Cities', 'Charles Dickens', 30), (3002, 'Harry Potter and the Philosophers Stone', 'J.K. Rowling', 40), (3003, 'The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 25), (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37), (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)]

#uses list above to add books into the table. id is the primary key and has the UNIQUE constraint so the books can't be added once already in. Will rollback if that is the case. 
try:
    cursor.executemany('''
    INSERT INTO books(id, title, author, qty)
        VALUES(?,?,?,?)
    ''', books_list)
    db.commit()
except Exception:
    db.rollback()

############################################### FUNCTIONS FOR MENU OF APP ###############################################

#Function to enter new book.
def enter_book():
    book_id = -1
    book_qty = -1
    #using while loop and try/except to get a valid input from user. ID and quantity needs to be a number or will return invalid input. 
    while book_id == -1:
        try:
            book_id = int(input('\nWhat is the ID of the book?:\n'))
        except Exception:
            print('Invalid input. Please enter a number.')
    book_title = input('\nWhat is the name of the book?:\n')
    book_author = input('\nWhat is the name of the author?:\n')
    while book_qty == -1:
        try:
            book_qty = int(input('\nHow many of these books do you have?:\n'))
        except Exception:
            print('Invalid input. Please enter a number.')
#inserting the new data into the table and commiting the change 
    cursor.execute('''
        INSERT INTO books(id, title, author, qty)
            VALUES (?,?,?,?)
''', (book_id, book_title, book_author, book_qty))
    print(f'\n{book_title} was added to the database successfully!\n')
    db.commit()



def update_book():
    ask_again = True
    #asking for ID using the same while loop and try/except method - needs to be a number input from user
    while ask_again:
        try:
            book_to_update = int(input('\nPlease enter the ID of the book you want to update:\n'))
            #using SELECT 1 function to see if the id the user has entered returns any rows from the table.
            cursor.execute('''
                    SELECT 1 FROM books
                    WHERE id = ?
''', (book_to_update,))
            book_check = cursor.fetchall()
            #if it doesn't return a result, len will 0 and will ask for another ID as book cannot be found
            if len(book_check) == 0:
                print('\nBook not found. Please enter a valid ID.\n')
            #if something is returned, then it will ask for a quantity and break while loop
            else:
                book_update = int(input('\nWhat is the new quantity?:\n'))                
                ask_again = False
        except Exception:
            print('\nInvalid input\n')
    #updates the value in the table 
    cursor.execute('''
        UPDATE books
        SET qty = ?
        WHERE id = ?
''', (book_update, book_to_update))
    print(f'\nThe quantity for book ID {book_to_update} has been updated.\n')
    db.commit()


def delete_book():
    ask_again = True
    #using same method as the above function to prevent errors with user input and checking if function returns a result. 
    while ask_again:
        try:
            book_to_delete = int(input('\nPlease enter the ID of the book you want to delete:\n'))
            cursor.execute('''
                SELECT 1 FROM books
                WHERE id = ?
''', (book_to_delete,))
            book_check = cursor.fetchall()
            if len(book_check) == 0:
                print('\nBook not found. Please try again.\n')
            else:
                ask_again = False
        except Exception:
            print('\nInvalid input\n')
    #deletes the row from the table.
    cursor.execute('''
        DELETE FROM books
        WHERE id = ? 
''', (book_to_delete, ))
    print('\nBook has been deleted.\n')
    db.commit()


def search_book():
    ask_again = True
    #uses while loop to ask for the method of search. 
    while ask_again:
        book_info = input('''
Please pick an option from below: 
    
    a - Search by ID
    b - Search by Name
    c - Search by Author
    d - Back to menu
''').lower()
        if book_info == 'a':
            #searching by ID
            try:
                search_id = int(input('\nPlease enter the ID you wish to search for:\n'))
                cursor.execute('''
                    SELECT * FROM books
                    WHERE id = ?
''', (search_id,))
                #getting a result if found and stripping the () around it. Then will split the string by ', ' to get a list where each item will be the different bits of information about the book
                search_list = cursor.fetchall()
                result = str(search_list[0])
                result_strip = result.strip('()')
                result_list = result_strip.split(', ')
                #will print the information of the book onto the terminal and then break while loop
                print(f'''
Book Title: {result_list[1]}
Book Author: {result_list[2]}
Quantity Left: {result_list[3]}
''')
                ask_again = False
                #will print book not found if not able to find a book with that ID 
            except Exception:
                print('\nBook not found.\n')
        elif book_info == 'b':
            #Search by book name
            try:
                search_name = input('\nEnter the name of the book you wish to search for:\n')
                #uses lower() function to get rid of case sensitivity with user's input
                cursor.execute('''
                    SELECT * FROM books
                    WHERE lower(title) = ?
''', (search_name.lower(),))
                search_list = cursor.fetchall()
                #if doesn't return a result, will print error message. 
                if len(search_list) == 0:
                    print('\nBook not found.\n')
                else:
                    #there can be books with the same name (title column in table does not have UNIQUE constraint) so uses for loop to get details of all of them and print. Will break while loop after.
                    for n in search_list:
                        result = str(n)
                        result_strip = result.strip('()')
                        result_list = result_strip.split(', ')
                        print(f'''
    Book ID: {result_list[0]}
    Book Author: {result_list[2]}  
    Quantity left: {result_list[3]}                 
    ''')
                    ask_again = False
            except Exception:
                print('\nBook not found.\n')
        elif book_info == 'c':
            #Search by author - can return multiple results so uses the same method as above (for searching by name)
            try:
                search_author = input('\nEnter the name of the author you wish you search for:\n')
                cursor.execute('''
                    SELECT * FROM books
                    WHERE lower(author) = ?
''', (search_author.lower(),))
                search_list = cursor.fetchall()
                if len(search_list) == 0:
                    print('\nBook not found.\n')
                else:
                    for n in search_list:
                        result = str(n)
                        result_strip = result.strip('()')
                        result_list = result_strip.split(', ')
                        print(f'''
    Book ID: {result_list[0]}
    Book Name: {result_list[1]}
    Quantity Left: {result_list[3]}
''')
            except Exception:
                print('Book not found.')
        elif book_info == 'd':
            pass
            ask_again = False
        else:
            print('\nInvalid input. Please try again.\n')


############################################### RUNNING THE APPLICATION MENU ###############################################


print('''
***************** WELCOME TO THE BOOKSTORE DATABASE *****************
''')
should_continue = True

while should_continue:
    try:
        user_choice = int(input('''
Please pick an option from the menu below:

1 - Enter book
2 - Update book
3 - Delete book
4 - Search book 
0 - Exit
'''))
        if user_choice == 1: 
            enter_book()
        elif user_choice == 2:
            update_book()
        elif user_choice == 3:
            delete_book()
        elif user_choice == 4:
            search_book()
        elif user_choice == 0:
            print('\nGoodbye!\n')
            db.close()
            should_continue = False
        else:
            print('\nInvalid choice. Please try again.')
    except Exception: 
        print('\nInvalid choice. Please try again.')

