from fastapi.responses import JSONResponse

class ItemNotFoundError(Exception):
    pass


class DuplicateItemError(Exception):
    pass


class ItemConflictError(Exception):
    pass

class NoFieldsProvidedError(Exception):
    pass

class DbError(Exception):
    pass
