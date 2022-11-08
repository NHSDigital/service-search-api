import os

from .environment import ENV

# Api Details
ENVIRONMENT = ENV["environment"]
BASE_URL = f"https://{ENVIRONMENT}.api.service.nhs.uk"
BASE_PATH = ENV["base_path"]

if "sandbox" in ENVIRONMENT:
    PROXY_API_KEY = "not-needed"
else:
    PROXY_API_KEY = os.environ["PROXY_API_KEY"]
