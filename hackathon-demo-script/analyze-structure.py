import requests
import json

AUTH = ('admin', 'admin')
BASE = "http://localhost:4502"

print("="*70)
print("ANALYZING WORKING STRUCTURE UNDER /en")
print("="*70)

# Check hero_carousel
print("\n### HERO_CAROUSEL ###")
url = f"{BASE}/content/mohhwebsites/us/en/jcr:content/root/container/container/hero_carousel.json"
response = requests.get(url, auth=AUTH)
if response.status_code == 200:
    data = response.json()
    print("Properties at component level:")
    for key, value in data.items():
        if not key.startswith('jcr:') and not isinstance(value, dict):
            print(f"  {key}: {value}")
else:
    print(f"  ERROR: {response.status_code}")

# Check hero_carousel slide
print("\nSlide properties:")
url = f"{BASE}/content/mohhwebsites/us/en/jcr:content/root/container/container/hero_carousel/slides/item0.json"
response = requests.get(url, auth=AUTH)
if response.status_code == 200:
    data = response.json()
    print("Properties in slides/item0:")
    for key, value in data.items():
        if not key.startswith('jcr:'):
            print(f"  {key}: {value}")
else:
    print(f"  Not found or error: {response.status_code}")

# Check four_card_carousel
print("\n### FOUR_CARD_CAROUSEL ###")
url = f"{BASE}/content/mohhwebsites/us/en/jcr:content/root/container/container/four_card_carousel.json"
response = requests.get(url, auth=AUTH)
if response.status_code == 200:
    data = response.json()
    print("Properties at component level:")
    for key, value in data.items():
        if not key.startswith('jcr:') and not isinstance(value, dict):
            print(f"  {key}: {value}")
else:
    print(f"  Not found")

# Check card properties
print("\nCard properties:")
url = f"{BASE}/content/mohhwebsites/us/en/jcr:content/root/container/container/four_card_carousel/cards/item0.json"
response = requests.get(url, auth=AUTH)
if response.status_code == 200:
    data = response.json()
    print("Properties in cards/item0:")
    for key, value in data.items():
        if not key.startswith('jcr:') and not isinstance(value, dict):
            print(f"  {key}: {value}")
else:
    print(f"  Not found or error: {response.status_code}")

# Check if nested container exists
print("\n### CONTAINER STRUCTURE ###")
url = f"{BASE}/content/mohhwebsites/us/en/jcr:content/root/container/container.json"
response = requests.get(url, auth=AUTH)
if response.status_code == 200:
    data = response.json()
    print(f"Nested container resource type: {data.get('sling:resourceType')}")
    print(f"Layout: {data.get('layout', 'N/A')}")
else:
    print(f"Nested container not found")

print("\n" + "="*70)
print("CURRENT SCRIPT CREATES AT:")
print("  /hackathon-demo-page/jcr:content/root/container/demoHeroCarousel")
print("\nSHOULD CREATE AT:")
print("  /hackathon-demo-page/jcr:content/root/container/container/hero_carousel")
print("="*70)
