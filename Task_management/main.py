from flask import Flask
from flask import render_template, request, redirect, url_for
from datetime import datetime
import csv

app=Flask(__name__)

def get_data():
    tasks = []
    with open('data.csv', 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            for key, value in row.items():
                if key == 'id':
                    row[key] = int(value)
                if key == 'title':
                    row[key] = str(value)
                if key == 'description':
                    row[key] = str(value)
                if key == 'date':
                    row[key] = value
                if key == 'status':
                    row[key] = str(value)
                if key == 'completed':
                    if value == 'True':
                        row[key] = True
                    else:
                        row[key] = False
            tasks.append(row)
    return tasks

def add_data(task):
    fields = ['id', 'title', 'description', 'date', 'status', 'completed']
    filename = "data.csv"
    with open(filename,'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writerow(task)

def overwrite_data(tasks):
    fields = ['id', 'title', 'description', 'date', 'status', 'completed']
    filename = "data.csv"
    with open(filename,'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        for task in tasks:
            writer.writerow(task)

@app.route('/')
def home():
    current_date=datetime.today().strftime('%Y-%m-%d')
    return render_template('index.html', tasks=get_data(), current_date=current_date)

@app.route('/add', methods=['POST'])
def add():
        raw_date = request.form['date']
        if raw_date:
            raw_date = datetime.strptime(raw_date, '%Y-%m-%d').strftime('%d-%m-%Y')
        
        new_task={
            "id": int(get_data()[-1]["id"])+1,
            "title": request.form['title'],
            "description": request.form['description'],
            "date": raw_date,
            "status": request.form['status'],
            "completed": False}
        add_data(new_task)
        return redirect(url_for('home'))

@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    tasks=get_data()
    for i in tasks:
        if i["id"]==task_id:
            i["completed"]=True
            break
    overwrite_data(tasks)
    return redirect(url_for('home'))

@app.route("/remove/<int:task_id>")
def delete_task(task_id):
    tasks=get_data()
    for i in tasks:
        if i['id']==task_id:
            tasks.remove(i)
            break
    overwrite_data(tasks)
    return redirect(url_for('home'))

@app.route('/update', methods=['POST'])
def updated():
    tasks=get_data()
    for i in tasks:
        if i['id']==int(request.form['id']):
            i['title']=request.form['title']
            i['description']=request.form['description']
            i['date']=request.form['date']
            i['status']=request.form['status']
            i['completed']=False
    overwrite_data(tasks)
    return redirect(url_for('home'))

@app.route("/editing/<int:task_id>")
def editing(task_id):
    tasks=get_data()
    for i in tasks:
        if i['id']==task_id:
            data=i
            break
    return render_template('edit.html', data=data)

app.run(debug=True)