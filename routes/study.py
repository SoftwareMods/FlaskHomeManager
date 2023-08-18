"""Routes for tools"""
import json
import os
from flask import Blueprint, flash, redirect, request, session, Response # last one use for overriding and passing NAVIGATION to all templates
from markupsafe import escape
from helpers.common import render_template, loadJSONFromFile, saveJSONToFile, getNewId
from helpers.study import subjects_file
from random import shuffle

study = Blueprint('study', __name__)

# Our index-page just shows a quick explanation. Check out the template
# "templates/index.html" documentation for more details.
@study.route('/study', methods=['POST','GET'])
def index():
    """"default landing page"""

    mysubjects = loadJSONFromFile(subjects_file)
    subject_id = getNewId(mysubjects)

    subject_info = {}
    if request.method == "POST":
        subject = request.form.get('study-subject')
        subject_info = {"id": subject_id, "name": subject, "score": 0, "questions": []}
        #print(f"Adding new subject: {subject_info}")
        mysubjects.append(subject_info)
        saveJSONToFile(subjects_file, mysubjects)

    return render_template('study/index.html', sidebar=True, tables=True, mysubjects=loadJSONFromFile(subjects_file))

@study.route('/study/review/<int:subject_id>', methods=['POST','GET'])
def review(subject_id):
    """"default landing page"""

    mysubjects = loadJSONFromFile(subjects_file)
    for i in range(len(mysubjects)):
        if mysubjects[i]['id'] == subject_id:
            subject = mysubjects[i]
            shuffle(mysubjects[i]['questions'])
            break

    return render_template('study/review-questions.html', sidebar=True, tables=True, subject=subject, mysubjects=mysubjects)


@study.route('/study/delete/<int:this_id>', methods=['GET','POST'])
def delete_task(this_id):
    """"delete given subject"""

    deleted = False
    mysubjects = loadJSONFromFile(subjects_file)
    for i in range(len(mysubjects)):
        if mysubjects[i]['id'] == this_id:
            name = mysubjects[i]['name']
            del mysubjects[i]
            saveJSONToFile(subjects_file, mysubjects)
            deleted = True
            break

    if deleted:
        flash(f'Successfully deleted subject {name}', 'success')
    else:
        flash(f'Failed to delete subject {name}', 'error')

    return redirect(f'/study')

@study.route('/study/add-questions/<int:subject_id>', methods=['POST','GET'])
def add(subject_id):
    """"Add questions to given subject"""

    mysubjects = loadJSONFromFile(subjects_file)
    for i in range(len(mysubjects)):
        if mysubjects[i]['id'] == subject_id:
            subject = mysubjects[i]
            subject_questions = subject['questions']
            break

    qid = getNewId(subject_questions)
    update_question = ""

    if request.method == "POST":

        incorrect_answers = []
        for key in request.form.keys():
            if 'new-incorrect-answer_' in key:
                value = request.form.get(key)
                if value != "":
                    incorrect_answers.append(value)

        if len(incorrect_answers) == 0:
            # Process question with single correct answer
            question = request.form.get('new-exact-question')
            print(question)
            answer   = request.form.get('new-exact-answer')
            for i in range(len(mysubjects)):
                if mysubjects[i]['id'] == subject_id:
                    if request.form.get('AddQuestion'):
                        mysubjects[i]['questions'].append({"id": qid, "question": question, "answer": answer})
                    elif request.form.get('UpdateQuestion'):
                        #print(f"Update: {mysubjects[i]}")
                        question_id = int(request.form.get('question_id'))
                        for q in range(len(mysubjects[i]['questions'])):
                            if question_id == mysubjects[i]['questions'][q]['id']:
                                print(f"Update here: {mysubjects[i]['questions'][q]} - {question}")
                                mysubjects[i]['questions'][q]['question'] = question
                                mysubjects[i]['questions'][q]['answer'] = answer
                                break
                    saveJSONToFile(subjects_file, mysubjects)
                    subject=mysubjects[i]
        else:
            # Process question with multiple choice
            question = request.form.get('new-multi-question')
            answer   = request.form.get('new-multi-answer')
            for i in range(len(mysubjects)):
                if mysubjects[i]['id'] == subject_id:
                    if request.form.get('AddQuestion'):
                        mysubjects[i]['questions'].append({"id": qid, "question": question, "answer": answer, "incorrect_answers": incorrect_answers})
                    elif request.form.get('UpdateQuestion'):
                        question_id = int(request.form.get('question_id'))
                        for q in range(len(mysubjects[i]['questions'])):
                            if question_id == mysubjects[i]['questions'][q]['id']:
                                print(f"Update {mysubjects[i]['questions'][q]}")
                                mysubjects[i]['questions'][q]['question'] = question
                                mysubjects[i]['questions'][q]['answer'] = answer
                                mysubjects[i]['questions'][q]['incorrect_answers'] = incorrect_answers
                                break
                    saveJSONToFile(subjects_file, mysubjects)
                    subject=mysubjects[i]

    elif request.method == 'GET':
        if request.args.get('update'):
            update_id = int(request.args.get('update'))
            for q in subject_questions:
                if q['id'] == update_id:
                    update_question = q
                    print(f"Updating {q}")

    return render_template('study/add-questions.html', sidebar=True, tables=True, subject=subject, update_question=update_question)

@study.route('/study/delete-question/<int:subject_id>/<int:question_id>', methods=['GET','POST'])
def delete_question(subject_id,question_id):
    """"delete given question"""

    print((subject_id,question_id))
    deleted = False
    mysubjects = loadJSONFromFile(subjects_file)
    for i in range(len(mysubjects)):
        if mysubjects[i]['id'] == subject_id:
            for q in range(len(mysubjects[i]['questions'])):
                if question_id == mysubjects[i]['questions'][q]['id']:
                    del mysubjects[i]['questions'][q]
                    saveJSONToFile(subjects_file,mysubjects)
                    deleted = True
                    break

    if deleted:
        flash('Successfully deleted question', 'success')
    else:
        flash('Failed to delete question', 'error')

    return redirect(f'/study/add-questions/{subject_id}')