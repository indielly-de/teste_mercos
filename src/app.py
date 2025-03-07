from fastapi import FastAPI

import api
from infra.database import init_database
from middleware import cors
from services import loader


def create_app():
    app = FastAPI()

    app.add_event_handler("startup", init_database)
    app.add_event_handler("startup", loader.initial_load)

    cors.init_app(app)
    api.init_app(app)

    return app
