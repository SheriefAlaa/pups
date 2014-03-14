# All feedback messages for webchatapp exist here.

class FeedbackMessages():
    # login() view messages
    bad_login = 'Invalid username or password, please retry.'

    # change_password() view messages
    good_pw = 'Successfully changed your password, please logout and use your new password.'
    bad_pw = 'Passwords do not match or you entered the current password incorrectly.'

    # logout() view messages
    was_logged = "Successfully logged out."
    not_logged = "You are not logged to begin with."

    # create_token() view messages
    ticket_exists = "Error: Someone already took this ticket."
    ticket_created = "Successfully created your ticket."
    bad_ticket_format = "Error: RT tickets needs to be numbers only."

    # token_page view messages
    empty_list = "There is nothing to edit/delete, please select something."
    delete_passed = "Successfully deleted what you selected."
    delete_failed = "Error: Could not delete."
    edit_pass = "Successfully saved your change(s)."
    edit_failed = "The following ticket(s) is/are already taken:"
    db_error = "Error: Something is wrong with the database."