from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


manager = Blueprint('manager', __name__)

# return all employees 
@manager.route('/employee', methods=['GET'])
def get_all_employee():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute('SELECT * FROM employee')

    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in 
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers. 
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))
        
    return jsonify(json_data)

# return all tasks 
@manager.route('/task/<employeeId>', methods=['GET'])
def get_all_task(employeeId):
    # get a cursor object from the database
    cursor = db.get_db().cursor()
    
    # Constructing the query
    query = 'SELECT * FROM task WHERE employeeId = %s'
    current_app.logger.info(query)
    
    # executing and committing the update statement
    cursor = db.get_db().cursor()
    cursor.execute(query, (employeeId))
    db.get_db().commit()

    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in 
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers. 
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))
        
    return jsonify(json_data)

# add a task
@manager.route('/task', methods=['POST'])
def add_new_task():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)
    
    
    taskId = the_data['taskId']
    description = the_data['description']
    dueDate = the_data['dueDate']
    status = the_data['status']
    employeeId = the_data['employeeId']

    # Constructing the query
    query = 'insert into task (taskId, description, dueDate, status, employeeId) values ("'
    query += str(taskId) + '", "'
    query += str(description) + '", "'
    query += str(dueDate) + '", "'
    query += str(status) + '", '
    query += str(employeeId) + ')'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

# update employee role
@manager.route('/employee/<employeeId>/<role>', methods=['PUT'])
def update_role(employeeId, role):

    # Extracting variables
    employeeId = employeeId
    role = role

    # Constructing the query
    query = 'UPDATE employee SET roleTitle = %s WHERE employeeId = %s'
    current_app.logger.info(query)

    # executing and committing the update statement
    cursor = db.get_db().cursor()
    cursor.execute(query, (role, employeeId))
    db.get_db().commit()

    return 'Success!'


