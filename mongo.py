from pymongo import MongoClient



client = MongoClient("mongodb://localhost:27017/")
db = client["TaskManager"]
tasks_collection = db["tasks"]
users_collection =db["users"]

def get_tasks():
    
    tasks = list(tasks_collection.find({'isCompleted': False}).sort('createdAt', -1))
    return tasks

def get_users():
    return list(users_collection.find({},{'_id':0, 'user_id':1, 'user_name':1, 'user_password':1, 'user_role':1, 'task_ids':1}))

def add_user(user_id,user_name,user_pass,user_role):
    users_collection.insert_one({'user_id':user_id,'user_name': user_name,'user_password':user_pass,'user_role': user_role, 'task_ids': []})

def get_tasks_with_username():
    tasks = tasks_collection.find()
    for task in tasks:
        user_id = task.get('assignedTo')
        user = users_collection.find_one({'_id': user_id})
        task['assignedTo'] = user['user_name'] if user else None
    return tasks
   

def create_task(task_data):
  tasks_collection.insert_one(task_data)

def update_task(task_id, new_description, new_priority,user_name):
    task=tasks_collection.find_one({'taskId':task_id})
    if task:
        current_username=task.get('assignedTo')
        if current_username!=user_name:
          users_collection.update_one({'user_name':current_username}, {'$pull':{'task_ids':task_id}}) 
          users_collection.update_one({'user_name':user_name},{'$push':{'task_ids':task_id}})  
   
    tasks_collection.update_one({'taskId': task_id}, {'$set': {'task': new_description, 'priorityLevel': new_priority,'assignedTo':user_name}})

# def delete_task(task_id):
    
#     tasks_collection.delete_one({'taskId': task_id})

def mark_task_as_completed(task_id):
   
    tasks_collection.update_one({'taskId': task_id}, {'$set': {'isCompleted': True}})

def get_completed_tasks():
    
    completed_tasks = list(tasks_collection.find({'isCompleted': True}).sort('createdAt', -1))
    return completed_tasks

def reopen_task(task_id):
   
    tasks_collection.update_one({'taskId': task_id}, {'$set': {'isCompleted': False}})

def update_user_task(task_id, user_name):
   
    users_collection.update_one({'user_name': user_name}, {'$push': {'task_ids': task_id}})

def delete_task(task_id): 
    task = tasks_collection.find_one({'taskId': task_id})
  
    if task:
        user_name = task['assignedTo']
        
    
        tasks_collection.delete_one({'taskId': task_id})
        
       
        users_collection.update_one({'user_name': user_name}, {'$pull': {'task_ids': task_id}})


def get_tasks_by_user(user_name):
    user = users_collection.find_one({'user_name': user_name})
    if user and 'task_ids' in user:
        task_ids = user['task_ids']
        tasks = list(tasks_collection.find({'taskId': {'$in': task_ids}}))
        return tasks
    return []        