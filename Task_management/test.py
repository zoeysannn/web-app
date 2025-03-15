import csv

def get_data():
    tasks = []
    with open('data.csv', 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            tasks.append(row)
    return tasks

def add_data(task):
    fields = ['id', 'title', 'description', 'date', 'status', 'completed']
    filename = "data.csv"
    with open(filename,'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writerow(task)
    return "done"

print(get_data())
#task={"id": 3, "title": "task", "description": "task", "date": "2021-09-01", "status": "task", "completed": False}

task={'id': 2, 'title': 'alskdhlkasjdkl', 'description': 'POASJDOPJDPAOJDPOASJDP', 'date': '22-02-2025', 'status': 'In progress', 'completed': False}


print(add_data(task))