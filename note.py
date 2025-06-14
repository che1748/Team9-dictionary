def take_notes(word, notes):
    '''This functions takes a word and the related notes as input and store 
    the information in a local SQLite database. The table stores three pieces of information:
    the word, the note, and the time.
    '''
    from datetime import datetime
    current_timme = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    import sqlite3
    con = sqlite3.connect("dic_note.db")
    cur = con.cursor()

    # Check if table exists before creating
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='note'")
    table_exists = cur.fetchone()

    if not table_exists:
        # Create table only if it doesn't exist
        cur.execute("CREATE TABLE note(word, notes, time)")
        print("Created new 'note' table")
    else:
        print("'note' table already exists")

    #res = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='note'")
    #print("Tables in database:", res.fetchone())

    # add notes into the database
    cur.execute("INSERT INTO note (word, notes, time) VALUES (?,?,?)",
            (word, notes, current_timme)  )


    con.commit()
    con.close()

def display_notes():
    import sqlite3
    con = sqlite3.connect('dic_note.db')
    cur = con.cursor()

    cur.execute("SELECT word, notes, time FROM note ORDER BY time")
    notes = cur.fetchall()
    
    con.close()
    return notes

def delete_note(word):
    import sqlite3
    con = sqlite3.connect('dic_note.db')
    cur = con.cursor()

    cur.execute("DELETE FROM note WHERE word = ?", (word))

    con.commit()
    con.close()

import sqlite3

def delete_all_notes():
    con = sqlite3.connect('dictionary.db')
    cur = con.cursor()
    
    # Delete all records from notes table
    cur.execute("DELETE FROM note")
    
    # Reset auto-increment counter (SQLite specific)
    cur.execute("DELETE FROM sqlite_sequence WHERE name='note'")
    
    con.commit()
    con.close()
    print("All notes deleted successfully")
