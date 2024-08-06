// script.js

document.addEventListener("DOMContentLoaded", function() {
    const editBtn = document.querySelector(".edit-btn");
    const editContainer = document.querySelector(".edit-container");
    
    editBtn.addEventListener("click", function() {
        // Hide original content
        const taskRecordArea = document.querySelector(".task-recordarea");
        taskRecordArea.style.display = "none";
        
        // Show edit container
        editContainer.style.display = "block";
    });
    
    const submitEditBtn = document.querySelector(".submit-edit-btn");
    submitEditBtn.addEventListener("click", function() {
        // Show original content
        const taskRecordArea = document.querySelector(".task-recordarea");
        taskRecordArea.style.display = "flex";
        
        // Hide edit container
        editContainer.style.display = "none";
    });
});















// """
// // 1. Page:
// Add_User:
// 	user_id
// 	user_name
// 	role - user/admin (select option)
//         task_ids [task_id1, task_id2]
        
// --> user collection created

// 2. create task - user - select option

// 3. create_task - tasks, date, priorirty, assigned_to = kishore
//    update the new task id in users collection"""