import csv
import json

# Comprehensive, realistic, diversified catalog of actual electrical & electronic products
# across 8 categories, covering budget, mid-range, and premium price tiers.
PRODUCTS = [
    # ==================== REFRIGERATORS ====================
    {
        "product_id": "REF-001",
        "name": "Hisense 45L Single Door Mini Refrigerator / Minibar",
        "category": "refrigerator",
        "brand": "Hisense",
        "price_inr": 8490,
        "capacity": "45L",
        "energy_rating": 2,
        "specs_json": json.dumps({"door_type": "Mini Bar", "compressor": "Standard", "defrost": "Manual", "warranty_years": 1, "noise_db": 38}),
        "key_pros": "Ultra-compact footprint; Reversible door hinge; Great for bedrooms, dorms, and office cabins",
        "key_cons": "Small 45L volume; No separate freezer compartment"
    },
    {
        "product_id": "REF-002",
        "name": "Godrej 180L 4-Star Inverter Single Door Refrigerator",
        "category": "refrigerator",
        "brand": "Godrej",
        "price_inr": 15290,
        "capacity": "180L",
        "energy_rating": 4,
        "specs_json": json.dumps({"door_type": "Single Door", "compressor": "Advanced Inverter", "stabilizer_free": True, "defrost": "Direct Cool", "warranty_years": 1}),
        "key_pros": "High 4-star energy efficiency; Advanced inverter compressor; Sturdy wire shelves",
        "key_cons": "Direct cool requires periodic manual defrosting; Compact for families above 2 members"
    },
    {
        "product_id": "REF-003",
        "name": "Whirlpool 192L 3-Star Single Door Direct Cool Refrigerator",
        "category": "refrigerator",
        "brand": "Whirlpool",
        "price_inr": 15990,
        "capacity": "192L",
        "energy_rating": 3,
        "specs_json": json.dumps({"door_type": "Single Door", "compressor": "Reciprocating", "stabilizer_free": True, "freezer_capacity": "14.3L", "warranty_years": 1}),
        "key_pros": "Lowest upfront price; Operates stabilizer-free (130V-300V); Insulated capillary technology",
        "key_cons": "Manual defrosting required; Non-inverter compressor"
    },
    {
        "product_id": "REF-004",
        "name": "Haier 190L 5-Star Inverter Direct Cool Single Door Refrigerator",
        "category": "refrigerator",
        "brand": "Haier",
        "price_inr": 17490,
        "capacity": "190L",
        "energy_rating": 5,
        "specs_json": json.dumps({"door_type": "Single Door", "compressor": "Inverter", "cooling_tech": "1 Hour Icing Tech", "stabilizer_free": True, "warranty_years": 2}),
        "key_pros": "Maximum 5-star electricity savings; Fast 1-hour ice making; Toughened glass shelves",
        "key_cons": "Direct cool manual defrost; Single door layout"
    },
    {
        "product_id": "REF-005",
        "name": "Samsung 236L 3-Star Digital Inverter Double Door Refrigerator",
        "category": "refrigerator",
        "brand": "Samsung",
        "price_inr": 24990,
        "capacity": "236L",
        "energy_rating": 3,
        "specs_json": json.dumps({"door_type": "Double Door", "compressor": "Digital Inverter", "cooling_tech": "All Around Cooling", "defrost": "Frost-Free", "warranty_years": 1}),
        "key_pros": "True frost-free convenience; Digital Inverter adjusts speed automatically; Ideal for 2-3 members",
        "key_cons": "3-star efficiency is average; Lacks convertible storage modes"
    },
    {
        "product_id": "REF-006",
        "name": "LG 242L 3-Star Smart Inverter Double Door Refrigerator",
        "category": "refrigerator",
        "brand": "LG",
        "price_inr": 25999,
        "capacity": "242L",
        "energy_rating": 3,
        "specs_json": json.dumps({"door_type": "Double Door", "compressor": "Smart Inverter", "cooling_tech": "Door Cooling+", "defrost": "Frost-Free", "stabilizer_free": True}),
        "key_pros": "Door Cooling+ vents chill door baskets evenly; Auto-connects to home inverter",
        "key_cons": "Slightly exceeds ₹25k limit; Specific warranty duration not stated in catalog"
    },
    {
        "product_id": "REF-007",
        "name": "Whirlpool 265L 3-Star IntelliFresh Inverter Double Door",
        "category": "refrigerator",
        "brand": "Whirlpool",
        "price_inr": 27490,
        "capacity": "265L",
        "energy_rating": 3,
        "specs_json": json.dumps({"door_type": "Double Door", "compressor": "IntelliSense Inverter", "convertible_modes": 5, "warranty_years": 1}),
        "key_pros": "5-in-1 convertible modes; Microblock technology prevents 99% bacterial growth; FreshFlow air tower",
        "key_cons": "Slightly higher power consumption than 4-star models"
    },
    {
        "product_id": "REF-008",
        "name": "Haier 325L 3-Star Triple Inverter Bottom Mount Refrigerator",
        "category": "refrigerator",
        "brand": "Haier",
        "price_inr": 34990,
        "capacity": "325L",
        "energy_rating": 3,
        "specs_json": json.dumps({"door_type": "Bottom Mount Double Door", "compressor": "Triple Inverter", "cooling_tech": "1 Hour Icing", "convertible_modes": 14, "warranty_years": 2}),
        "key_pros": "Bottom mounted freezer reduces bending by 90%; 14-in-1 convertible flexi storage; 325L capacity",
        "key_cons": "Takes wider kitchen floor space; Higher power draw than single doors"
    },
    {
        "product_id": "REF-009",
        "name": "LG 343L 3-Star Frost-Free Double Door Convertible",
        "category": "refrigerator",
        "brand": "LG",
        "price_inr": 38990,
        "capacity": "343L",
        "energy_rating": 3,
        "specs_json": json.dumps({"door_type": "Double Door", "compressor": "Smart Inverter", "cooling_tech": "Door Cooling+", "convertible": True, "warranty_years": 1}),
        "key_pros": "Spacious for 4-5 member families; Convertible freezer to fridge; Toughened glass shelves",
        "key_cons": "Pricier; Bulkier dimensions require measured kitchen space"
    },
    {
        "product_id": "REF-010",
        "name": "Samsung 653L 3-Star Side-by-Side Convertible Refrigerator",
        "category": "refrigerator",
        "brand": "Samsung",
        "price_inr": 79990,
        "capacity": "653L",
        "energy_rating": 3,
        "specs_json": json.dumps({"door_type": "Side-by-Side", "compressor": "Digital Inverter", "cooling_tech": "Twin Cooling Plus", "wifi_enabled": True, "warranty_years": 1}),
        "key_pros": "Massive 653L capacity for large households; SmartThings Wi-Fi control; Twin Cooling prevents odor mixing",
        "key_cons": "Requires wide kitchen entrance; High electricity consumption; Premium price tag"
    },

    # ==================== WASHING MACHINES ====================
    {
        "product_id": "WM-001",
        "name": "Whirlpool 7 Kg 5-Star Superb Atom Semi-Automatic Washing Machine",
        "category": "washing_machine",
        "brand": "Whirlpool",
        "price_inr": 9990,
        "capacity": "7.0 kg",
        "energy_rating": 5,
        "specs_json": json.dumps({"type": "Semi-Automatic", "motor": "Heavy Duty", "max_rpm": 1400, "water_proof_panel": True, "warranty_years": 2}),
        "key_pros": "Unbeatable sub-10k price; 1400 RPM high spin speed dries clothes rapidly; Rust-proof body",
        "key_cons": "Requires manual transfer from wash to spin tub; High manual effort"
    },
    {
        "product_id": "WM-002",
        "name": "Godrej 7 Kg 5-Star I-Wash Fully Automatic Top Load",
        "category": "washing_machine",
        "brand": "Godrej",
        "price_inr": 13990,
        "capacity": "7.0 kg",
        "energy_rating": 5,
        "specs_json": json.dumps({"type": "Top Load", "motor": "Standard", "max_rpm": 700, "wash_programs": 5, "warranty_years": 2}),
        "key_pros": "Affordable automatic wash; 5-star energy rating; Toughened glass soft-shut lid",
        "key_cons": "No built-in heater; Limited wash programs compared to inverter models"
    },
    {
        "product_id": "WM-003",
        "name": "Samsung 7 Kg 5-Star Inverter Fully Automatic Top Load",
        "category": "washing_machine",
        "brand": "Samsung",
        "price_inr": 17490,
        "capacity": "7.0 kg",
        "energy_rating": 5,
        "specs_json": json.dumps({"type": "Top Load", "motor": "Digital Inverter", "max_rpm": 700, "technology": "Ecobubble & Wobble", "warranty_years": 3}),
        "key_pros": "Top energy efficiency; Ecobubble deep cleans at low temps; Wobble pulsator prevents tangling",
        "key_cons": "No in-built hot water heater; Lower spin RPM compared to front-loaders"
    },
    {
        "product_id": "WM-004",
        "name": "LG 7 Kg 5-Star Smart Inverter Fully Automatic Top Load",
        "category": "washing_machine",
        "brand": "LG",
        "price_inr": 18990,
        "capacity": "7.0 kg",
        "energy_rating": 5,
        "specs_json": json.dumps({"type": "Top Load", "motor": "Smart Inverter", "max_rpm": 780, "technology": "TurboDrum", "warranty_years": 2}),
        "key_pros": "Smart Inverter saves electricity; TurboDrum dual-motion wash cleans tough stains; Auto restart",
        "key_cons": "Lacks steam wash; Top load design uses more water than front loaders"
    },
    {
        "product_id": "WM-005",
        "name": "Whirlpool 7.5 Kg 5-Star BloomWash Inverter Top Load",
        "category": "washing_machine",
        "brand": "Whirlpool",
        "price_inr": 21990,
        "capacity": "7.5 kg",
        "energy_rating": 5,
        "specs_json": json.dumps({"type": "Top Load", "motor": "Inverter", "max_rpm": 740, "heater": True, "hot_wash": True, "warranty_years": 2}),
        "key_pros": "Built-in heater up to 60C in top-load; Removes up to 50 tough stains; Soft close hydraulic lid",
        "key_cons": "Heavier water consumption during hot wash cycles"
    },
    {
        "product_id": "WM-006",
        "name": "LG 7 Kg 5-Star Inverter Direct Drive Front Load",
        "category": "washing_machine",
        "brand": "LG",
        "price_inr": 28990,
        "capacity": "7.0 kg",
        "energy_rating": 5,
        "specs_json": json.dumps({"type": "Front Load", "motor": "Inverter Direct Drive", "max_rpm": 1200, "heater": True, "steam_wash": True, "warranty_years": 2}),
        "key_pros": "Direct Drive motor eliminates belts for ultra-quiet operation; Steam Allergy Care; In-built 60C heater",
        "key_cons": "Higher price point; Requires continuous pressurized water supply"
    },
    {
        "product_id": "WM-007",
        "name": "Samsung 8 Kg 5-Star AI Control Front Load Washing Machine",
        "category": "washing_machine",
        "brand": "Samsung",
        "price_inr": 34990,
        "capacity": "8.0 kg",
        "energy_rating": 5,
        "specs_json": json.dumps({"type": "Front Load", "motor": "Digital Inverter", "max_rpm": 1400, "heater": True, "ai_control": True, "warranty_years": 3}),
        "key_pros": "AI pattern learning personalizes wash cycles; Hygiene Steam removes 99.9% bacteria; 1400 RPM spin",
        "key_cons": "Smart app setup requires home Wi-Fi; Higher cost"
    },
    {
        "product_id": "WM-008",
        "name": "IFB 8 Kg 5-Star AI Powered Front Load Washing Machine",
        "category": "washing_machine",
        "brand": "IFB",
        "price_inr": 36990,
        "capacity": "8.0 kg",
        "energy_rating": 5,
        "specs_json": json.dumps({"type": "Front Load", "motor": "AI Inverter", "max_rpm": 1400, "heater": True, "steam_wash": True}),
        "key_pros": "AI fabric detector selects optimal drum motions; 95C hot water sanitization; 8kg family capacity",
        "key_cons": "Premium price; Warranty terms not explicitly specified in record"
    },
    {
        "product_id": "WM-009",
        "name": "Bosch 8 Kg 5-Star Series 6 Inverter Front Load",
        "category": "washing_machine",
        "brand": "Bosch",
        "price_inr": 42990,
        "capacity": "8.0 kg",
        "energy_rating": 5,
        "specs_json": json.dumps({"type": "Front Load", "motor": "EcoSilence Drive", "max_rpm": 1400, "heater": True, "anti_tangle": True, "warranty_years": 2}),
        "key_pros": "German engineering build quality; EcoSilence Drive motor is practically noiseless; Anti-tangle wash",
        "key_cons": "Spare parts can be expensive; Long cycle times on intensive cotton settings"
    },

    # ==================== LAPTOPS & COMPUTING ====================
    {
        "product_id": "LAP-001",
        "name": "Acer Aspire Lite (AMD Athlon Silver / 8GB / 256GB SSD)",
        "category": "laptop",
        "brand": "Acer",
        "price_inr": 24990,
        "capacity": "15.6 inch",
        "energy_rating": 3,
        "specs_json": json.dumps({"cpu": "AMD Athlon 3050U", "ram": "8GB DDR4", "storage": "256GB SSD", "display": "HD", "weight_kg": 1.7, "warranty_years": 1}),
        "key_pros": "Very affordable sub-₹25k laptop; Fast SSD storage; Suitable for basic browsing and schooling",
        "key_cons": "Entry-level processor; HD 720p screen resolution; Not for heavy multitasking"
    },
    {
        "product_id": "LAP-002",
        "name": "Lenovo IdeaPad Slim 3 (Core i3 12th Gen / 8GB / 512GB SSD)",
        "category": "laptop",
        "brand": "Lenovo",
        "price_inr": 34990,
        "capacity": "15.6 inch",
        "energy_rating": 4,
        "specs_json": json.dumps({"cpu": "Intel Core i3-1215U", "ram": "8GB DDR4", "storage": "512GB NVMe SSD", "display": "FHD Anti-Glare", "weight_kg": 1.63, "battery_hours": 6, "warranty_years": 1}),
        "key_pros": "Superb value under ₹35k; Fast 512GB NVMe SSD; Comfortable keyboard for typing",
        "key_cons": "8GB RAM is soldered (limited future upgrade); Unsuitable for heavy video editing or gaming"
    },
    {
        "product_id": "LAP-003",
        "name": "HP 15s (AMD Ryzen 5 5500U / 16GB / 512GB SSD)",
        "category": "laptop",
        "brand": "HP",
        "price_inr": 41990,
        "capacity": "15.6 inch",
        "energy_rating": 4,
        "specs_json": json.dumps({"cpu": "AMD Ryzen 5 5500U 6-Core", "ram": "16GB DDR4", "storage": "512GB SSD", "display": "FHD IPS Micro-Edge", "weight_kg": 1.69, "fast_charge": True, "warranty_years": 1}),
        "key_pros": "16GB RAM out of the box for effortless multitasking; 6-core Ryzen 5 handles programming & Docker",
        "key_cons": "Plastic build; No keyboard backlighting; Moderate speakers"
    },
    {
        "product_id": "LAP-004",
        "name": "ASUS Vivobook 16 (Ryzen 5 7530U / 16GB / 512GB SSD)",
        "category": "laptop",
        "brand": "ASUS",
        "price_inr": 46990,
        "capacity": "16.0 inch",
        "energy_rating": 4,
        "specs_json": json.dumps({"cpu": "AMD Ryzen 5 7530U", "ram": "16GB DDR4", "storage": "512GB SSD", "display": "16-inch WUXGA 16:10", "weight_kg": 1.88, "warranty_years": 1}),
        "key_pros": "Modern 16:10 tall display gives extra vertical lines for coding; 180-degree lay-flat hinge",
        "key_cons": "Display peak brightness nits missing in catalog; No dedicated graphics card"
    },
    {
        "product_id": "LAP-005",
        "name": "Dell Inspiron 14 2-in-1 Touchscreen (Core i5 13th Gen / 16GB / 512GB)",
        "category": "laptop",
        "brand": "Dell",
        "price_inr": 62990,
        "capacity": "14.0 inch",
        "energy_rating": 4,
        "specs_json": json.dumps({"cpu": "Intel Core i5-1335U", "ram": "16GB LPDDR5", "storage": "512GB SSD", "display": "FHD+ Touch IPS 360-hinge", "weight_kg": 1.58, "stylus_support": True, "warranty_years": 1}),
        "key_pros": "Versatile 360-degree convertible hinge for tablet note-taking; Crisp touchscreen; Premium aluminum lid",
        "key_cons": "Glossy screen has reflective glare under sunlight; Heavier than non-touch ultrabooks"
    },
    {
        "product_id": "LAP-006",
        "name": "Acer Nitro V Gaming (Core i5 13th Gen / RTX 4050 / 16GB / 512GB)",
        "category": "laptop",
        "brand": "Acer",
        "price_inr": 69990,
        "capacity": "15.6 inch",
        "energy_rating": 4,
        "specs_json": json.dumps({"cpu": "Intel Core i5-13420H", "ram": "16GB DDR5", "storage": "512GB SSD", "gpu": "NVIDIA RTX 4050 6GB GDDR6", "refresh_rate": "144Hz", "weight_kg": 2.1}),
        "key_pros": "Dedicated RTX 4050 GPU runs AAA games & AI training; 144Hz smooth gaming panel; Fast DDR5 memory",
        "key_cons": "Heavy charging brick; Short 3-4 hr battery life; Catalog lacks stated warranty period"
    },
    {
        "product_id": "LAP-007",
        "name": "Lenovo Legion Slim 5 (Ryzen 7 7840HS / RTX 4060 / 16GB / 1TB)",
        "category": "laptop",
        "brand": "Lenovo",
        "price_inr": 98990,
        "capacity": "16.0 inch",
        "energy_rating": 5,
        "specs_json": json.dumps({"cpu": "AMD Ryzen 7 7840HS", "ram": "16GB DDR5", "storage": "1TB Gen4 SSD", "gpu": "RTX 4060 8GB", "display": "WQXGA 165Hz 100% sRGB", "warranty_years": 1}),
        "key_pros": "High-tier RTX 4060 8GB GPU; Incredible 165Hz color-accurate screen; 1TB fast SSD",
        "key_cons": "Requires 230W power brick; High price point"
    },
    {
        "product_id": "LAP-008",
        "name": "Apple MacBook Air M2 (8GB Unified / 256GB SSD)",
        "category": "laptop",
        "brand": "Apple",
        "price_inr": 84990,
        "capacity": "13.6 inch",
        "energy_rating": 5,
        "specs_json": json.dumps({"cpu": "Apple M2 8-Core CPU / 8-Core GPU", "ram": "8GB Unified", "storage": "256GB SSD", "display": "Liquid Retina", "battery_hours": 18, "weight_kg": 1.24, "warranty_years": 1}),
        "key_pros": "Unrivaled 18-hour battery longevity; Silent fanless unibody design; Superior display & trackpad",
        "key_cons": "Non-upgradable 256GB base storage; High starting cost"
    },

    # ==================== AIR CONDITIONERS ====================
    {
        "product_id": "AC-001",
        "name": "Lloyd 1.5 Ton 3-Star Heavy Duty Window AC",
        "category": "air_conditioner",
        "brand": "Lloyd",
        "price_inr": 26990,
        "capacity": "1.5 Ton",
        "energy_rating": 3,
        "specs_json": json.dumps({"type": "Window AC", "copper_condenser": True, "filter": "Clean Air Filter", "room_size_sqft": "120-150 sq ft", "warranty_years": 1}),
        "key_pros": "No wall drilling or indoor-outdoor pipe routing needed; Sturdy metal chassis; Low purchase cost",
        "key_cons": "Higher operational noise than split ACs; Blocks window daylight; No inverter compressor"
    },
    {
        "product_id": "AC-002",
        "name": "Voltas 1 Ton 3-Star Inverter Split AC",
        "category": "air_conditioner",
        "brand": "Voltas",
        "price_inr": 28490,
        "capacity": "1.0 Ton",
        "energy_rating": 3,
        "specs_json": json.dumps({"type": "Split Inverter", "copper_condenser": True, "stabilizer_free": True, "room_size_sqft": "up to 110 sq ft"}),
        "key_pros": "Affordable entry into split inverter cooling; 100% copper condenser; Good for small study rooms",
        "key_cons": "Only 1 Ton capacity (inadequate for medium/large rooms); Warranty unstated in catalog"
    },
    {
        "product_id": "AC-003",
        "name": "Godrej 1.5 Ton 3-Star Inverter Split AC",
        "category": "air_conditioner",
        "brand": "Godrej",
        "price_inr": 31990,
        "capacity": "1.5 Ton",
        "energy_rating": 3,
        "specs_json": json.dumps({"type": "Split Inverter", "copper_condenser": True, "anti_freeze": True, "warranty_years": 1}),
        "key_pros": "Sub-₹32k price for 1.5 Ton capacity; 100% copper tubes; Active carbon filter",
        "key_cons": "3-star energy efficiency; Average aesthetics"
    },
    {
        "product_id": "AC-004",
        "name": "Daikin 1.5 Ton 3-Star Inverter Split AC",
        "category": "air_conditioner",
        "brand": "Daikin",
        "price_inr": 36990,
        "capacity": "1.5 Ton",
        "energy_rating": 3,
        "specs_json": json.dumps({"type": "Split Inverter", "copper_condenser": True, "pm25_filter": True, "refrigerant": "R32", "room_size_sqft": "111-150 sq ft", "warranty_years": 1}),
        "key_pros": "Cools effectively even at 52C ambient heat; Copper condenser tubes; PM 2.5 air filtration",
        "key_cons": "3-star model consumes roughly 15-20% more power than 5-star inverter equivalents"
    },
    {
        "product_id": "AC-005",
        "name": "Panasonic 1.5 Ton 5-Star Smart Wi-Fi Inverter Split AC",
        "category": "air_conditioner",
        "brand": "Panasonic",
        "price_inr": 43990,
        "capacity": "1.5 Ton",
        "energy_rating": 5,
        "specs_json": json.dumps({"type": "Split Inverter", "copper_condenser": True, "wifi_enabled": True, "ai_mode": True, "room_size_sqft": "120-170 sq ft", "warranty_years": 1}),
        "key_pros": "Maximum 5-star power bill savings; Miraie smart app & Alexa voice control; AI adaptive cooling",
        "key_cons": "Higher initial investment; Requires dependable home Wi-Fi for smart capabilities"
    },
    {
        "product_id": "AC-006",
        "name": "LG 1.5 Ton 5-Star AI DUAL Inverter Split AC",
        "category": "air_conditioner",
        "brand": "LG",
        "price_inr": 46490,
        "capacity": "1.5 Ton",
        "energy_rating": 5,
        "specs_json": json.dumps({"type": "Split Inverter", "copper_condenser": True, "dual_inverter": True, "convertible_modes": 6, "warranty_years": 1}),
        "key_pros": "Dual Inverter compressor runs quieter with lower vibration; 6-in-1 convertible tonnage scaling",
        "key_cons": "Premium price; Outdoor unit is slightly heavy"
    },

    # ==================== MICROWAVES & AIR FRYERS ====================
    {
        "product_id": "MIC-001",
        "name": "LG 20L Solo Microwave Oven",
        "category": "microwave",
        "brand": "LG",
        "price_inr": 5890,
        "capacity": "20L",
        "energy_rating": 3,
        "specs_json": json.dumps({"type": "Solo", "power_wattage": 700, "control": "Mechanical Dials", "warranty_years": 1}),
        "key_pros": "Extremely budget-friendly; Mechanical dial control is intuitive for seniors; Fast reheating",
        "key_cons": "Cannot bake cakes, roast or grill; Small 20L cavity limited to single dinner plates"
    },
    {
        "product_id": "MIC-002",
        "name": "Philips Digital Air Fryer HD9252 (4.1L / Rapid Air Tech)",
        "category": "microwave",
        "brand": "Philips",
        "price_inr": 7490,
        "capacity": "4.1L",
        "energy_rating": 4,
        "specs_json": json.dumps({"type": "Air Fryer", "power_wattage": 1400, "technology": "Rapid Air 360", "digital_touch": True, "warranty_years": 2}),
        "key_pros": "Cuts oil usage by up to 90%; Fast 1400W heating; Dishwasher-safe non-stick basket",
        "key_cons": "4.1L basket accommodates 2-3 portions max; Not intended for reheating liquids/soups"
    },
    {
        "product_id": "MIC-003",
        "name": "IFB 24L Grill Microwave Oven",
        "category": "microwave",
        "brand": "IFB",
        "price_inr": 8790,
        "capacity": "24L",
        "energy_rating": 3,
        "specs_json": json.dumps({"type": "Grill", "power_wattage": 900, "grill_power": 1000, "auto_cook_menus": 65, "warranty_years": 1}),
        "key_pros": "Includes quartz grill heater for crispy kebabs & toasts; 65 pre-programmed Indian cooking menus",
        "key_cons": "Cannot perform convection baking for cakes/breads; Touch membrane panel needs careful handling"
    },
    {
        "product_id": "MIC-004",
        "name": "Samsung 28L Convection Microwave Oven",
        "category": "microwave",
        "brand": "Samsung",
        "price_inr": 12490,
        "capacity": "28L",
        "energy_rating": 4,
        "specs_json": json.dumps({"type": "Convection", "power_wattage": 900, "tandoor_tech": True, "fermentation_curd": True, "warranty_years": 1}),
        "key_pros": "All-in-one baking, grilling, tandoor & curd making; SlimFry technology for low-oil frying",
        "key_cons": "Consumes larger countertop real estate; Metal racks require manual cleaning"
    },
    {
        "product_id": "MIC-005",
        "name": "LG 32L Charcoal Convection Microwave Oven",
        "category": "microwave",
        "brand": "LG",
        "price_inr": 18990,
        "capacity": "32L",
        "energy_rating": 4,
        "specs_json": json.dumps({"type": "Convection", "power_wattage": 1000, "charcoal_heater": True, "rotisserie": True, "warranty_years": 1}),
        "key_pros": "Charcoal Lighting Heater delivers smoky tandoor texture; Motorized 360 rotisserie; 32L massive cavity",
        "key_cons": "Heavy 20kg footprint; Premium price"
    },

    # ==================== SMART TELEVISIONS ====================
    {
        "product_id": "TV-001",
        "name": "Mi 32-inch A Series HD Ready Smart Google TV",
        "category": "television",
        "brand": "Xiaomi",
        "price_inr": 12499,
        "capacity": "32 inch",
        "energy_rating": 3,
        "specs_json": json.dumps({"display_type": "HD Ready LED", "resolution": "1366x768", "refresh_rate": "60Hz", "os": "Google TV", "audio_wattage": 20, "warranty_years": 1}),
        "key_pros": "Affordable smart TV; Built-in Google TV OS with Play Store, Netflix, Prime; Dual 20W speakers",
        "key_cons": "720p HD resolution only (not Full HD); Modest viewing angles in brightly lit rooms"
    },
    {
        "product_id": "TV-002",
        "name": "TCL 43-inch 4K Ultra HD Metallic Bezel-less Smart TV",
        "category": "television",
        "brand": "TCL",
        "price_inr": 23990,
        "capacity": "43 inch",
        "energy_rating": 4,
        "specs_json": json.dumps({"display_type": "4K UHD LED", "resolution": "3840x2160", "hdr": "HDR10", "os": "Google TV", "warranty_years": 1}),
        "key_pros": "Entry-level 4K under ₹25k; Sleek metallic borderless design; Dolby Audio support",
        "key_cons": "60Hz panel; Basic HDR brightness"
    },
    {
        "product_id": "TV-003",
        "name": "LG 43-inch 4K Ultra HD Smart LED TV",
        "category": "television",
        "brand": "LG",
        "price_inr": 31990,
        "capacity": "43 inch",
        "energy_rating": 4,
        "specs_json": json.dumps({"display_type": "4K Ultra HD IPS LED", "resolution": "3840x2160", "refresh_rate": "60Hz", "os": "webOS", "hdr": "HDR10 Pro", "processor": "alpha5 AI Gen6", "warranty_years": 1}),
        "key_pros": "Vibrant 4K IPS panel with wide viewing angles; Magic Remote with point-and-click air mouse",
        "key_cons": "Native 60Hz panel (no 120Hz for PS5 gaming); Basic black level depth in dark rooms"
    },
    {
        "product_id": "TV-004",
        "name": "Samsung 55-inch Crystal 4K iSmart UHD TV",
        "category": "television",
        "brand": "Samsung",
        "price_inr": 42990,
        "capacity": "55 inch",
        "energy_rating": 4,
        "specs_json": json.dumps({"display_type": "Crystal 4K LED", "resolution": "3840x2160", "processor": "Crystal Processor 4K", "os": "Tizen", "warranty_years": 1}),
        "key_pros": "Large 55-inch immersive screen; PurColor technology; OTS Lite 3D surround sound",
        "key_cons": "Tizen OS app selection slightly smaller than Android/Google TV"
    },
    {
        "product_id": "TV-005",
        "name": "Sony Bravia 55-inch 4K Ultra HD Smart Google TV (X74L)",
        "category": "television",
        "brand": "Sony",
        "price_inr": 54990,
        "capacity": "55 inch",
        "energy_rating": 4,
        "specs_json": json.dumps({"display_type": "4K Ultra HD LED", "resolution": "3840x2160", "processor": "X1 4K Processor", "os": "Google TV", "audio": "20W Open Baffle", "warranty_years": 1}),
        "key_pros": "Industry benchmark Sony X1 upscaling engine; Realistic color grading; Immersive Google TV ecosystem",
        "key_cons": "Does not support Dolby Vision (HDR10 only); Premium price over rival budget 55-inch models"
    },
    {
        "product_id": "TV-006",
        "name": "LG 55-inch 4K OLED Cinema TV (B3 Series)",
        "category": "television",
        "brand": "LG",
        "price_inr": 99990,
        "capacity": "55 inch",
        "energy_rating": 5,
        "specs_json": json.dumps({"display_type": "Self-Lit OLED", "resolution": "3840x2160", "refresh_rate": "120Hz", "hdr": "Dolby Vision IQ & Atmos", "hdmi_2_1": True}),
        "key_pros": "Infinite contrast with true self-lighting pixels; 120Hz refresh & HDMI 2.1 for PS5/PC gaming; Dolby Vision",
        "key_cons": "High cost; OLED burn-in risk if static logos displayed continuously for hours; Warranty not in record"
    },

    # ==================== AUDIO & SOUNDBARS ====================
    {
        "product_id": "AUD-001",
        "name": "boAt Airdopes 141 ANC True Wireless Earbuds",
        "category": "audio",
        "brand": "boAt",
        "price_inr": 1499,
        "capacity": "Earbuds",
        "energy_rating": 4,
        "specs_json": json.dumps({"type": "TWS", "anc": "Active Noise Cancellation up to 32dB", "playback_hours": 42, "driver_size": "10mm", "ip_rating": "IPX5", "warranty_years": 1}),
        "key_pros": "Active Noise Cancellation under ₹1,500; Punchy bass for casual listening; Total 42hr battery",
        "key_cons": "Plastic case feel; Microphone quality dips in windy outdoor traffic"
    },
    {
        "product_id": "AUD-002",
        "name": "OnePlus Buds Pro 2 (Dual Drivers / 48dB ANC / Spatial Audio)",
        "category": "audio",
        "brand": "OnePlus",
        "price_inr": 8990,
        "capacity": "Earbuds",
        "energy_rating": 5,
        "specs_json": json.dumps({"type": "TWS", "anc": "Adaptive 48dB ANC", "drivers": "11mm woofer + 6mm tweeter", "battery_hours": 39, "lhdc": True, "warranty_years": 1}),
        "key_pros": "MelodyBoost dual driver sound tuned by Dynaudio; Hi-Res LHDC codec; Spatial audio head tracking",
        "key_cons": "Full feature customization requires OnePlus smartphone"
    },
    {
        "product_id": "AUD-003",
        "name": "JBL Cinema SB271 2.1 Channel Soundbar with Wireless Subwoofer",
        "category": "audio",
        "brand": "JBL",
        "price_inr": 11990,
        "capacity": "Soundbar",
        "energy_rating": 4,
        "specs_json": json.dumps({"type": "Soundbar 2.1 Ch", "power_output_watts": 220, "subwoofer": "Wireless Subwoofer", "connectivity": "HDMI ARC, Bluetooth, Optical", "warranty_years": 1}),
        "key_pros": "220W maximum system power gives punchy cinema bass; Wireless subwoofer frees up cabling; HDMI ARC",
        "key_cons": "No dedicated center speaker for isolated voice dialogue enhancement; Lacks Dolby Atmos"
    },
    {
        "product_id": "AUD-004",
        "name": "Sony WH-1000XM5 Wireless Active Noise Canceling Headphones",
        "category": "audio",
        "brand": "Sony",
        "price_inr": 26990,
        "capacity": "Over-Ear",
        "energy_rating": 5,
        "specs_json": json.dumps({"type": "Over-Ear Wireless", "anc": "Dual Processor V1 + HD QN1", "battery_hours": 30, "codecs": "LDAC, AAC, SBC", "weight_g": 250, "warranty_years": 1}),
        "key_pros": "Class-leading Active Noise Cancellation shuts out airplane & cafe noise; Hi-Res LDAC audio; 30hr battery",
        "key_cons": "Earcups do not fold inward into compact ball; Premium pricing"
    },

    # ==================== SMART HOME & CLEANING ====================
    {
        "product_id": "SMR-001",
        "name": "Mi Smart Air Purifier 4 (HEPA Filter / Wi-Fi App)",
        "category": "smart_home",
        "brand": "Xiaomi",
        "price_inr": 14999,
        "capacity": "Room Purifier",
        "energy_rating": 4,
        "specs_json": json.dumps({"type": "Air Purifier", "coverage_sqft": 516, "cadr_m3h": 400, "filter": "True HEPA H13", "pm25_laser_sensor": True, "warranty_years": 1}),
        "key_pros": "Filters 99.97% particles down to 0.3 microns; High 400 CADR covers living rooms; App air quality report",
        "key_cons": "HEPA replacement filters cost approx ₹2,500 every 6-12 months"
    },
    {
        "product_id": "SMR-002",
        "name": "Ecovacs Deebot Y1 Pro 2-in-1 Robot Vacuum Cleaner & Mop",
        "category": "smart_home",
        "brand": "Ecovacs",
        "price_inr": 24900,
        "capacity": "Robot Vacuum",
        "energy_rating": 4,
        "specs_json": json.dumps({"type": "Robot Vacuum & Mop", "suction_pa": 6500, "navigation": "LDS LiDAR LDS 360", "battery_mah": 5200, "warranty_years": 1}),
        "key_pros": "Simultaneous vacuuming and wet mopping; Precision LiDAR navigation maps multi-story homes; Strong suction",
        "key_cons": "Requires cleaning hair tangled on roller brush weekly; Struggles with thick door mats"
    },
    {
        "product_id": "SMR-003",
        "name": "Dyson V8 Absolute Cordless Stick Vacuum Cleaner",
        "category": "smart_home",
        "brand": "Dyson",
        "price_inr": 32900,
        "capacity": "Stick Vacuum",
        "energy_rating": 5,
        "specs_json": json.dumps({"type": "Cordless Stick Vacuum", "motor": "Dyson Digital Motor V8", "battery_mins": 40, "filtration": "Whole-machine filtration", "weight_kg": 2.6}),
        "key_pros": "Cordless maneuverability cleans ceilings, car seats and sofas easily; Fluffy head protects wooden floors",
        "key_cons": "Maximum boost mode lasts only ~7 minutes; Missing official catalog warranty duration"
    }
]

def generate_clean_catalog():
    fields = ['product_id', 'name', 'category', 'brand', 'price_inr', 'capacity', 'energy_rating', 'specs_json', 'key_pros', 'key_cons']
    with open('data/products.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for p in PRODUCTS:
            writer.writerow(p)
    print(f"Successfully generated clean, authentic catalog with {len(PRODUCTS)} real appliances in data/products.csv")

if __name__ == "__main__":
    generate_clean_catalog()
