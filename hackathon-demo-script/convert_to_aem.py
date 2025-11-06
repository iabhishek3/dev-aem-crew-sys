#!/usr/bin/env python3
"""
Convert Physician MOHH Website Data to AEM Component Format

This script converts the extracted website data from www_physician_mohh_com_sg.json
to the AEM component structure format (physician_mohh_aem.json) that can be
migrated using migrate.py.

Usage:
    python convert_to_aem.py
"""

import json
import sys
from datetime import datetime

# Configuration
SOURCE_FILE = 'www_physician_mohh_com_sg.json'
OUTPUT_FILE = 'physician_mohh_aem.json'
TARGET_PAGE = '/content/mohhwebsites/us/hackathon-demo-page'

# Image paths to use (existing in AEM)
AVAILABLE_IMAGES = [
    '/content/dam/mohhwebsites/mohh-hero-carousel-desktop.jpg',
    '/content/dam/mohhwebsites/mohh-hero-career.jpg'
]

# Default link URL
DEFAULT_LINK_URL = '/content/mohhwebsites'

def convert_herobanner_to_herocarousel(herobanner_data):
    """
    Convert herobanner component to HeroCarousel format

    Key Mapping:
    - herobanner.properties.slides[].heading -> herocarousel.slides[].slideHeading
    - herobanner.properties.slides[].description -> herocarousel.slides[].slideDescription
    - herobanner.properties.slides[].image.damPath -> herocarousel.slides[].slideImagePath (using available images)
    - herobanner.properties.slides[].ctaText -> herocarousel.slides[].slideCtaText
    - herobanner.properties.slides[].ctaUrl -> herocarousel.slides[].slideCtaLink (using default)
    """

    slides = []
    source_slides = herobanner_data.get('properties', {}).get('slides', [])

    # Convert source slides (use up to 2 slides or create second one)
    for idx, source_slide in enumerate(source_slides[:2]):
        slide = {
            "slideHeading": source_slide.get('heading', ''),
            "slideDescription": source_slide.get('description', ''),
            "slideImagePath": AVAILABLE_IMAGES[idx % len(AVAILABLE_IMAGES)],
            "slideCtaText": source_slide.get('ctaText') or 'Learn More',
            "slideCtaLink": source_slide.get('ctaUrl') or DEFAULT_LINK_URL
        }
        slides.append(slide)

    # If only one slide in source, create a second one for carousel
    if len(slides) == 1:
        slides.append({
            "slideHeading": "Join Our Medical Team",
            "slideDescription": "Be part of Singapore's leading public healthcare institutions and make a difference in patients' lives.",
            "slideImagePath": AVAILABLE_IMAGES[1],
            "slideCtaText": "Explore Opportunities",
            "slideCtaLink": DEFAULT_LINK_URL
        })

    return {
        "componentType": "herocarousel",
        "componentName": "hero_carousel",
        "resourceType": "mohhwebsites/components/hero-carousel",
        "settings": {
            "autoPlay": True,
            "autoPlayDelay": 7,
            "backgroundColor": "#F5F0E8",
            "textColor": "#2D3748",
            "buttonColor": "#7BA7E9",
            "buttonTextColor": "#FFFFFF",
            "showArrow": True
        },
        "slides": slides
    }

def convert_teaser_to_teasergrid(teaser_data):
    """
    Convert teaser component to TeaserGridCardFour format

    Key Mapping:
    - teaser.properties.cards[].title -> teasergridcardfour.cards[].title
    - teaser.properties.cards[].description -> teasergridcardfour.cards[].description
    - teaser.properties.cards[].icon.damPath -> teasergridcardfour.cards[].image (using available images)
    - teaser.properties.cards[].links[].text -> teasergridcardfour.cards[].links[].text
    - teaser.properties.cards[].links[].url -> teasergridcardfour.cards[].links[].url (using default)
    """

    cards = []
    source_cards = teaser_data.get('properties', {}).get('cards', [])

    # Process up to 4 cards
    for idx, source_card in enumerate(source_cards[:4]):
        # Alternate between the two available images
        image_path = AVAILABLE_IMAGES[idx % len(AVAILABLE_IMAGES)]

        # Map title and description directly
        title = source_card.get('title', '')
        description = source_card.get('description', '')

        # Convert links - keep link text from source, use default URL
        links = []
        source_links = source_card.get('links', [])
        for source_link in source_links:
            links.append({
                "text": source_link.get('text', ''),
                "url": DEFAULT_LINK_URL,  # Use default as per requirement
                "target": "_self"
            })

        # Build imageAlt from title and description
        image_alt = f"{title} - {description}".strip()

        card = {
            "image": image_path,
            "imageAlt": image_alt,
            "title": title,
            "description": description,
            "links": links
        }

        cards.append(card)

    return {
        "componentType": "teasergridcardfour",
        "componentName": "four_card_carousel",
        "resourceType": "mohhwebsites/components/teasergridcardfour",
        "header": {
            "title": "Our",
            "subtitle": "Programs",
            "description": "Discover career opportunities and development programs in Singapore's public healthcare sector",
            "titleColor": "#2c3e50",
            "subtitleColor": "#3498db"
        },
        "settings": {
            "autoRotateEnabled": True,
            "autoRotateInterval": 6
        },
        "cards": cards
    }

def main():
    print("=" * 70)
    print("AEM Component Conversion")
    print("=" * 70)
    print(f"Source: {SOURCE_FILE}")
    print(f"Output: {OUTPUT_FILE}")
    print("=" * 70)

    # Read source JSON
    try:
        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            source_data = json.load(f)
    except FileNotFoundError:
        print(f"\n[ERROR] Source file not found: {SOURCE_FILE}")
        print("Please ensure the file exists in the current directory.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"\n[ERROR] Invalid JSON in source file: {e}")
        sys.exit(1)

    print("\n[OK] Source file loaded successfully")

    # Extract components
    components = source_data.get('page', {}).get('content', {}).get('components', [])

    if not components:
        print("[ERROR] No components found in source data")
        sys.exit(1)

    print(f"[OK] Found {len(components)} components in source")

    # Find herobanner and teaser components
    herobanner = None
    teaser = None

    for component in components:
        comp_type = component.get('componentType', '').lower()
        if comp_type == 'herobanner':
            herobanner = component
            print(f"  - Found herobanner component")
        elif comp_type == 'teaser':
            teaser = component
            print(f"  - Found teaser component")

    if not herobanner or not teaser:
        print("\n[ERROR] Required components not found!")
        print(f"  herobanner: {'Found' if herobanner else 'Missing'}")
        print(f"  teaser: {'Found' if teaser else 'Missing'}")
        sys.exit(1)

    # Convert components
    print("\n[Converting] herobanner -> HeroCarousel")
    hero_carousel = convert_herobanner_to_herocarousel(herobanner)
    print(f"  - Created {len(hero_carousel['slides'])} slides")

    print("[Converting] teaser -> TeaserGridCardFour")
    teaser_grid = convert_teaser_to_teasergrid(teaser)
    print(f"  - Created {len(teaser_grid['cards'])} cards")

    # Build output structure
    output_data = {
        "metadata": {
            "description": "Physician MOHH website - AEM Component data for HeroCarousel and TeaserGridCardFour",
            "targetPage": TARGET_PAGE,
            "sourceFile": SOURCE_FILE,
            "createdDate": datetime.now().strftime("%Y-%m-%d"),
            "version": "1.0"
        },
        "components": [
            hero_carousel,
            teaser_grid
        ]
    }

    # Write output
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        print(f"\n[OK] Successfully created: {OUTPUT_FILE}")
        print(f"     Components: {len(output_data['components'])}")
        print(f"     Total slides: {len(hero_carousel['slides'])}")
        print(f"     Total cards: {len(teaser_grid['cards'])}")

    except Exception as e:
        print(f"\n[ERROR] Failed to write output file: {e}")
        sys.exit(1)

    print("\n" + "=" * 70)
    print("CONVERSION COMPLETE")
    print("=" * 70)
    print(f"\nNext steps:")
    print(f"1. Review the output file: {OUTPUT_FILE}")
    print(f"2. Run migration: python migrate.py")
    print("=" * 70)

    return 0

if __name__ == '__main__':
    sys.exit(main())
