from flask import request, jsonify
from datetime import datetime
from config import app, db
from models import task_schema, Task, tasks_schema

# Create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    title = request.json['title']
    description = request.json['description']
    due_date = request.json['due_date']

    new_task = Task(title, description, due_date)
    db.session.add(new_task)
    db.session.commit()

    return task_schema.jsonify(new_task)

# Retrieve a single task by its ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    return task_schema.jsonify(task)

# Update an existing task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)

    title = request.json['title']
    description = request.json['description']
    due_date = datetime.strptime(request.json['due_date'], '%d-%m-%Y').date()
    status = request.json['status']

    task.title = title
    task.description = description
    task.due_date = due_date
    task.status = status
    db.session.commit()

    return task_schema.jsonify(task)

# Delete a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()

    return task_schema.jsonify(task)

# List all tasks with pagination support
@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    tasks = Task.query.paginate(page=page, per_page=per_page)
    result = tasks_schema.dump(tasks.items)

    return jsonify({
        'tasks': result,
        'total_pages': tasks.pages,
        'current_page': tasks.page,
        'has_next': tasks.has_next,
        'has_prev': tasks.has_prev
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)