class InstanceAlreadyExistsError(Exception):
    '''Raised when instance for current user is already in the RunTimeCollection.

    Attributes:
        user_id -- user ID
    '''

    def __init__(self, user_id):
        self.user_id = user_id
