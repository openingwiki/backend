from pydantic import BaseModel


def return_converter(func):
    """Decorator for data validation."""

    def wrapper(*args, **kwargs):
        """
        Excluding not matching fields from result pydantic model.
        Last arg in function calling must be pydantic response type.
        """
        if not callable(args[-1]) and not args[-1] is BaseModel:
            return func(*args, **kwargs)

        result: BaseModel = func(*args[:-1], **kwargs)
        FunctionReturnModel: BaseModel = args[-1]
        return FunctionReturnModel(**result.model_dump())

    return wrapper
