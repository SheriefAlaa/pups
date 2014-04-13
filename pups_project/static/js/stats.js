$(document).ready (function (){

  // New question event listener
  $("#savenewq").click(function() {


    if ($("#newqtext").val() == '') {
      alert ('Please enter something');
      return false;
    }

    var uid = generateUUID();
    var quid =  "'" + uid + "'"; // Wrapped in quotes to make things cleaner.

    // Send question text to sqlite

    // Create a new question
    $("#questions").append('<div id="id-' + uid + '"></div>');

    $("#id-"+uid).append('<input id="qtext-' + uid + '" class="form-control" name="qtext" type="text" value="'+ $("#newqtext").val() +'" readonly>');
    $("#id-"+uid).append('<input id="qtextedit-'+ uid +'" class="form-control" style="display:none;" type="text" size="85" value="">');
    $("#id-"+uid).append('<input id="save-'+ uid +'" style="display:none;" class="btn btn-danger" type="button" value="Save" onClick="saveEdit('+quid+');">');
    $("#id-"+uid).append('<input id="cancel-'+ uid +'" style="display:none;" class="btn btn-default" type="button" value="Cancel"onClick="cancelEdit('+quid+');">');
    $("#id-"+uid).append('<input id="counter-' + uid + '" class="form-control" name="counter" type="text" size="4" value="" readonly>');
    $("#id-"+uid).append('<input id="plus-' + uid + '" class="btn btn-default" type="button" value="+1" onClick="counter('+quid+');">');
    $("#id-"+uid).append('<input id="edit-' + uid + '" class="btn btn-default" type="button" value="Edit" style="display:inline-block" onClick="editq('+quid+');" >');
    $("#id-"+uid).append('<input id="del-' + uid + '" class="btn btn-danger" type="button" value="Delete" onClick="deleteq('+quid+');">');


    // Clear question to avoid replication by mistake.
    $("#newqtext").val("");
  });

});

// Edit a question
function editq(uid) {
  $('#qtext-' + uid).hide();
  $('#qtextedit-' + uid).val($('#qtext-' + uid).val());
  $('#qtextedit-'+ uid).css('display','inline-block');
  $('#counter-'+ uid).css('display','inline-block');
  $('#save-'+ uid).css('display','inline-block');
  $('#cancel-'+ uid).css('display','inline-block');
}

function saveEdit(uid) {

  // Should send changes to sqlite

  // Save locally for UI
  $('#qtext-' + uid).val( $('#qtextedit-' + uid).val() );
  $('#qtextedit-'+ uid).css('display','none');
  $('#save-'+ uid).css('display','none');
  $('#cancel-'+ uid).css('display','none');
  $('#qtext-' + uid).show();      
}

function cancelEdit(uid) {
  $('#qtextedit-'+ uid).css('display','none');
  $('#save-'+ uid).css('display','none');
  $('#cancel-'+ uid).css('display','none');
  $('#qtext-' + uid).show();

}

// Delete a question
function deleteq(uid) {
  if (confirmBox()) {

    // Send a delete request to sqlite

    // Remove the div from the page
    $("#del-" + uid).parent().remove();
  }
}

// +1 a question
function counter(uid) {

  // Send a +1 to sqlite

  // Increase the counter by 1
  if ($("#counter-" + uid).val() == "")
    $("#counter-" + uid).val("1");
  else
    $("#counter-" + uid).val(parseInt($("#counter-" + uid).val()) + 1);
}

// Standard JS dialog box
function confirmBox() {
  if (confirm("Are you sure you want to delete this?"))
    return true;
  else 
    return false;
}

// Generates a UUID for each div
function generateUUID() {
    var d = new Date().getTime();
    var uuid = 'xxxxxxxxxxxx4xxxyxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x7|0x8)).toString(16);
    });
    return uuid;
}