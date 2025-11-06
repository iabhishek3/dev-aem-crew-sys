#!/usr/bin/env python3
"""
AEM Component Migration Script
Migrates HeroCarousel and TeaserGridCardFour components to AEM

Usage:
    python migrate.py
    python migrate.py --json physician_mohh_aem.json
    python migrate.py --page /content/mohhwebsites/us/my-page --json my-data.json
"""

import json
import requests
import sys
import argparse

# Default Configuration
AEM_HOST = "http://localhost:4502"
AUTH = ('admin', 'admin')
PAGE_PATH = "/content/mohhwebsites/us/hackathon-demo-page"
CONTAINER_PATH = "/jcr:content/root/container/container"  # FIXED: Nested container!
DEFAULT_JSON_FILE = "demo-components.json"

def migrate_hero_carousel(component, page_path, container_path, aem_host=AEM_HOST):
    """Migrate HeroCarousel with CORRECT property names"""

    component_name = component.get('componentName', 'heroCarousel')
    component_path = f"{page_path}{container_path}/{component_name}"

    print(f"\n[HeroCarousel] Migrating to: {component_path}")

    form_data = {}

    # Resource type
    form_data['./sling:resourceType'] = component.get('resourceType', 'mohhwebsites/components/hero-carousel')

    # Main settings - CORRECT property names
    settings = component.get('settings', {})
    form_data['./autoPlay'] = 'on' if settings.get('autoPlay', True) else ''
    form_data['./autoPlayDelay'] = str(settings.get('autoPlayDelay', 5))
    form_data['./backgroundColor'] = settings.get('backgroundColor', '#F5F0E8')
    form_data['./textColor'] = settings.get('textColor', '#2D3748')
    form_data['./buttonColor'] = settings.get('buttonColor', '#7BA7E9')
    form_data['./buttonTextColor'] = settings.get('buttonTextColor', '#FFFFFF')
    form_data['./showArrow'] = 'on' if settings.get('showArrow', True) else ''

    # Slides - CORRECT property names
    slides = component.get('slides', [])
    if slides:
        form_data['./slides@TypeHint'] = 'nt:unstructured'

    for slide_idx, slide in enumerate(slides):
        slide_prefix = f'./slides/item{slide_idx}'
        form_data[f'{slide_prefix}@TypeHint'] = 'nt:unstructured'

        # CORRECT property names (no nested structures!)
        form_data[f'{slide_prefix}/slideHeading'] = slide.get('slideHeading', '')
        form_data[f'{slide_prefix}/slideDescription'] = slide.get('slideDescription', '')
        form_data[f'{slide_prefix}/slideImagePath'] = slide.get('slideImagePath', '')
        form_data[f'{slide_prefix}/slideCtaText'] = slide.get('slideCtaText', '')
        form_data[f'{slide_prefix}/slideCtaLink'] = slide.get('slideCtaLink', '')

    print(f"  Properties: {len(form_data)}")
    print(f"  Slides: {len(slides)}")

    # POST to AEM
    return post_to_aem(component_path, form_data, aem_host)

def migrate_teaser_grid_card_four(component, page_path, container_path, aem_host=AEM_HOST):
    """Migrate TeaserGridCardFour with CORRECT property names"""

    component_name = component.get('componentName', 'teaserGrid')
    component_path = f"{page_path}{container_path}/{component_name}"

    print(f"\n[TeaserGridCardFour] Migrating to: {component_path}")

    form_data = {}

    # Resource type
    form_data['./sling:resourceType'] = component.get('resourceType', 'mohhwebsites/components/teasergridcardfour')

    # Header - CORRECT property names
    header = component.get('header', {})
    form_data['./headerTitle'] = header.get('title', '')
    form_data['./headerSubtitle'] = header.get('subtitle', '')
    if header.get('description'):
        form_data['./headerDescription'] = header.get('description')
    form_data['./headerTitleColor'] = header.get('titleColor', '#6b6b6b')
    form_data['./headerSubtitleColor'] = header.get('subtitleColor', '#7ba7d6')

    # Settings - CORRECT property names
    settings = component.get('settings', {})
    form_data['./autoRotateEnabled'] = 'on' if settings.get('autoRotateEnabled', False) else ''
    form_data['./autoRotateInterval'] = str(settings.get('autoRotateInterval', 5))

    # Cards - CORRECT property names
    cards = component.get('cards', [])
    if cards:
        form_data['./cards@TypeHint'] = 'nt:unstructured'

    for card_idx, card in enumerate(cards):
        card_prefix = f'./cards/item{card_idx}'
        form_data[f'{card_prefix}@TypeHint'] = 'nt:unstructured'

        # Card properties - CORRECT names
        form_data[f'{card_prefix}/image'] = card.get('image', '')
        form_data[f'{card_prefix}/imageAlt'] = card.get('imageAlt', '')
        form_data[f'{card_prefix}/title'] = card.get('title', '')
        if card.get('description'):
            form_data[f'{card_prefix}/description'] = card.get('description')

        # Links - CORRECT property names
        links = card.get('links', [])
        if links:
            form_data[f'{card_prefix}/links@TypeHint'] = 'nt:unstructured'

        for link_idx, link in enumerate(links):
            link_prefix = f'{card_prefix}/links/item{link_idx}'
            form_data[f'{link_prefix}@TypeHint'] = 'nt:unstructured'
            form_data[f'{link_prefix}/text'] = link.get('text', '')
            form_data[f'{link_prefix}/url'] = link.get('url', '')
            form_data[f'{link_prefix}/target'] = link.get('target', '_self')

    total_links = sum(len(card.get('links', [])) for card in cards)
    print(f"  Properties: {len(form_data)}")
    print(f"  Cards: {len(cards)}")
    print(f"  Total Links: {total_links}")

    # POST to AEM
    return post_to_aem(component_path, form_data, aem_host)

def post_to_aem(component_path, form_data, aem_host=AEM_HOST):
    """POST form data to AEM"""
    url = f"{aem_host}{component_path}"

    try:
        print(f"  Posting to: {url}")
        response = requests.post(url, data=form_data, auth=AUTH, timeout=30)

        if response.status_code in [200, 201]:
            print(f"  [OK] Success!")
            return True
        else:
            print(f"  [ERROR] Failed: HTTP {response.status_code}")
            print(f"  Response: {response.text[:300]}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"  [ERROR] Request failed: {str(e)}")
        return False

def verify_page_exists(page_path, aem_host=AEM_HOST):
    """Verify target page exists"""
    url = f"{aem_host}{page_path}.json"

    try:
        response = requests.get(url, auth=AUTH, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if data.get('jcr:primaryType') == 'cq:Page':
                print(f"[OK] Target page exists: {page_path}")
                return True

        print(f"[ERROR] Page not found: {page_path}")
        return False

    except Exception as e:
        print(f"[ERROR] Error checking page: {str(e)}")
        return False

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Migrate AEM components from JSON data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python migrate.py
  python migrate.py --json physician_mohh_aem.json
  python migrate.py --page /content/mohhwebsites/us/my-page
  python migrate.py --page /content/mohhwebsites/us/my-page --json my-data.json --host http://localhost:4502
        """
    )

    parser.add_argument('--json',
                       default=DEFAULT_JSON_FILE,
                       help=f'JSON file with component data (default: {DEFAULT_JSON_FILE})')

    parser.add_argument('--page',
                       default=PAGE_PATH,
                       help=f'Target page path (default: {PAGE_PATH})')

    parser.add_argument('--host',
                       default=AEM_HOST,
                       help=f'AEM host URL (default: {AEM_HOST})')

    parser.add_argument('--container',
                       default=CONTAINER_PATH,
                       help=f'Container path (default: {CONTAINER_PATH})')

    args = parser.parse_args()

    # Use arguments
    json_file = args.json
    page_path = args.page
    aem_host = args.host
    container_path = args.container

    print("=" * 70)
    print("AEM Component Migration")
    print("=" * 70)
    print(f"AEM Host: {aem_host}")
    print(f"Target Page: {page_path}")
    print(f"Container: {container_path}")
    print(f"JSON File: {json_file}")
    print("=" * 70)

    # Read JSON data
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"\n[ERROR] JSON file not found: {json_file}")
        print(f"Please ensure the file exists in the current directory.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"\n[ERROR] Invalid JSON: {e}")
        sys.exit(1)

    components = data.get('components', [])
    print(f"\nComponents to migrate: {len(components)}")

    # Verify page exists
    if not verify_page_exists(page_path, aem_host):
        print("\n[ERROR] Target page does not exist. Create it first.")
        sys.exit(1)

    # Migrate components
    results = {'success': 0, 'failed': 0}

    for component in components:
        component_type = component.get('componentType', '').lower()

        if component_type == 'herocarousel':
            success = migrate_hero_carousel(component, page_path, container_path, aem_host)
        elif component_type == 'teasergridcardfour':
            success = migrate_teaser_grid_card_four(component, page_path, container_path, aem_host)
        else:
            print(f"\n[ERROR] Unknown component type: {component_type}")
            success = False

        if success:
            results['success'] += 1
        else:
            results['failed'] += 1

    # Summary
    print("\n" + "=" * 70)
    print("MIGRATION SUMMARY")
    print("=" * 70)
    print(f"[OK] Success: {results['success']}")
    print(f"[ERROR] Failed: {results['failed']}")

    if results['failed'] == 0:
        print("\n[OK] All components migrated successfully!")
        print(f"\nView page: {aem_host}/editor.html{page_path}.html")
    else:
        print("\n[ERROR] Some components failed to migrate.")

    print("=" * 70)

    sys.exit(0 if results['failed'] == 0 else 1)

if __name__ == '__main__':
    main()
