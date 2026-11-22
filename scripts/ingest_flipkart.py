import sys
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

import json
import re
import math
import pandas as pd

RAW_FLIPKART_PATH = BASE_DIR / "data" / "flipkart_com-ecommerce_sample.csv"
OUTPUT_PRODUCTS_PATH = BASE_DIR / "data" / "products.csv"

# Core curated appliance catalog ensuring 100% coverage for home appliances, ACs, TVs, etc.
CURATED_APPLIANCES = [
    {
        'product_id': 'REF-001',
        'name': 'Whirlpool 192L 3-Star Single Door Refrigerator',
        'category': 'refrigerator',
        'brand': 'Whirlpool',
        'price_inr': 15990,
        'capacity': '192L',
        'energy_rating': 3,
        'specs_json': '{"door_type": "Single Door", "compressor": "Reciprocating", "stabilizer_free": true, "freezer_capacity": "14.3L", "defrost": "Manual", "warranty_years": 1}',
        'key_pros': 'Lowest upfront cost; Stabilizer-free (130V-300V); Ideal for singles and bachelor pads',
        'key_cons': 'Requires manual defrosting; Limited freezer space; No inverter motor'
    },
    {
        'product_id': 'REF-002',
        'name': 'Godrej 180L 4-Star Inverter Single Door Refrigerator',
        'category': 'refrigerator',
        'brand': 'Godrej',
        'price_inr': 15290,
        'capacity': '180L',
        'energy_rating': 4,
        'specs_json': '{"door_type": "Single Door", "compressor": "Advanced Inverter", "stabilizer_free": true, "defrost": "Manual", "warranty_years": 1}',
        'key_pros': 'High 4-star energy savings; Inverter compressor at entry price; Compact kitchen footprint',
        'key_cons': 'Direct cool manual defrost; Compact capacity unsuitable for >2 people'
    },
    {
        'product_id': 'REF-003',
        'name': 'Samsung 236L 3-Star Digital Inverter Double Door Refrigerator',
        'category': 'refrigerator',
        'brand': 'Samsung',
        'price_inr': 24990,
        'capacity': '236L',
        'energy_rating': 3,
        'specs_json': '{"door_type": "Double Door", "compressor": "Digital Inverter", "cooling_tech": "All Around Cooling", "defrost": "Frost-Free", "warranty_years": 1}',
        'key_pros': 'True frost-free convenience; Reliable digital inverter; Perfect sweet-spot for small family of 2-3',
        'key_cons': '3-star efficiency is average; Lacks convertible vegetable/fridge modes'
    },
    {
        'product_id': 'REF-004',
        'name': 'LG 242L 3-Star Smart Inverter Double Door Refrigerator',
        'category': 'refrigerator',
        'brand': 'LG',
        'price_inr': 25999,
        'capacity': '242L',
        'energy_rating': 3,
        'specs_json': '{"door_type": "Double Door", "compressor": "Smart Inverter", "cooling_tech": "Door Cooling+", "defrost": "Frost-Free", "stabilizer_free": true}',
        'key_pros': 'Door Cooling+ ensures vents chill door baskets evenly; Auto smart connect to home inverter',
        'key_cons': 'Slightly above ₹25k limit; Specific warranty duration not stated in catalog'
    },
    {
        'product_id': 'REF-005',
        'name': 'Haier 325L 3-Star Triple Inverter Bottom Mount Refrigerator',
        'category': 'refrigerator',
        'brand': 'Haier',
        'price_inr': 34990,
        'capacity': '325L',
        'energy_rating': 3,
        'specs_json': '{"door_type": "Bottom Mount Double Door", "compressor": "Triple Inverter", "cooling_tech": "1 Hour Icing", "convertible_modes": 14, "warranty_years": 2}',
        'key_pros': 'Bottom mounted freezer eliminates 90% bending for daily items; 14-in-1 convertible flexi storage',
        'key_cons': 'Takes wider floor space; Higher power consumption than single doors'
    },
    {
        'product_id': 'REF-006',
        'name': 'LG 343L 3-Star Frost-Free Double Door Convertible',
        'category': 'refrigerator',
        'brand': 'LG',
        'price_inr': 38990,
        'capacity': '343L',
        'energy_rating': 3,
        'specs_json': '{"door_type": "Double Door", "compressor": "Smart Inverter", "cooling_tech": "Door Cooling+", "convertible": true, "warranty_years": 1}',
        'key_pros': 'Large capacity for 4-5 member families; Convertible freezer to fridge; Toughened glass shelves',
        'key_cons': 'Pricier; Bulkier dimensions require measured kitchen space'
    },
    {
        'product_id': 'REF-007',
        'name': 'Samsung 653L 3-Star Side-by-Side Convertible Refrigerator',
        'category': 'refrigerator',
        'brand': 'Samsung',
        'price_inr': 79990,
        'capacity': '653L',
        'energy_rating': 3,
        'specs_json': '{"door_type": "Side-by-Side", "compressor": "Digital Inverter", "cooling_tech": "Twin Cooling Plus", "wifi_enabled": true, "warranty_years": 1}',
        'key_pros': 'Massive 653L capacity for large households; SmartThings Wi-Fi control; Twin Cooling prevents odor mixing',
        'key_cons': 'Requires wide kitchen entrance; High electricity consumption; Premium price tag'
    },
    {
        'product_id': 'REF-008',
        'name': 'Hisense 45L Single Door Mini Refrigerator / Minibar',
        'category': 'refrigerator',
        'brand': 'Hisense',
        'price_inr': 8490,
        'capacity': '45L',
        'energy_rating': '',
        'specs_json': '{"door_type": "Mini Single Door", "compressor": "Standard", "reversible_door": true, "chiller_zone": true, "warranty_years": 1}',
        'key_pros': 'Ultra-compact mini fridge; Reversible door hinge; Great for bedrooms, hostels and office cabins',
        'key_cons': 'No dedicated deep freezer; Manual temperature knob; Not star-rated by BEE'
    },
    {
        'product_id': 'WM-001',
        'name': 'Whirlpool 7 Kg 5-Star Superb Atom Semi-Automatic Washing Machine',
        'category': 'washing_machine',
        'brand': 'Whirlpool',
        'price_inr': 9990,
        'capacity': '7.0 kg',
        'energy_rating': 5,
        'specs_json': '{"type": "Semi-Automatic", "motor": "Heavy Duty", "max_rpm": 1400, "water_proof_panel": true, "warranty_years": 2}',
        'key_pros': 'Unbeatable sub-10k price; 1400 RPM high spin speed dries clothes rapidly; Rust-proof body',
        'key_cons': 'Requires manual intervention to move clothes to spin tub; High manual effort'
    },
    {
        'product_id': 'WM-002',
        'name': 'Samsung 7 Kg 5-Star Inverter Fully Automatic Top Load',
        'category': 'washing_machine',
        'brand': 'Samsung',
        'price_inr': 17490,
        'capacity': '7.0 kg',
        'energy_rating': 5,
        'specs_json': '{"type": "Top Load", "motor": "Digital Inverter", "max_rpm": 700, "technology": "Ecobubble & Wobble", "warranty_years": 3}',
        'key_pros': 'Top energy efficiency; Ecobubble deep cleans at low temps; Wobble pulsator prevents tangling',
        'key_cons': 'No in-built hot water heater; Lower spin RPM compared to front-loaders'
    },
    {
        'product_id': 'WM-003',
        'name': 'LG 7 Kg 5-Star Smart Inverter Fully Automatic Top Load',
        'category': 'washing_machine',
        'brand': 'LG',
        'price_inr': 18990,
        'capacity': '7.0 kg',
        'energy_rating': 5,
        'specs_json': '{"type": "Top Load", "motor": "Smart Inverter", "max_rpm": 780, "technology": "TurboDrum", "warranty_years": 2}',
        'key_pros': 'Smart Inverter saves electricity; TurboDrum dual-motion wash cleans tough stains; Auto restart',
        'key_cons': 'Lacks steam wash; Top load design uses more water than front loaders'
    },
    {
        'product_id': 'WM-004',
        'name': 'LG 7 Kg 5-Star Inverter Direct Drive Front Load',
        'category': 'washing_machine',
        'brand': 'LG',
        'price_inr': 28990,
        'capacity': '7.0 kg',
        'energy_rating': 5,
        'specs_json': '{"type": "Front Load", "motor": "Inverter Direct Drive", "max_rpm": 1200, "heater": true, "steam_wash": true, "warranty_years": 2}',
        'key_pros': 'Direct Drive motor eliminates belts for ultra-quiet operation; Steam Allergy Care; In-built 60C heater',
        'key_cons': 'Higher price point; Requires continuous pressurized water supply'
    },
    {
        'product_id': 'WM-005',
        'name': 'IFB 8 Kg 5-Star AI Powered Front Load Washing Machine',
        'category': 'washing_machine',
        'brand': 'IFB',
        'price_inr': 36990,
        'capacity': '8.0 kg',
        'energy_rating': 5,
        'specs_json': '{"type": "Front Load", "motor": "AI Inverter", "max_rpm": 1400, "heater": true, "steam_wash": true}',
        'key_pros': 'AI fabric detector selects optimal drum motions; 95C hot water sanitization; 8kg family capacity',
        'key_cons': 'Premium price; Warranty terms not explicitly specified in record'
    },
    {
        'product_id': 'WM-006',
        'name': 'Bosch 8 Kg 5-Star Series 6 Inverter Front Load',
        'category': 'washing_machine',
        'brand': 'Bosch',
        'price_inr': 42990,
        'capacity': '8.0 kg',
        'energy_rating': 5,
        'specs_json': '{"type": "Front Load", "motor": "EcoSilence Drive", "max_rpm": 1400, "heater": true, "anti_tangle": true, "warranty_years": 2}',
        'key_pros': 'German engineering build quality; EcoSilence Drive motor is practically noiseless; Anti-tangle wash',
        'key_cons': 'Spare parts can be expensive; Long cycle times on intensive cotton settings'
    },
    {
        'product_id': 'LAP-001',
        'name': 'Lenovo IdeaPad Slim 3 (Core i3 12th Gen / 8GB / 512GB SSD)',
        'category': 'laptop',
        'brand': 'Lenovo',
        'price_inr': 34990,
        'capacity': '15.6 inch',
        'energy_rating': '',
        'specs_json': '{"cpu": "Intel Core i3-1215U", "ram": "8GB DDR4", "storage": "512GB NVMe SSD", "display": "FHD Anti-Glare", "weight_kg": 1.63, "battery_hours": 6, "warranty_years": 1}',
        'key_pros': 'Superb value under ₹35k; Fast 512GB NVMe SSD; Comfortable keyboard for typing',
        'key_cons': '8GB RAM is soldered (limited future upgrade); Unsuitable for heavy video editing or gaming'
    },
    {
        'product_id': 'LAP-002',
        'name': 'HP 15s (AMD Ryzen 5 5500U / 16GB / 512GB SSD)',
        'category': 'laptop',
        'brand': 'HP',
        'price_inr': 41990,
        'capacity': '15.6 inch',
        'energy_rating': '',
        'specs_json': '{"cpu": "AMD Ryzen 5 5500U 6-Core", "ram": "16GB DDR4", "storage": "512GB SSD", "display": "FHD IPS Micro-Edge", "weight_kg": 1.69, "fast_charge": true, "warranty_years": 1}',
        'key_pros': '16GB RAM out of the box for effortless multitasking; 6-core Ryzen 5 handles programming & Docker',
        'key_cons': 'Plastic build; No keyboard backlighting; Moderate speakers'
    },
    {
        'product_id': 'LAP-003',
        'name': 'ASUS Vivobook 16 (Ryzen 5 7530U / 16GB / 512GB SSD)',
        'category': 'laptop',
        'brand': 'ASUS',
        'price_inr': 46990,
        'capacity': '16.0 inch',
        'energy_rating': '',
        'specs_json': '{"cpu": "AMD Ryzen 5 7530U", "ram": "16GB DDR4", "storage": "512GB SSD", "display": "16-inch WUXGA 16:10", "weight_kg": 1.88, "warranty_years": 1}',
        'key_pros': 'Modern 16:10 tall display gives extra vertical lines for coding; 180-degree lay-flat hinge',
        'key_cons': 'Display peak brightness nits missing in catalog; No dedicated graphics card'
    },
    {
        'product_id': 'LAP-004',
        'name': 'Acer Nitro V Gaming (Core i5 13th Gen / RTX 4050 / 16GB / 512GB)',
        'category': 'laptop',
        'brand': 'Acer',
        'price_inr': 69990,
        'capacity': '15.6 inch',
        'energy_rating': '',
        'specs_json': '{"cpu": "Intel Core i5-13420H", "ram": "16GB DDR5", "storage": "512GB SSD", "gpu": "NVIDIA RTX 4050 6GB GDDR6", "refresh_rate": "144Hz", "weight_kg": 2.1}',
        'key_pros': 'Dedicated RTX 4050 GPU runs AAA games & AI training; 144Hz smooth gaming panel; Fast DDR5 memory',
        'key_cons': 'Heavy charging brick; Short 3-4 hr battery life; Catalog lacks stated warranty period'
    },
    {
        'product_id': 'LAP-005',
        'name': 'Apple MacBook Air M2 (8GB Unified / 256GB SSD)',
        'category': 'laptop',
        'brand': 'Apple',
        'price_inr': 84990,
        'capacity': '13.6 inch',
        'energy_rating': '',
        'specs_json': '{"cpu": "Apple M2 8-Core CPU / 8-Core GPU", "ram": "8GB Unified", "storage": "256GB SSD", "display": "Liquid Retina", "battery_hours": 18, "weight_kg": 1.24, "warranty_years": 1}',
        'key_pros': 'Unrivaled 18-hour battery longevity; Silent fanless unibody design; Superior display & trackpad',
        'key_cons': 'Non-upgradable 256GB base storage; High starting cost'
    },
    {
        'product_id': 'AC-001',
        'name': 'Voltas 1 Ton 3-Star Inverter Split AC',
        'category': 'air_conditioner',
        'brand': 'Voltas',
        'price_inr': 28490,
        'capacity': '1.0 Ton',
        'energy_rating': 3,
        'specs_json': '{"type": "Split Inverter", "copper_condenser": true, "stabilizer_free": true, "room_size_sqft": "up to 110 sq ft"}',
        'key_pros': 'Affordable entry into split inverter cooling; 100% copper condenser; Good for small study rooms',
        'key_cons': 'Only 1 Ton capacity (inadequate for medium/large rooms); Warranty unstated in catalog'
    },
    {
        'product_id': 'AC-002',
        'name': 'Daikin 1.5 Ton 3-Star Inverter Split AC',
        'category': 'air_conditioner',
        'brand': 'Daikin',
        'price_inr': 36990,
        'capacity': '1.5 Ton',
        'energy_rating': 3,
        'specs_json': '{"type": "Split Inverter", "copper_condenser": true, "pm25_filter": true, "refrigerant": "R32", "room_size_sqft": "111-150 sq ft", "warranty_years": 1}',
        'key_pros': 'Cools effectively even at 52C ambient heat; Copper condenser tubes; PM 2.5 air filtration',
        'key_cons': '3-star model consumes roughly 15-20% more power than 5-star inverter equivalents'
    },
    {
        'product_id': 'AC-003',
        'name': 'Panasonic 1.5 Ton 5-Star Smart Wi-Fi Inverter Split AC',
        'category': 'air_conditioner',
        'brand': 'Panasonic',
        'price_inr': 43990,
        'capacity': '1.5 Ton',
        'energy_rating': 5,
        'specs_json': '{"type": "Split Inverter", "copper_condenser": true, "wifi_enabled": true, "ai_mode": true, "room_size_sqft": "120-170 sq ft", "warranty_years": 1}',
        'key_pros': 'Maximum 5-star power bill savings; Miraie smart app & Alexa voice control; AI adaptive cooling',
        'key_cons': 'Higher initial investment; Requires dependable home Wi-Fi for smart capabilities'
    },
    {
        'product_id': 'MIC-001',
        'name': 'LG 20L Solo Microwave Oven',
        'category': 'microwave',
        'brand': 'LG',
        'price_inr': 5890,
        'capacity': '20L',
        'energy_rating': '',
        'specs_json': '{"type": "Solo", "power_wattage": 700, "control": "Mechanical Dials", "warranty_years": 1}',
        'key_pros': 'Extremely budget-friendly; Mechanical dial control is intuitive for seniors; Fast reheating',
        'key_cons': 'Cannot bake cakes, roast or grill; Small 20L cavity limited to single dinner plates'
    },
    {
        'product_id': 'MIC-003',
        'name': 'Samsung 28L Convection Microwave Oven',
        'category': 'microwave',
        'brand': 'Samsung',
        'price_inr': 12490,
        'capacity': '28L',
        'energy_rating': '',
        'specs_json': '{"type": "Convection", "power_wattage": 900, "tandoor_tech": true, "fermentation_curd": true, "warranty_years": 1}',
        'key_pros': 'All-in-one baking, grilling, tandoor & curd making; SlimFry technology for low-oil frying',
        'key_cons': 'Consumes larger countertop real estate; Metal racks require manual cleaning'
    },
    {
        'product_id': 'TV-001',
        'name': 'Mi 32-inch A Series HD Ready Smart Google TV',
        'category': 'television',
        'brand': 'Xiaomi',
        'price_inr': 12499,
        'capacity': '32 inch',
        'energy_rating': '',
        'specs_json': '{"display_type": "HD Ready LED", "resolution": "1366x768", "refresh_rate": "60Hz", "os": "Google TV", "audio_wattage": 20, "warranty_years": 1}',
        'key_pros': 'Affordable smart TV; Built-in Google TV OS with Play Store, Netflix, Prime; Dual 20W speakers',
        'key_cons': '720p HD resolution only (not Full HD); Modest viewing angles in brightly lit rooms'
    },
    {
        'product_id': 'TV-002',
        'name': 'LG 43-inch 4K Ultra HD Smart LED TV',
        'category': 'television',
        'brand': 'LG',
        'price_inr': 31990,
        'capacity': '43 inch',
        'energy_rating': '',
        'specs_json': '{"display_type": "4K Ultra HD IPS LED", "resolution": "3840x2160", "refresh_rate": "60Hz", "os": "webOS", "hdr": "HDR10 Pro", "processor": "alpha5 AI Gen6", "warranty_years": 1}',
        'key_pros': 'Vibrant 4K IPS panel with wide viewing angles; Magic Remote with point-and-click air mouse',
        'key_cons': 'Native 60Hz panel (no 120Hz for PS5 gaming); Basic black level depth in dark rooms'
    },
    {
        'product_id': 'AUD-002',
        'name': 'Sony WH-1000XM5 Wireless Active Noise Canceling Headphones',
        'category': 'audio',
        'brand': 'Sony',
        'price_inr': 26990,
        'capacity': 'Over-Ear',
        'energy_rating': '',
        'specs_json': '{"type": "Over-Ear Wireless", "anc": "Dual Processor V1 + HD QN1", "battery_hours": 30, "codecs": "LDAC, AAC, SBC", "weight_g": 250, "warranty_years": 1}',
        'key_pros': 'Class-leading Active Noise Cancellation shuts out airplane & cafe noise; Hi-Res LDAC audio; 30hr battery',
        'key_cons': 'Earcups do not fold inward into compact ball; Premium pricing'
    },
    {
        'product_id': 'SMR-002',
        'name': 'Ecovacs Deebot Y1 Pro 2-in-1 Robot Vacuum Cleaner & Mop',
        'category': 'smart_home',
        'brand': 'Ecovacs',
        'price_inr': 24900,
        'capacity': 'Robot Vacuum',
        'energy_rating': '',
        'specs_json': '{"type": "Robot Vacuum & Mop", "suction_pa": 6500, "navigation": "LDS LiDAR LDS 360", "battery_mah": 5200, "warranty_years": 1}',
        'key_pros': 'Simultaneous vacuuming and wet mopping; Precision LiDAR navigation maps multi-story homes; Strong suction',
        'key_cons': 'Requires cleaning hair tangled on roller brush weekly; Struggles with thick door mats'
    }
]

def parse_flipkart_specs(specs_str):
    if not isinstance(specs_str, str) or not specs_str.strip():
        return {}
    try:
        clean_str = specs_str.replace('=>', ':')
        data = json.loads(clean_str)
        spec_list = data.get('product_specification', [])
        result = {}
        for item in spec_list:
            if isinstance(item, dict):
                k = item.get('key')
                v = item.get('value')
                if k and v:
                    result[k.strip()] = str(v).strip()
        return result
    except Exception:
        kv = re.findall(r'\"key\"\s*:\s*\"(.*?)\".*?\"value\"\s*:\s*\"(.*?)\"', str(specs_str).replace('=>', ':'))
        return {k.strip(): v.strip() for k, v in kv}

def ingest_flipkart_data():
    print(f"Reading raw Flipkart CSV from {RAW_FLIPKART_PATH}...")
    df = pd.read_csv(RAW_FLIPKART_PATH)
    print(f"Raw rows: {len(df)}")

    curated_df = pd.DataFrame(CURATED_APPLIANCES)
    print(f"Curated baseline products: {len(curated_df)}")

    new_items = []
    for idx, row in df.iterrows():
        cat_tree = str(row['product_category_tree'])
        pname = str(row['product_name'])

        is_tech = False
        assigned_cat = None

        if 'Routers' in cat_tree or 'Router' in pname:
            assigned_cat = 'router'
            is_tech = True
        elif 'Headphones' in cat_tree or 'Earphones' in pname or 'Headphone' in pname:
            assigned_cat = 'audio'
            is_tech = True
        elif 'Laptop Accessories' in cat_tree or ('Laptop' in pname and 'Skin' not in cat_tree and 'Cover' not in cat_tree):
            assigned_cat = 'laptop'
            is_tech = True
        elif 'Printers' in cat_tree or 'Printer' in pname:
            assigned_cat = 'printer'
            is_tech = True
        elif 'Cameras' in cat_tree and ('Battery' in pname or 'Charger' in pname or 'Lens' in pname):
            assigned_cat = 'camera'
            is_tech = True
        elif 'Power Bank' in pname or 'Chargers' in cat_tree:
            assigned_cat = 'mobile_accessory'
            is_tech = True

        if is_tech:
            price = row['discounted_price']
            if pd.isna(price) or str(price).strip() == '':
                price = row['retail_price']
            try:
                price_val = float(price)
                if math.isnan(price_val) or price_val <= 0:
                    continue
            except (ValueError, TypeError):
                continue

            specs = parse_flipkart_specs(row['product_specifications'])
            brand = str(row['brand']).strip() if pd.notna(row['brand']) and str(row['brand']).strip() else 'Flipkart Seller'

            warranty = specs.get('Warranty Summary') or specs.get('Covered in Warranty') or specs.get('Warranty')
            pros = f"Authentic Flipkart listing; {specs.get('Type', 'Electronic device/accessory')}; Brand: {brand}"
            cons = "Standard e-commerce return policy; " + (f"Warranty: {warranty}" if warranty else "Warranty details not specified in catalog")

            new_items.append({
                'product_id': f"FK-{str(row['uniq_id'])[:8].upper()}",
                'name': pname,
                'category': assigned_cat,
                'brand': brand,
                'price_inr': int(price_val),
                'capacity': specs.get('Capacity') or specs.get('Size') or '',
                'energy_rating': '',
                'specs_json': json.dumps(specs),
                'key_pros': pros,
                'key_cons': cons
            })

    new_df = pd.DataFrame(new_items)
    print(f"Parsed {len(new_df)} authentic electronic/tech products from Flipkart dataset.")

    # Combine curated appliances + Flipkart products
    combined_df = pd.concat([curated_df, new_df], ignore_index=True)
    combined_df = combined_df.drop_duplicates(subset=['product_id'])
    
    combined_df.to_csv(OUTPUT_PRODUCTS_PATH, index=False)
    print(f"Successfully saved combined dataset with {len(combined_df)} products to {OUTPUT_PRODUCTS_PATH}!")
    print("\nCategory breakdown in merged catalog:")
    print(combined_df['category'].value_counts())

if __name__ == "__main__":
    ingest_flipkart_data()
