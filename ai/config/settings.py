"""
Centralized runtime settings for AI modules.

No new environment variables are introduced here; these are hardcoded
defaults to keep the .env minimal. Adjust values here if needed.
"""

# Huawei ModelArts HTTP behavior
HUAWEI_API_CONNECT_TIMEOUT_SECONDS = 20
HUAWEI_API_READ_TIMEOUT_SECONDS = 90

# Retry backoff sequence for transient timeouts (in seconds)
HUAWEI_REQUEST_BACKOFFS = [2, 4, 8]

# Auth header flavor to use with the competition endpoint
# Options: "Authorization" (Bearer <token>) or "X-Auth-Token": <token>
HUAWEI_AUTH_HEADER = "Authorization"

# Default token budget to reduce latency/timeouts
DEFAULT_MAX_TOKENS = 800

# Prompt size management
MAX_DESCRIPTION_CHARS = 1200
KNOWLEDGE_SUMMARY_MAX_LINES = 40


