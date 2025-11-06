# Hackathon Demo - Component Migration

Quick setup for migrating HeroCarousel and TeaserGridCardFour components to your AEM demo page.

## Files

- **`demo-components.json`** - Demo component data (2 HeroCarousel slides, 4 TeaserGridCardFour cards)
- **`physician_mohh_aem.json`** - Physician website component data (converted from actual website)
- **`www_physician_mohh_com_sg.json`** - Source website data extracted from physician.mohh.com.sg
- **`convert_to_aem.py`** - Python script to convert website data to AEM component format
- **`migrate.py`** - Python migration script to push components to AEM
- **`FIELD_MAPPING.md`** - Complete field mapping documentation
- **`README.md`** - This file

## Component Data

### HeroCarousel (2 slides)
- **Slide 1**: "Excellence in Healthcare" - Uses `mohh-hero-carousel-desktop.jpg`
- **Slide 2**: "Join Our Team" - Uses `mohh-hero-career.jpg`

### TeaserGridCardFour (4 cards)
1. **Cardiac Care** - 2 links
2. **Emergency Care** - 3 links
3. **Surgical Services** - 3 links
4. **Patient Care** - 2 links

All images reference: `/content/dam/mohhwebsites/mohh-hero-carousel-desktop.jpg` and `mohh-hero-career.jpg`

## Workflows

This toolkit supports two workflows:

### Workflow 1: Demo Data (Quick Start)
Use pre-made demo data for testing:
1. Use `demo-components.json` (already created)
2. Run `python migrate.py` to push to AEM

### Workflow 2: Real Website Data (Production)
Convert actual website data to AEM format:
1. Start with `www_physician_mohh_com_sg.json` (source website data)
2. Run `python convert_to_aem.py` to generate `physician_mohh_aem.json`
3. Run `python migrate.py` to push to AEM

---

## Prerequisites

### 1. Python Requirements
```bash
pip install requests
```

### 2. AEM Setup
- AEM running at http://localhost:4502
- Page exists at `/content/mohhwebsites/us/hackathon-demo-page`
- Images uploaded to DAM:
  - `/content/dam/mohhwebsites/mohh-hero-carousel-desktop.jpg`
  - `/content/dam/mohhwebsites/mohh-hero-career.jpg`

### 3. Verify Images in DAM
Open AEM Assets: http://localhost:4502/assets.html/content/dam/mohhwebsites

Ensure both images are uploaded.

## Usage

### Option A: Quick Start with Demo Data

```bash
# Navigate to script folder
cd scripts/hackathon-demo-script

# Run migration with demo data
python migrate.py
```

This uses `demo-components.json` by default.

### Option B: Convert Real Website Data

```bash
# Navigate to script folder
cd scripts/hackathon-demo-script

# Step 1: Convert website data to AEM format
python convert_to_aem.py

# Step 2: Migrate converted data to AEM
python migrate.py
```

This converts `www_physician_mohh_com_sg.json` → `physician_mohh_aem.json` → AEM

### Dry Run (Test Without Changes)

```bash
python migrate.py --page /content/mohhwebsites/us/hackathon-demo-page --dry-run
```

### Custom AEM Host

```bash
python migrate.py --page /content/mohhwebsites/us/hackathon-demo-page --host http://localhost:4502
```

### Help

```bash
python migrate.py --help
```

## Step-by-Step Execution

### Workflow 1: Using Demo Data

#### Step 1: Verify JSON Data

```bash
# View the JSON structure
cat demo-components.json | python -m json.tool
```

#### Step 2: Run Migration (continues below...)

---

### Workflow 2: Converting Real Website Data

#### Step 1: Verify Source Data

```bash
# View the source website data
cat www_physician_mohh_com_sg.json | python -m json.tool

# Check for herobanner and teaser components
python -c "import json; data=json.load(open('www_physician_mohh_com_sg.json')); comps=[c['componentType'] for c in data['page']['content']['components']]; print('Components found:', comps)"
```

**Expected Output:**
```
Components found: ['herobanner', 'teaser', 'heading', 'richtext', ...]
```

#### Step 2: Run Conversion Script

```bash
python convert_to_aem.py
```

**Expected Output:**
```
======================================================================
AEM Component Conversion
======================================================================
Source: www_physician_mohh_com_sg.json
Output: physician_mohh_aem.json
======================================================================

[OK] Source file loaded successfully
[OK] Found 10 components in source
  - Found herobanner component
  - Found teaser component

[Converting] herobanner -> HeroCarousel
  - Created 2 slides
[Converting] teaser -> TeaserGridCardFour
  - Created 4 cards

[OK] Successfully created: physician_mohh_aem.json
     Components: 2
     Total slides: 2
     Total cards: 4

======================================================================
CONVERSION COMPLETE
======================================================================

Next steps:
1. Review the output file: physician_mohh_aem.json
2. Run migration: python migrate.py
======================================================================
```

#### Step 3: Verify Converted Data

```bash
# View the converted AEM format
cat physician_mohh_aem.json | python -m json.tool

# Compare field counts
python -c "import json; data=json.load(open('physician_mohh_aem.json')); hero=data['components'][0]; teaser=data['components'][1]; print(f'HeroCarousel: {len(hero[\"slides\"])} slides'); print(f'TeaserGrid: {len(teaser[\"cards\"])} cards'); print(f'Total links: {sum(len(c[\"links\"]) for c in teaser[\"cards\"])}')"
```

**Expected Output:**
```
HeroCarousel: 2 slides
TeaserGrid: 4 cards
Total links: 8
```

#### Step 4: Review Field Mappings

```bash
# View complete field mapping documentation
cat FIELD_MAPPING.md
```

This shows the exact mapping from source fields to AEM component fields.

---

### Step 2 (Common): Test Connection (Dry Run)

```bash
# Using demo data (default)
python migrate.py --dry-run

# OR using converted physician data
python migrate.py --dry-run
```

Note: The script uses `demo-components.json` by default. To use the converted data, you would update the script or rename the file.

**Expected Output:**
```
======================================================================
AEM Component Migration
======================================================================
AEM Host: http://localhost:4502
Target Page: /content/mohhwebsites/us/hackathon-demo-page
Container: /jcr:content/root/container
JSON File: demo-components.json
Mode: DRY RUN
======================================================================

Components to migrate: 2

[DRY RUN] Migrating HeroCarousel: /content/mohhwebsites/us/hackathon-demo-page/jcr:content/root/container/demoHeroCarousel
  Slides: 2
  Properties: 28
  [DRY RUN] Skipping actual POST to AEM

[DRY RUN] Migrating TeaserGridCardFour: /content/mohhwebsites/us/hackathon-demo-page/jcr:content/root/container/demoTeaserGrid
  Cards: 4
  Total Links: 10
  Properties: 42
  [DRY RUN] Skipping actual POST to AEM

======================================================================
MIGRATION SUMMARY
======================================================================
✓ Success: 2
✗ Failed: 0

[DRY RUN] No changes were made to AEM
======================================================================
```

### Step 3 (Common): Run Actual Migration

```bash
# Run migration to AEM
python migrate.py
```

**Expected Output:**
```
✓ Target page exists: /content/mohhwebsites/us/hackathon-demo-page
  Title: Hackathon Demo Page

Migrating HeroCarousel: /content/mohhwebsites/us/hackathon-demo-page/jcr:content/root/container/demoHeroCarousel
  Slides: 2
  Properties: 28
  Posting to: http://localhost:4502/content/mohhwebsites/us/hackathon-demo-page/jcr:content/root/container/demoHeroCarousel
  ✓ Success: Component created/updated

Migrating TeaserGridCardFour: /content/mohhwebsites/us/hackathon-demo-page/jcr:content/root/container/demoTeaserGrid
  Cards: 4
  Total Links: 10
  Properties: 42
  Posting to: http://localhost:4502/content/mohhwebsites/us/hackathon-demo-page/jcr:content/root/container/demoTeaserGrid
  ✓ Success: Component created/updated

======================================================================
MIGRATION SUMMARY
======================================================================
✓ Success: 2
✗ Failed: 0

✓ All components migrated successfully!

View page in AEM: http://localhost:4502/editor.html/content/mohhwebsites/us/hackathon-demo-page.html
======================================================================
```

### Step 4 (Common): Verify in AEM

1. **Open in Author Mode:**
   ```
   http://localhost:4502/editor.html/content/mohhwebsites/us/hackathon-demo-page.html
   ```

2. **Check CRXDE Lite:**
   ```
   http://localhost:4502/crx/de/index.jsp#/content/mohhwebsites/us/hackathon-demo-page/jcr:content/root/container/container
   ```

3. **Verify Components:**
   - `hero_carousel` - Should have 2 slides with all properties
   - `four_card_carousel` - Should have 4 cards with links

4. **Verify Component Data:**

   **For Demo Data:**
   - HeroCarousel Slide 1: "Excellence in Healthcare"
   - TeaserGrid Cards: Cardiac Care, Emergency Care, Surgical Services, Patient Care

   **For Physician Data:**
   - HeroCarousel Slide 1: "The heart of public healthcare"
   - TeaserGrid Cards: Medicine, Residency, Grants, Dentistry

## Expected JCR Structure

After migration, you should see:

```
/content/mohhwebsites/us/hackathon-demo-page
  /jcr:content
    /root
      /container
        /demoHeroCarousel
          @sling:resourceType = "mohhwebsites/components/herocarousel"
          @autoRotateEnabled = true
          @autoRotateInterval = 7
          /slides
            /item0
              @backgroundImage = "/content/dam/mohhwebsites/mohh-hero-carousel-desktop.jpg"
              @headline = "Excellence in Healthcare"
              /primaryCTA
                @text = "Our Services"
                @url = "/content/mohhwebsites/us/services"
            /item1
              @backgroundImage = "/content/dam/mohhwebsites/mohh-hero-career.jpg"
              @headline = "Join Our Team"
        /demoTeaserGrid
          @sling:resourceType = "mohhwebsites/components/teasergridcardfour"
          @headerTitle = "Our Healthcare"
          @headerSubtitle = "Services"
          /cards
            /item0
              @title = "Cardiac Care"
              @image = "/content/dam/mohhwebsites/mohh-hero-carousel-desktop.jpg"
              /links
                /item0 (@text, @url)
                /item1 (@text, @url)
            /item1...
            /item2...
            /item3...
```

## Data Conversion Details

### What convert_to_aem.py Does

1. **Reads** source website JSON (`www_physician_mohh_com_sg.json`)
2. **Extracts** herobanner and teaser components
3. **Maps** fields to AEM component structure:
   - `herobanner.heading` → `herocarousel.slideHeading`
   - `herobanner.description` → `herocarousel.slideDescription`
   - `teaser.cards[].title` → `teasergridcardfour.cards[].title`
   - `teaser.cards[].description` → `teasergridcardfour.cards[].description`
   - And more... (see FIELD_MAPPING.md for complete list)
4. **Generates** AEM-specific fields (settings, colors, etc.)
5. **Outputs** to `physician_mohh_aem.json`

### Key Conversion Rules

- **Images**: Uses only available AEM images (mohh-hero-carousel-desktop.jpg, mohh-hero-career.jpg)
- **Links**: All URLs set to `/content/mohhwebsites` (as specified)
- **Slides**: Extracts from source + generates second slide if needed
- **Cards**: Processes up to 4 cards from source teaser component
- **Field Names**: Exact mapping documented in FIELD_MAPPING.md

### Customizing Conversion

Edit `convert_to_aem.py` to customize:

```python
# Change default link URL
DEFAULT_LINK_URL = '/content/mohhwebsites'  # ← Modify this

# Change available images
AVAILABLE_IMAGES = [
    '/content/dam/mohhwebsites/mohh-hero-carousel-desktop.jpg',
    '/content/dam/mohhwebsites/mohh-hero-career.jpg'
]  # ← Add more images here

# Change target page
TARGET_PAGE = '/content/mohhwebsites/us/hackathon-demo-page'  # ← Modify this
```

---

## Troubleshooting

### Error: "Source file not found: www_physician_mohh_com_sg.json"

**Problem:** Source website JSON file missing

**Solution:**
- Ensure `www_physician_mohh_com_sg.json` exists in the same folder
- Check file name spelling (case sensitive on Linux/Mac)

### Error: "No components found in source data"

**Problem:** Source JSON has unexpected structure

**Solution:**
- Verify source JSON has `page.content.components` structure
- Check components array is not empty
- Run: `python -c "import json; print(json.load(open('www_physician_mohh_com_sg.json'))['page']['content']['components'][:2])"`

### Error: "Required components not found!"

**Problem:** Missing herobanner or teaser components in source

**Solution:**
- Check source has both herobanner and teaser component types
- Run conversion script - it will show which components are found/missing

### Error: "Page not found"

**Problem:** Target page doesn't exist in AEM

**Solution:** Create the page first:
1. Go to http://localhost:4502/sites.html
2. Navigate to /content/mohhwebsites/us
3. Create new page: "Hackathon Demo Page"

### Error: "Connection refused"

**Problem:** AEM not running or wrong host

**Solution:**
- Check AEM is running: http://localhost:4502
- Verify credentials (default: admin/admin)
- Use correct host: `--host http://localhost:4502`

### Error: "Module 'requests' not found"

**Problem:** Python requests library not installed

**Solution:**
```bash
pip install requests
```

### Images Not Displaying

**Problem:** Images not in DAM

**Solution:** Upload images to AEM Assets:
1. Go to http://localhost:4502/assets.html/content/dam/mohhwebsites
2. Upload `mohh-hero-carousel-desktop.jpg` and `mohh-hero-career.jpg`

### Components Not Rendering

**Problem:** Component definitions might not be deployed

**Solution:**
- Ensure component code is deployed to AEM
- Check component resource type matches:
  - `mohhwebsites/components/herocarousel`
  - `mohhwebsites/components/teasergridcardfour`

## Customizing Data

### Change Component Names

Edit `demo-components.json`:

```json
{
  "componentName": "myCustomName"  // ← Change this
}
```

### Change Target Page

Use command line:
```bash
python migrate.py --page /content/mohhwebsites/us/my-other-page
```

### Add More Slides/Cards

Edit `demo-components.json` and add more items to `slides` or `cards` arrays.

### Change Images

Edit `demo-components.json` and update image paths:
```json
{
  "image": "/content/dam/mohhwebsites/your-image.jpg"
}
```

## Environment Variables

Set these to avoid passing parameters every time:

```bash
# Windows (PowerShell)
$env:AEM_HOST = "http://localhost:4502"
$env:AEM_USER = "admin"
$env:AEM_PASS = "admin"

# Windows (CMD)
set AEM_HOST=http://localhost:4502
set AEM_USER=admin
set AEM_PASS=admin

# Linux/Mac
export AEM_HOST=http://localhost:4502
export AEM_USER=admin
export AEM_PASS=admin
```

Then run:
```bash
python migrate.py --page /content/mohhwebsites/us/hackathon-demo-page
```

## Advanced Options

### Migrate to Different Container

```bash
python migrate.py --page /content/mohhwebsites/us/hackathon-demo-page \
  --container /jcr:content/root/responsivegrid
```

### Use Different JSON File

```bash
python migrate.py --page /content/mohhwebsites/us/hackathon-demo-page \
  --json my-custom-data.json
```

## Quick Reference

### Conversion Commands

| Command | Description |
|---------|-------------|
| `python convert_to_aem.py` | Convert website data to AEM format |
| `cat www_physician_mohh_com_sg.json` | View source website data |
| `cat physician_mohh_aem.json` | View converted AEM data |
| `cat FIELD_MAPPING.md` | View field mapping documentation |

### Migration Commands

| Command | Description |
|---------|-------------|
| `python migrate.py` | Migrate components to AEM |
| `python migrate.py --dry-run` | Test without changes |
| `cat demo-components.json` | View demo JSON data |

### Complete Workflow

```bash
# Workflow 1: Demo Data
python migrate.py

# Workflow 2: Real Website Data
python convert_to_aem.py    # Convert
python migrate.py           # Migrate
```

## Success Criteria

✅ Script runs without errors
✅ Exit code 0
✅ Both components show "✓ Success"
✅ Components visible in AEM Author
✅ All images display correctly
✅ All links are clickable
✅ Auto-rotation works (HeroCarousel and TeaserGrid)

---

**Ready for your hackathon demo! 🚀**
