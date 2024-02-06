from fastapi import FastAPI


def get_url_from_api_route_name(app: FastAPI, name: str, **params) -> str | None:
    for route in app.routes:
        if route.name == name:
            return route.path.format(**params)
    return None  # for mypy
