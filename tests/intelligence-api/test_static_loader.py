import urllib.request
import json

def test_static_json_delivery():
    # Note: Ensure `npm run dev` is running on port 3000 before running this test
    url = "http://localhost:3000/data/intelligence/intelligence_summary.json"
    try:
        response = urllib.request.urlopen(url)
        assert response.status == 200
        
        data = json.loads(response.read().decode('utf-8'))
        assert data["project_id"] == "POC-41"
    except urllib.error.URLError:
        assert False, "Frontend server is not running or file is not in public directory"