$(document).ready(function () {
    $('.reopen-btn').click(function () {
        var taskId = $(this).data('task-id');
        $.ajax({
            type: 'POST',
            url: '/completedtasks',
            data: {
                reopen_task_id: taskId
            },
            success: function (response) {
                // Remove the task record from the DOM
                // $('.reopen-btn[data-task-id="' + taskId + '"]').closest('.task-recordarea').remove();
                // Optional: display a success message or perform any other action
                // alert('Task reopened successfully!');
                window.location.href = '/'; 
            },
            error: function (xhr, status, error) {
                console.error('Error reopening task:', error);
            }
        });
    });
});