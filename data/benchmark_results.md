# ElectraMatch Milestone 2: Evaluation Benchmark Table (12 Test Inputs)

- **Total Test Inputs**: 12
- **Baseline Prompt Compliance (CCR)**: 66.7%
- **ElectraMatch Grounded Pipeline Compliance (CCR)**: 100.0%

| Test ID | Test Type | User Query | Budget | Expected Output | Actual Output | Pipeline Status | Baseline Status |
| :---: | :--- | :--- | :---: | :--- | :--- | :---: | :---: |
| **Q-01** | Standard Functional | Recommend a refrigerator under ₹25,000 for a small family of three. Prefer double door frost-free if possible. | ₹25,000 | Samsung 236L 3-Star Digital Inverter Double Door (₹24,990) | Samsung 236L 3-Star Digital Inverter Double Door Refrigerator (₹24,990) | **PASS** | FAIL |
| **Q-02** | Standard Functional | I am a college student needing a lightweight laptop under ₹40,000 for programming, assignments and watching lectures. | ₹40,000 | Lenovo IdeaPad Slim 3 (Core i3 / 8GB / 512GB SSD) (₹34,990) | Lenovo IdeaPad Slim 3 (Core i3 12th Gen / 8GB / 512GB SSD) (₹34,990) | **PASS** | PASS |
| **Q-03** | Standard Functional | Looking for a 1.5 Ton AC for a master bedroom under ₹38,000 with copper condenser and inverter compressor. | ₹38,000 | Daikin 1.5 Ton 3-Star Inverter Split AC (₹36,990) | Daikin 1.5 Ton 3-Star Inverter Split AC (₹36,990) | **PASS** | PASS |
| **Q-04** | Standard Functional | Need a fully automatic washing machine with minimum 7kg capacity under ₹20,000. | ₹20,000 | LG 7 Kg 5-Star Smart Inverter Top Load (₹18,990) | LG 7 Kg 5-Star Smart Inverter Fully Automatic Top Load (₹18,990) | **PASS** | FAIL |
| **Q-05** | Standard Functional | I want a microwave that can bake cakes, make pizza, and grill chicken under ₹15,000. | ₹15,000 | Samsung 28L Convection Microwave Oven (₹12,490) | Samsung 28L Convection Microwave Oven (₹12,490) | **PASS** | FAIL |
| **Q-06** | Standard Functional | Suggest a 4K smart TV under ₹35,000 for living room movie streaming with good viewing angles. | ₹35,000 | LG 43-inch 4K Ultra HD Smart LED TV (₹31,990) | LG 43-inch 4K Ultra HD Smart LED TV (₹31,990) | **PASS** | PASS |
| **Q-07** | Standard Functional | I want premium noise canceling wireless headphones under ₹30,000 for flight travel and office focus. | ₹30,000 | Sony WH-1000XM5 Wireless ANC Headphones (₹26,990) | Sony WH-1000XM5 Wireless Active Noise Canceling Headphones (₹26,990) | **PASS** | PASS |
| **Q-08** | Standard Functional | Looking for a smart robot vacuum cleaner and mop under ₹26,000 with LiDAR navigation. | ₹26,000 | Ecovacs Deebot Y1 Pro 2-in-1 Robot Vacuum & Mop (₹24,900) | Ecovacs Deebot Y1 Pro 2-in-1 Robot Vacuum Cleaner & Mop (₹24,900) | **PASS** | PASS |
| **Q-09** | Edge Case: Impossible / Under-Budget | Looking for an inverter double door frost-free refrigerator under ₹5,000. | ₹5,000 | Fallback Notification / Closest Alternative with Budget Warning | Relaxation Alert: Closest alternative No match / Out-of-bounds warning (N/A) | **PASS** | FAIL |
| **Q-10** | Edge Case: Contradictory / Unrealistic Constraints | Need a high-end dedicated GPU gaming laptop with RTX graphics and 18-hour battery life under ₹30,000. | ₹30,000 | Acer Aspire Lite (₹24,990) or Budget Warning | Acer Aspire Lite (AMD Athlon Silver / 8GB / 256GB SSD) (₹24,990) | **PASS** | PASS |
| **Q-11** | Edge Case: Ultra-Premium Budget Upper-Bound | I want the best 55-inch OLED TV with 120Hz refresh rate and HDMI 2.1 for PS5 gaming with an unlimited budget of ₹1,20,000. | ₹120,000 | LG 55-inch 4K OLED Cinema TV (₹99,990) | LG 55-inch 4K OLED Cinema TV (B3 Series) (₹99,990) | **PASS** | PASS |
| **Q-12** | Edge Case: Missing / Unspecified Budget with Strict Feature Requirements | Recommend a quiet front load washing machine with steam wash and allergen care for sensitive skin. | Unbounded | LG 7 Kg 5-Star Inverter Direct Drive Front Load (₹28,990) | IFB 8 Kg 5-Star AI Powered Front Load Washing Machine (₹36,990) | **PASS** | PASS |
