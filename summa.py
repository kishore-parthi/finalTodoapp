from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import uuid
from celery import Celery
import mongo

app = Flask(__name__)
app.secret_key = 'lalpurb126745'

# Configure Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

def check_login():
    if 'user' not in session:
        return False
    return True

def get_tasks(selected_user):
    if selected_user == "All Users":
        return mongo.get_tasks()
    else:
        return mongo.get_tasks_by_user(selected_user)
    

def read_all_tasks():
    users = mongo.get_users()
    tasks = mongo.get_tasks()
    return render_template('home.html', tasks=tasks, users=users, selected_user='All Users')


@app.route('/', methods=['GET','POST'])
def read():
    if not check_login():
        return redirect(url_for('login'))
    
    users = mongo.get_users()
    
    if request.method == 'POST':
        selected_user = request.form.get('user_name')
        session['selected_user'] = selected_user
        return redirect(url_for('read'))

    if session.get('selected_user'):
        selected_user = session['selected_user']
        tasks = get_tasks(selected_user)
        session['selected_user']= None
    else:
        return read_all_tasks()

    return render_template('home.html', tasks=tasks, users=users, selected_user=selected_user)


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = mongo.get_users()
        for user in users:
            if user['user_name'] == username and user['user_password'] == password:
                session['user'] = username
                return redirect(url_for('read'))
        flash('Invalid username or password')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('selected_user', None)
    return redirect(url_for('login'))


@app.route('/add_user', methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        uuid_id = str(uuid.uuid4())
        user_id = uuid_id.replace('-', '')
        user_name = request.form['user_name']
        user_pass = request.form['password']
        user_role = request.form['user_role']
        add_user_task.delay(user_id, user_name, user_pass, user_role)
        return redirect('/')
    return render_template('addUsers.html')
    

@app.route('/create', methods=['POST'])
def create():
    description = request.form.get('description')
    prioritylevel = request.form.get('prioritylevel')
    uuid_id = str(uuid.uuid4())
    task_id = uuid_id.replace('-', '')
    current_date = datetime.now().isoformat()
    is_completed = False
    user_name = request.form.get('user_name') 

    task_data = {
        'taskId': task_id,
        'task': description,
        'priorityLevel': prioritylevel,
        'createdAt': current_date,
        'isCompleted': is_completed,
        'assignedTo': user_name
    }
    create_task_task.delay(task_data)
    update_user_task_task.delay(task_data['taskId'], task_data['assignedTo'])
    return redirect('/')

@app.route('/update_task', methods=['POST'])
def update_task():
    task_id = request.form.get('task_id')
    new_description = request.form.get('new_description')
    new_priority = request.form.get('new_priority')
    user_name = request.form.get('edit-user_name')
    update_task_task.delay(task_id, new_description, new_priority, user_name)
    return redirect('/')

@app.route('/delete_task', methods=['POST'])
def delete_task():
    task_id = request.form.get('task_id_delete')
    delete_task_task.delay(task_id)
    return redirect('/')

@app.route('/done_task', methods=['POST'])
def done_task():
    task_id = request.form.get('task_id_done')
    mark_task_as_completed_task.delay(task_id)
    return redirect('/')

@app.route('/completedtasks', methods=['GET'])
def completed_tasks():
    if 'user' not in session:
        return redirect(url_for('login'))
    completed_tasks = mongo.get_completed_tasks()
    return render_template('completedtask.html', completed_tasks=completed_tasks)

@app.route('/reopen_task', methods=['POST'])
def reopen_task():
    task_id = request.form.get('reopen_task_id')
    reopen_task_task.delay(task_id)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

# Celery Tasks
@celery.task
def add_user_task(user_id, user_name, user_pass, user_role):
    mongo.add_user(user_id, user_name, user_pass, user_role)

@celery.task
def create_task_task(task_data):
    mongo.create_task(task_data)

@celery.task
def update_task_task(task_id, new_description, new_priority, user_name):
    mongo.update_task(task_id, new_description, new_priority, user_name)

@celery.task
def delete_task_task(task_id):
    mongo.delete_task(task_id)

@celery.task
def mark_task_as_completed_task(task_id):
    mongo.mark_task_as_completed(task_id)

@celery.task
def reopen_task_task(task_id):
    mongo.reopen_task(task_id)

@celery.task
def update_user_task_task(task_id, user_name):
    mongo.update_user_task(task_id, user_name)
