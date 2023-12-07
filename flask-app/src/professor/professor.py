#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 21:03:36 2023

@author: giannidiarbi
"""

from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db

professor = Blueprint('professor', __name__)

# return all students 
@professor.route('/student', methods=['GET'])
def get_all_student():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute('SELECT * FROM student')

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

# return all attendance info for students in ac particular section
@professor.route('/attendance/<attendanceId>', methods=['GET'])
def view_attendance(attendanceId):
    # get a cursor object from the database
    cursor = db.get_db().cursor()
    
    # use cursor to query the database for a list of products
    cursor.execute('''SELECT * FROM attendance 
                   JOIN onus.studentAttendance ON attendance.attendanceId = attendance.attendanceId = studentAttendance.attendanceId 
                   JOIN section ON studentAttendance.sectionId =''' + str(attendanceId))
    
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

# return a list of all courses taughts by a professor
@professor.route('/courses/<profId>', methods=['GET'])
def view_exam_dates(profId):
    # get a cursor object from the database
    cursor = db.get_db().cursor()
    
    # use cursor to query the database for a list of products
    cursor.execute('SELECT examId, date, FROM exam WHERE profId =' + str(profId))
    
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

# return a list of all homework due dates for a particular course
@professor.route('/courses/<courseID>/exams/date', methods=['GET'])
def view_homework_dates(courseId):
    # get a cursor object from the database
    cursor = db.get_db().cursor()
    
    # use cursor to query the database for a list of products
    cursor.execute('SELECT homeworkId, dueDate from homeworkAssignment WHERE courseID =' + str(courseId))
    
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

# update department
@professor.route('/professor/<profId>/<department>', methods=['PUT'])
def update_year(profId, department):

    # Extracting variables
    profId = profId
    department = department

    # Constructing the query
    query = 'UPDATE professor SET department = %s WHERE profId = %s'
    current_app.logger.info(query)

    # executing and committing the update statement
    cursor = db.get_db().cursor()
    cursor.execute(query, (department, profId))
    db.get_db().commit()

    return 'Success!'

# remove a professor who retired
@professor.route('/professor/<profId>', methods=['DELETE'])
def remove_prof(profId):
    # Constructing the delete query
    query = f'DELETE FROM professor WHERE profId =' + str(profId)
    
    # executing and committing the delete statement
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    # Check if any row was affected (meeting was deleted)
    if cursor.rowcount == 0:
        return jsonify({'error': 'Professor not found'}), 404
    
    return 'Professor removed successfully'

# add an exam to a course
@professor.route('/exam/<examId>', methods=['POST'])
def create_exam(examId, courseId):
     # collecting data from the request object 
     the_data = request.json
     current_app.logger.info(the_data)

     #extracting the variable
     examId = the_data['examId']

     # Constructing the query
     query = 'insert into exam (examId) values (" WHERE courseId = {courseId}'
     query += examId + '", "'
     current_app.logger.info(query)

     # executing and committing the insert statement 
     cursor = db.get_db().cursor()
     cursor.execute(query)
     db.get_db().commit()
     
     return 'Success!'

