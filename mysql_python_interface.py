import mysql.connector
import json
from dotenv import dotenv_values

env = dotenv_values(".env")
HOST = env["host"]
SQL_USERNAME = env["sql_username"]
SQL_PASSWORD = env["sql_password"]
DATABASE = env["database"]

def connectDB():
    mydb = mysql.connector.connect(
      host= HOST,
      user= SQL_USERNAME,
      passwd= SQL_PASSWORD,
      database= DATABASE # you may use this some other time
    )

    mycursor = mydb.cursor()
    return mydb, mycursor

def insert_into_db(tag, value, table):
    sql = "INSERT INTO "+table+" VALUES (%s, %s);"
    val = (tag,value)

    db_vars = connectDB()
    mydb = db_vars[0]
    mycursor = db_vars[1]

    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    print(sql, val)
    mycursor.close()

def read_from_db(table,attributes):
    sql = "SELECT "+attributes+" FROM "+table+";"

    db_vars = connectDB()
    mydb = db_vars[0]
    mycursor = db_vars[1]

    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    mycursor.close()

    return myresult

def read_from_db_with_condition(table,attributes,condition):
    sql = "SELECT "+attributes+" FROM "+table+" where "+condition+";"

    db_vars = connectDB()
    mydb = db_vars[0]
    mycursor = db_vars[1]

    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    mycursor.close()

    return myresult

def write_json_into_db(json_file_name): #use this function if you need to insert new infos from a json file
    with open(json_file_name) as file:
        data = json.load(file)

    for intent in data['intents']:
        for pattern in intent['patterns']:
            insert_into_db(intent['tag'],pattern,"tag_patterns")

        for response in intent['responses']:
            insert_into_db(intent['tag'],response,"tag_responses")

    print("Successfully done")
