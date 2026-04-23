

class ItemNotFoundError(Exception):
    pass


class DuplicateItemError(Exception):
    pass


class ItemConflictError(Exception):
    pass

class DbError(Exception):
    pass