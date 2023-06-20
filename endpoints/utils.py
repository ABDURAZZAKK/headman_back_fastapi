from pydantic import BaseModel


def add_creater_field_to_dict(dt: dict, data: int) -> dict:
    dt["creater"] = data
    return dt


def dict_without_null_from_pydantic_model(d: BaseModel) -> dict:
    data = dict()
    for i in filter(lambda x: bool(x[1]), d):
        data[i[0]] = i[1]

    return data
