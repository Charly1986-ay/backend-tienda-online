from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.main import app

for i, included in enumerate(app.routes):
    if type(included).__name__ != "_IncludedRouter":
        continue

    router = included.original_router

    for route in router.routes:
        path = getattr(route, "path", None)
        name = getattr(route, "name", None)

        print(f"\nProbando router {i}: {path} ({name})")

        test_app = FastAPI()
        test_app.router.routes.append(route)

        try:
            get_openapi(
                title="Diagnostico",
                version="1.0.0",
                routes=test_app.routes,
            )
            print("OK")
        except Exception as exc:
            print("ERROR:", type(exc).__name__, str(exc))