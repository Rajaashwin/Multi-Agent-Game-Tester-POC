import requests
import json

BASE = "http://localhost:8000"

def pretty_print(title, obj):
    print('\n' + '='*30)
    print(title)
    print('='*30)
    try:
        print(json.dumps(obj, indent=2))
    except Exception:
        print(obj)

# GET /
try:
    r = requests.get(BASE + "/")
    pretty_print('GET /', r.json())
except Exception as e:
    print('GET / failed:', e)

# GET /health
try:
    r = requests.get(BASE + "/health")
    pretty_print('GET /health', r.json())
except Exception as e:
    print('GET /health failed:', e)

# POST /api/plan
try:
    payload = {"game_url": "https://play.ezygamers.com/", "test_name": "Smoke Test"}
    r = requests.post(BASE + "/api/plan", json=payload, timeout=30)
    pretty_print('POST /api/plan', r.json())
except Exception as e:
    print('POST /api/plan failed:', e)

# POST /api/execute (run orchestration)
try:
    payload = {"game_url": "https://play.ezygamers.com/", "test_name": "Smoke Execute"}
    r = requests.post(BASE + "/api/execute", json=payload, timeout=120)
    pretty_print('POST /api/execute', r.json())
except Exception as e:
    print('POST /api/execute failed:', e)

# GET /api/latest-report
try:
    r = requests.get(BASE + "/api/latest-report", timeout=30)
    pretty_print('GET /api/latest-report', r.json())
except Exception as e:
    print('GET /api/latest-report failed:', e)

# GET /api/artifacts
try:
    r = requests.get(BASE + "/api/artifacts", timeout=10)
    pretty_print('GET /api/artifacts', r.json())
except Exception as e:
    print('GET /api/artifacts failed:', e)

print('\nSmoke tests completed')
