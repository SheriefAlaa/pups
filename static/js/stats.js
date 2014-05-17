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

var Stats = {};
var current_issue_edit_id;
var gridUpdateInterval;
const MAX_ROW_LENGTH = 86;
const GRID_UPDATE_TIMER = 10000;

// Remembers if "more" was clicked to stop updateGrid() reverting
// the issue text to the shorty version
var expandedIssues = [];

$(document).ready (function (){

  gridUpdateInterval = setInterval("Stats.Util.updateGrid()", GRID_UPDATE_TIMER);
  
  Stats.Util.updateGrid(); // Update the grid when the page is loaded (off by one).

  $(document).on('click', '[name=edit_issue]', function() {
    Stats.Util.updateGrid();
    Stats.ActionHandler.editIssue(
      Stats.Util.getID($(this).attr("id"), '-', 1)
    );
  });

  $(document).on('click', '[name=delete_issue]', function() {
    Stats.ActionHandler.deleteIssue(
      Stats.Util.getID($(this).attr("id"), '-', 1)
      );
  });

  $(document).on('click', '[name=plus_one_button]', function() {
    Stats.ActionHandler.plusOne(
      Stats.Util.getID($(this).attr("id"), '-', 1)
      );
  });

  $("#save_issue").click(function() {

    if ($("#new_issue_text").val() == '') {
      alert ('Please enter something');
      return false;
    }
  });
  
  $(document).on('click', '#save_edit', function() {

    Stats.ActionHandler.saveEdit(current_issue_edit_id);
    Stats.ActionHandler.unlockIssue(current_issue_edit_id);
    Stats.Util.updateGrid();
  });

  $(document).on('click', '#close_edit',function() {
    Stats.ActionHandler.unlockIssue(current_issue_edit_id);
  });

  $(document).on('click', '.readMore', function() {
    Stats.UI.fullComment($(this).attr("id"));
  });

  $(document).on('click', '.readLess', function() {
    Stats.UI.shortComment($(this).attr("id"));
  });

  $('#alert-ok').on('click', function() {
    gridUpdateInterval = setInterval("Stats.Util.updateGrid()", GRID_UPDATE_TIMER);
  });

});

Stats.ActionHandler = {

  editIssue: function(id) {
    $.ajax({
      type: "POST",
      url: "/edit_issue",
      data: {"id": id},
      success: function(issue) {
        if (issue['lock_status'] == 'lock_success' || issue['locked_by'] === $.trim($("#user").text()) ){
          // Let the user edit the issue
          $('#EditIssue').modal('show');
          $("#edit_text").val($("#full_issue_text-" + id).val());
          current_issue_edit_id = id;

        }else if (issue['lock_status'] == 'does_not_exist') {

          $('#Alert').modal('show');
          $(".alert-body").html("This issue doesn't exist anymore, please refresh");

        }else if (issue['locked_by'] !== undefined) {
          if (issue['locked_by'] == $("#user").val()) {
            $('#EditIssue').modal('show');
            $("#edit_text").val($("#full_issue_text-" + id).val());
            current_issue_edit_id = id;
          }else{
            $('#Alert').modal('show');
            $(".alert-body").html("This issue is currently being edited by " + issue['locked_by']);
          }
        }
      },
      error: function(){
        clearInterval(gridUpdateInterval);
        Stats.UI.reportServerUnreachable();
      },
      headers: {
        'X-CSRFToken': Stats.Util.getCookie('csrftoken')
      }
    });

  },

  saveEdit: function(id) {
    $.ajax({
      type: "POST",
      url: "/save_issue_edit",
      data: {"id": id, "edited_text": $("#edit_text").val()},
      success: function() {
        $("#EditIssue").modal('hide');
      },
      error: function(){
        clearInterval(gridUpdateInterval);
        Stats.UI.reportServerUnreachable();
      },
      headers: {
        'X-CSRFToken': Stats.Util.getCookie('csrftoken')
      }
    });
  },

  deleteIssue: function(id) {

    if (confirm_box()) {
      // Send a delete request to sqlite
      $.ajax({
        type: "POST",
        url: "/delete_issue",
        data: {"id": id},
        success: function() {
          $("#issue-" + id).remove();
        },
        error: function(){
          clearInterval(gridUpdateInterval);
          Stats.UI.reportServerUnreachable();
        },
        headers: {
          'X-CSRFToken': Stats.Util.getCookie('csrftoken')
        }
      });
    }
  },

  plusOne: function(id) {
    // Send a +1 to db
    $.ajax({
      type: "POST",
      url: "/plus_one",
      data: {"id": id},
      success: function() {
        // Updating fields manually
        if ($("#plus_one-" + id).val() == "")
          $("#plus_one-" + id).val("1");
        else
          $("#plus_one-" + id).val(parseInt($("#plus_one-" + id).val()) + 1);
      },
      error: function(){
        clearInterval(gridUpdateInterval);
        Stats.UI.reportServerUnreachable();
      },
      headers: {
        'X-CSRFToken': Stats.Util.getCookie('csrftoken')
      }
    });
  },

  // unlocks a row in db
  unlockIssue: function(id) {
    $.ajax({
      type: "POST",
      url: "/unlock_issue",
      data: {"id": id},
      error: function(){
        clearInterval(gridUpdateInterval);
        Stats.UI.reportServerUnreachable();
      },
      headers: {'X-CSRFToken': Stats.Util.getCookie('csrftoken')}
    });
  },

}

Stats.Util = {
  
  getID: function(str, delimiter, pos) {
    return str.split(delimiter)[pos]
  },

  // Required for django's csrf protection
  getCookie: function(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie != '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = jQuery.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) == (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  },

  updateGrid: function() {
    $.ajax({
      type: "POST",
      dataType: "json",
      url: "/stats_data_ajax",
      success: function(issues) {

        issues_json = JSON.parse(issues);
        $.each(issues_json, function(key, value) {

          // If someone created a new issue, add it to the DOM dynamically
          if ($("#issue-" + value['pk']).length == false) {

            $("#issues").append(
              '<div class="clear"></div>'
              +'<div id="issue-'+ value['pk'] +'" class="row">');

            $("#issue-" + value['pk']).append(
                '<div id="short_issue_text-'+ value['pk']+'" name="issue_text" class="col-md-9">'
                 +'<span id="short_sub_text-'+ value['pk']+'"></span>'
              +' </div>'
              +'<input id="full_issue_text-'+ value['pk']+'" type="hidden" value="'+ value['fields'].text+'">'
              +'<input id="user" type="hidden" value="">'
               +'<div class="options">'
                +'<input id="plus_one-'+ value['pk']+'" name="plus_one" class="form-control" type="text" size="4" value="'+value['fields'].frequency+'" readonly>'
                +' <button id="plus-'+ value['pk']+'" name="plus_one_button" class="btn btn-default">+1</button>'
                +' <button id="edit-'+ value['pk']+'" name="edit_issue" class="btn btn-default" data-toggle="modal">Edit</button>'
                +' <button id="del-'+ value['pk']+'" name="delete_issue" class="btn btn-danger">Delete</button>'
               +'</div>'
              );

            var shortText = value['fields'].text;
          
            if (value['fields'].text.length > MAX_ROW_LENGTH) {
              var shortText = value['fields'].text.substring(0, MAX_ROW_LENGTH); 
              $("#short_issue_text-" + value['pk']).append('<a id="more-'+ value['pk']+'" class="readMore" href="#"> more</a>');
            }

            // Adding the issue's short text after creating the element to use .text() to escape text
            $("#short_sub_text-" + value['pk']).text(shortText);


          }else{

            // Updating existing issues if any changes occured

            // Issue text update
            if ( $("#full_issue_text-" + value['pk']).val() !== value['fields'].text ) {
              $("#full_issue_text-" + value['pk']).val(value['fields'].text);

              // if an issue was expanded ("more" was currently clicked by the user)
              var expandedIssue = expandedIssues.indexOf(value['pk']);

              if ( expandedIssues[expandedIssue] == value['pk'] ) {
                $("#short_sub_text-" + value['pk']).text(value['fields'].text);
                
                if ( value['fields'].text.length > MAX_ROW_LENGTH )
                 $("#short_issue_text-" + value['pk']).append('<a id="less-'+ value['pk'] +'" class="readLess" href="#"> less</a>');

              }else{

                $("#short_sub_text-" + value['pk']).text(value['fields'].text.substring(0, MAX_ROW_LENGTH));
                
                if ( value['fields'].text.length > MAX_ROW_LENGTH && $("#more-" + value['pk']).length == 0){
                  $("#short_issue_text-" + value['pk']).append('<a id="more-'+ value['pk']+'" class="readMore" href="#"> more</a>');
                } else if (value['fields'].text.length < MAX_ROW_LENGTH) {
                  $("#more-" + value['pk']).remove();
                }
              }
            }

            // Issue frequency update
            $("#plus_one-" + value['pk']).val(value['fields'].frequency);
          }
        });
      },
      error: function(){
        clearInterval(gridUpdateInterval);
        Stats.UI.reportServerUnreachable();
      },
      headers: {
        'X-CSRFToken': Stats.Util.getCookie('csrftoken')
      },
    });
  
  },
}

Stats.UI = {
  fullComment: function(parentid){
    id = parentid.split('-')[1];
    
    // Remember that "more" was clicked
    if ( expandedIssues.indexOf(id) == -1)
      expandedIssues.push(id);

    // Show full comment
    $("#short_sub_text-" + id).text($("#full_issue_text-" + id).val());
    $("#more-" + id).remove();

    // Add a less link
    $("#short_sub_text-" + id).append('<a id="less-'+ id +'" class="readLess" href="#"> less</a>');

  },

  shortComment: function(parentid){
    id = parentid.split('-')[1]; 
    $("#less-" + id).remove();

    // Forget "more" state
    expandedIssues.splice(expandedIssues.indexOf(id), 1);
    $("#short_sub_text-" + id).text($("#full_issue_text-" + id).val().substring(0, MAX_ROW_LENGTH));

    // Add "more" link
    $("#short_sub_text-" + id).append('<a id="more-'+ id +'" class="readMore" href="#"> more</a>');
  },

  reportServerUnreachable: function(){
    $("#Alert").modal({
      keyboard: false,
      backdrop: false,
      show: true
    });
    $(".alert-body").html("Stats can't reach the server, would you like to retry?");
  }
}

// Standard JS dialog box
function confirm_box() {
  if (confirm("Are you sure you want to delete this?"))
    return true;
  return false;
}