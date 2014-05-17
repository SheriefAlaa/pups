// This file is part of Pups, a django/python project which contains
// web support tools
//
//  Author: Sherief Alaa <sheriefalaa.w@gmail.com>
//
//  Copyright:
//   (c) 2014 Sherief Alaa.
//   (c) 2014 The Tor Project, Inc.
//
// Pups is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// Pups is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with Pups.  If not, see <http://www.gnu.org/licenses/>.

var current_issue_edit_id;

$(document).ready (function (){

  $("#save_issue").click(function() {

    if ($("#new_issue_text").val() == '') {
      alert ('Please enter something');
      return false;
    }

    NewIssue();
  });

  $("#save_edit").click(function() {

    SaveEdit(current_issue_edit_id);
  });

  $("#close_edit").click(function() {

    CancelEdit(current_issue_edit_id);
  });

});

function NewIssue() {

    var uid = generateUUID();
    var quoted_uid =  "'" + uid + "'"; // Wrapped in quotes to make things cleaner.

    // Send question text to sqlite

    // Create a new question
    $("#issues").append(
      '<div class="clear"></div>'
      +'<div id="issue-' + uid + '" class="row"></div>');
    $("#issue-" + uid).append(
      '<div id="issue_text-' + uid + '" name="issue_text" class="col-md-9">' + $("#new_issue_text").val() + '</div>'
      +'<div class="options">'
      +'<input id="counter-' + uid + '" class="form-control" name="counter" type="text" size="4" value="" readonly>'
      +'<button id="plus-' + uid + '" class="btn btn-default" onclick="counter(' + quoted_uid + ');">+1</button>'
      +'<button id="edit-' + uid + '" class="btn btn-default" data-toggle="modal" data-target="#EditIssue" onclick="edit_issue(' + quoted_uid + ')">Edit</button>'
      +'<input id="del-' + uid + '" class="btn btn-danger" type="button" value="Delete" onclick="DeleteIssue(' + quoted_uid + ');">'
     +'</div>');

    // Clear question to avoid replication by mistake.
    $("#new_issue_text").val("");
}

// Edit a question
function edit_issue(quoted_uid) {

  // Lock issue in db

  // Let the user edit issue
  $("#edit_text").val($("#issue_text-" + quoted_uid).text());
  current_issue_edit_id = quoted_uid;
}

function SaveEdit(quoted_uid) {

  $("#EditIssue").modal('hide');
  // Should send changes to sqlite and unclock db

  // Save locally for UI
}

function CancelEdit(quoted_uid) {

  // unlock issue in db
}

// Delete a question
function DeleteIssue(uid) {
  if (confirmBox()) {

    // Send a delete request to sqlite

    // Remove issue from db and html
    $("#issue-" + uid).remove();
  }
}

// +1 a question
function counter(uid) {

  // Send a +1 to sqlite

  // lock the button to avoid double +1s

  // wait for success callback

  // if callback returns a failure alert DB error

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