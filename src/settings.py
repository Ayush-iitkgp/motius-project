from os import getenv

TITLE = "Motius Project for Chat App"
DESCRIPTION = "This projects"

PORT = int(getenv("APP_PORT", "9090"))
HOST = getenv("APP_HOST", "0.0.0.0")
