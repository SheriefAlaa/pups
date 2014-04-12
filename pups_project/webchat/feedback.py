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
    token_created = "Successfully created your ticket."

    # token_page view messages
    empty_list = "There is nothing to delete, please select something."
    revoke_success = "Successfully revoked selected tokens."
    db_error = "Error: Something is wrong with the database."