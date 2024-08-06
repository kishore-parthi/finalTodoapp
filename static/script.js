
$(document).ready(function () {
    var selectedPriority; 
    $('#addTaskBtn').click(function () {
        $('#displayArea').toggle();
        selectedPriority = $('#prioritySelector').val();
       
       
    });
    $('.close-btn').click(function () {
        $('#displayArea').hide();
    });

    $(document).ready(function() {
        $('#priorityLevel').change(function() {
            var selectedPriority = $(this).val();
            $(this).removeClass().addClass(selectedPriority + '-priority');
        });
    });
    
    $('#prioritySelector').change(function () {
        var selectedColor = $(this).find('option:selected').css('color');
        $(this).css('color', selectedColor);
    }); 

   
    
// script.js.............11111111111111111...........
$(document).ready(function () {
    // When Edit button is clicked
    $('.edit-btn').click(function () {
        var taskId = $(this).data('task-id');
        var taskText = $(this).data('task-text');
        var taskPriority = $(this).data('task-priority');
        var assignedTo = $(this).closest('.task-recordarea').find('.userselect').find('span').text().trim();
        
        // Set the text and priority level in the edit container
        $('#edit-container-' + taskId + ' .edit-textarea').val(taskText);
        $('#edit-container-' + taskId + ' .edit-priorityLevel').val(taskPriority);
        $('#edit-container-' + taskId + ' .edit-user-selector').val(assignedTo); 
       
        
        // Hide all edit containers
        $('.edit-container').hide();
        // Show edit container for the clicked task
        $('#edit-container-' + taskId).show();
        $(this).addClass('edit-fading');
        
    });

    // When Submit button inside edit container is clicked
    $('.submit-edit-btn').click(function () {
        // Hide the edit container
        $(this).closest('.edit-container').hide();
    });
});
// script.js


    

//  // Delete button click event
// $(document).ready(function () {
    // Show delete confirmation popup when delete button is clicked
    $('.delete-btn').click(function () {
        var taskId = $(this).data('task-id');
        $(this).addClass('delete-fading');

    // Disable the cursor
    $(this).css('cursor', 'not-allowed');
        // $('.delete-confirm-popup[data-task-id="' + taskId + '"]').show();
        $(this).closest('.task-recordarea').find('.delete_cont').show();
    });
    $('.close').click(function () {
        $(this).closest('.task-recordarea').find('.delete_cont').hide();
        $('.delete-btn').removeClass('delete-fading');
    });
    // Hide delete confirmation popup when cancel button is clicked
    $('.cancel').click(function () {
        $(this).closest('.task-recordarea').find('.delete_cont').hide();
        $('.delete-btn').removeClass('delete-fading');

        // Enable the cursor
        $('.delete-btn').css('cursor', 'pointer');
    });
    

$('.done-btn').click(function () {
    var taskId = $(this).data('task-id');
   
    $(this).addClass('done-fading');

    // Disable the cursor
    $(this).css('cursor', 'not-allowed');
    $(this).closest('.task-recordarea').find('.done_cont').show();
    
});
$('.close').click(function () {

    $(this).closest('.task-recordarea').find('.done_cont').hide();
    var taskId = $(this).data('task-id');
   
    
    $('.done-btn').removeClass('done-fading');

    // Enable the cursor
    $('.done-btn').css('cursor', 'pointer');
    
});
$('.cancel').click(function () {
    $(this).closest('.task-recordarea').find('.done_cont').hide();
    $('.done-btn').removeClass('done-fading');

    // Enable the cursor
    $('.done-btn').css('cursor', 'pointer');
});

});






//-----------------------//
