"""Connectivity checks for Huawei ModelArts and OpenAI using env from project root."""
import os
import sys
from pathlib import Path
import json
import requests
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ENV_PATH = PROJECT_ROOT / ".env"
load_dotenv(ENV_PATH)


def mask(value: str, show: int = 4) -> str:
    if not value:
        return "<missing>"
    if len(value) <= show * 2:
        return "*" * len(value)
    return value[:show] + "*" * (len(value) - (show * 2)) + value[-show:]


def check_env():
    print("Environment variables check:")
    hw_token = os.getenv("DEEPSEEK_API_KEY")
    hw_base_url = os.getenv(
        "AI_DEEPSEEK_BASE_URL",
        "https://pangu.ap-southeast1.myhuaweicloud.com/api/v2/chat/completions",
    )
    hw_model_qwen = os.getenv(
        "AI_DEEPSEEK_MODEL",
        os.getenv("AI_MODEL", "deepseek-r1-distil-qwen-32b_raziqt"),
    )
    hw_model_llama = os.getenv("AI_HUAWEI_LLAMA_MODEL", "distill-llama-8b_46e6iu")

    openai_key = os.getenv("OPENAI_API_KEY")
    openai_model = os.getenv("AI_OPENAI_MODEL") or "gpt-4o"

    print(f"  - HUAWEI TOKEN       : {'set' if hw_token else 'missing'} ({mask(hw_token)})")
    print(f"  - HUAWEI BASE URL    : {hw_base_url}")
    print(f"  - HUAWEI QWEN MODEL  : {hw_model_qwen}")
    print(f"  - HUAWEI LLAMA MODEL : {hw_model_llama}")
    print(f"  - OPENAI_API_KEY     : {'set' if openai_key else 'missing'} ({mask(openai_key)})")
    print(f"  - AI_OPENAI_MODEL    : {openai_model}")

    return hw_token, hw_base_url, hw_model_qwen, hw_model_llama, openai_key, openai_model


def test_huawei_modelarts_chat(hw_token: str, base_url: str, model: str, auth_header: str = "X-Auth-Token") -> None:
    print("\nHuawei ModelArts API check:")
    url = base_url

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "ping"}],
        "max_tokens": 16,
        "temperature": 0.0,
    }
    headers = {"Content-Type": "application/json"}
    if auth_header.lower() == "authorization":
        headers["Authorization"] = f"Bearer {hw_token}"
    else:
        headers["X-Auth-Token"] = hw_token

    try:
        resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
        if resp.status_code == 200:
            print("  ✓ Huawei ModelArts: OK")
            data = resp.json()
            txt = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            print(f"    sample: {txt[:60]!r}")
        else:
            print(f"  ✗ Huawei ModelArts: HTTP {resp.status_code}")
            print(f"    body: {resp.text[:300]}")
    except Exception as e:
        print(f"  ✗ Huawei ModelArts: {e}")


def test_openai_models(openai_key: str, model: str) -> None:
    print("\nOpenAI API key sanity check (no billing used):")
    url = "https://api.openai.com/v1/models"
    headers = {
        "Authorization": f"Bearer {openai_key}",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=20)
        if resp.status_code == 200:
            print("  ✓ OpenAI: OK (models endpoint reachable)")
            # Optionally check desired model name presence
            has_model = any((m.get("id") == model) for m in resp.json().get("data", []))
            print(f"    model '{model}': {'available' if has_model else 'not listed'}")
        else:
            print(f"  ✗ OpenAI: HTTP {resp.status_code}")
            print(f"    body: {resp.text[:200]}")
    except Exception as e:
        print(f"  ✗ OpenAI: {e}")


if __name__ == "__main__":
    (
        hw_token,
        hw_base_url,
        hw_model_qwen,
        hw_model_llama,
        openai_key,
        openai_model,
    ) = check_env()

    if hw_token:
        test_huawei_modelarts_chat(hw_token, hw_base_url, hw_model_qwen, auth_header="Authorization")
        test_huawei_modelarts_chat(hw_token, hw_base_url, hw_model_llama, auth_header="Authorization")
    else:
        print("\nHuawei ModelArts: skipped (missing token)")

    if openai_key:
        test_openai_models(openai_key, openai_model)
    else:
        print("\nOpenAI: skipped (missing key)")

    print("\nDone.")


