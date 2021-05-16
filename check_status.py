def check_status(user_id, white_lst):
    """
    return True if user_id is inside white list, else False
    """
    if str(user_id) in white_lst:
        return True
    return False