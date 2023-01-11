TODO_CREATE_VIEW = {
    'operation_description': 'Enables the authenticated user to create a Todo object.',
    'operation_summary': 'create a todo object',
}

TODO_LIST_VIEW = {
    'operation_description': 'Lists all the Todo objects that are created by the authenticated user.',
    'operation_summary': 'list todo objects',
}

TODO_RETRIEVE_RANDOM_VIEW = {
    'operation_description': 'Retrieves a random Todo object that is created by the authenticated user.',
    'operation_summary': 'retrieve a random todo object',
}

TODO_RETRIEVE_VIEW = {
    'operation_description': 'Retrieves a Todo object that is identified by the id provided by the authenticated user. Retrieving a Todo object created by another user is not authorized.',
    'operation_summary': 'retrieve a todo object by id',
}

TODO_UPDATE_VIEW = {
    'operation_description': 'Completely updates a Todo object that is identified by the id provided by the authenticated user. Updating a Todo object created by another user is not authorized.',
    'operation_summary': 'update a todo object by id',
}

TODO_DESTROY_VIEW = {
    'operation_description': 'Deletes a Todo object that is identified by the id provided by the authenticated user. Deleting a Todo object created by another user is not authorized.',
    'operation_summary': 'destroy a todo object by id',
}

TODO_PARTIAL_UPDATE_VIEW = {
    'operation_description': 'Partially updates a Todo object that is identified by the id provided by the authenticated user. Updating a Todo object created by another user is not authorized.',
    'operation_summary': 'partially update a todo object by id',
}
