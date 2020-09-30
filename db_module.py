import sqlite3

db = sqlite3.connect("vera_logs.db")
cur = db.cursor()

db.execute("CREATE TABLE IF NOT EXISTS chat_log (message_id INT,message_text STRING,author_id INT,author_username STRING, server_name STRING, server_id INT, response_generated STRING, timestamp STRING)")
db.commit()

def add_chatlog(message,response):

    message_text = message.content
    message_id = message.id
    author_id = message.author.id
    author_username = message.author.name
    if message.guild == None:
        server_name = author_username+" DM's"
        server_id = author_id
    else:
        server_name = message.guild.name
        server_id = message.guild.id
    response = str(response)
    timestamp = message.created_at
    db.execute("INSERT INTO chat_log (message_id,message_text,author_id,author_username,server_name,server_id,response_generated,timestamp) VALUES (?,?,?,?,?,?,?,?)",(message_id,message_text,author_id,author_username,server_name,server_id,response,timestamp))
    db.commit()
