"""
Swift Sign Group - Comprehensive Multi-Subsidiary Knowledge Base
Contains complete corporate, division, contact, and location details
for all Swift Sign Group subsidiaries and operations.
"""

from typing import Optional, Dict

COMPANY_DATA: Dict[str, str] = {
    "corporate_info": """
Swift Sign Group of Companies (Corporate Overview):
- Overview: Swift Sign Group is a premier multi-disciplinary enterprise operating across Pakistan, the UAE, and international markets.
- Major Subsidiaries & Divisions:
  1. Swift Sign IT & Cyber Solutions
  2. Swift Sign Business Management & Setup
  3. Swift Sign Shipping LLC & General Trading
  4. Laila Hijab (Fashion & Modest Apparel)
  5. Swift Sign Organic Food Division
- Corporate Head Office (Pakistan): Office 22, 4th Floor, Pakland City Center, I-8 Markaz, Islamabad, Pakistan.
- International / Regional Operations (UAE): Dubai, United Arab Emirates (GCC Hub).
- General Inquiries Email: info@swiftsignbm.com
- Central Contact Numbers: +92 334 8399480 / +92 315 8399446
- Global Footprint: Pakistan, UAE, GCC countries (KSA, Qatar, Kuwait, Bahrain, Oman), Europe, Asia, and the Americas.
""",

    "it_cyber": """
Swift Sign IT & Cyber Solutions:
- Office Location: Office 22, 4th Floor, Pakland City Center, I-8 Markaz, Islamabad, Pakistan.
- Digital & Software Engineering Services:
  * Custom Software Development (Enterprise solutions, ERP, CRM, portal development)
  * Cyber Security Audits & Vulnerability Assessments, Network Security, Risk Mitigation
  * Web Application Development (Full-stack modern web apps)
  * Mobile App Development (iOS & Android native and hybrid applications)
  * UI/UX Design, Wireframing & Prototyping
  * IT Infrastructure Consultancy & Cloud Solutions
  * Digital Marketing, SEO, Social Media Management
  * Graphic Design, Branding & Professional Video Editing
- Physical Security & Hardware Solutions:
  * CCTV Surveillance System Installation & Maintenance
  * Biometric Attendance Systems & Facial Recognition Devices
  * RFID Access Control Systems & Smart Locks
  * Security Alarm & Intrusion Detection Systems
  * Parking Barrier Systems & Automatic Boom Gates
  * Enterprise Networking, Structured Cabling & Server Rack Setup
- Direct Contact: info@it.swiftsignbm.com | Phone / WhatsApp: +92 315 8399446 / +92 334 8399480.
""",

    "business_mgmt": """
Swift Sign Business Management & Setup:
- Regional Focus: United Arab Emirates (Dubai, Abu Dhabi, Sharjah), GCC, and International Markets.
- Core Services:
  * UAE Company Formation & Business Setup (Mainland, Free Zones, and Offshore company registration)
  * Commercial, Professional & Industrial Licensing Assistance
  * Government PRO Services, Visa Processing & Corporate Documentation
  * Regulatory Compliance & Corporate Risk Advisory
  * Financial Advisory, Accounting & Bookkeeping
  * Corporate Bank Account Opening Assistance
  * Tax Consulting & VAT Registration / Filings in the UAE
- Mission: Providing end-to-end consulting for startups, SMEs, and foreign investors expanding into the UAE and GCC.
- Direct Contact: info@swiftsignbm.com | Phone / WhatsApp: +92 334 8399480.
""",

    "shipping_trading": """
Swift Sign Shipping LLC & General Trading:
- Regional Hub: Dubai, United Arab Emirates with extensive GCC and worldwide network.
- Logistics & Freight Forwarding Services:
  * Ocean / Sea Freight (FCL - Full Container Load & LCL - Less than Container Load)
  * Air Freight Cargo (Express and standard international air shipments)
  * Land Freight & Cross-Border Transportation across GCC (UAE, Saudi Arabia/KSA, Qatar, Kuwait, Bahrain, Oman)
  * Door-to-Door Cargo Delivery & Express Logistics
  * Customs Clearance & Brokerage Services
  * Warehousing, Inventory Storage & Supply Chain Management
  * Project Cargo & Heavy Lift Cargo Handling
- General Trading & Industrial Packaging:
  * Premium High-Quality Wooden Pallets (Manufacturing, Supply & Custom Sizes)
  * Heat-Treated Pallets (ISPM-15 export compliant for international shipping)
  * Custom Industrial Pallet Designs & Heavy-duty Skids
  * Industrial Packaging Solutions, Shrink Wrapping, and Cargo Securing Materials
- Global Reach: Europe, North America, Asia-Pacific, GCC, and Middle East.
- Direct Contact: info@swiftsigngeneraltrading.com | Phone / WhatsApp: +92 334 8399480.
""",

    "laila_hijab": """
Laila Hijab (Fashion & Modest Apparel Division):
- Brand Identity: Swift Sign Group's dedicated modern and modest women's fashion brand.
- Product Offerings:
  * Premium Hijab Collections (Chiffon, Silk, Cotton, Jersey, Georgette, Modal)
  * Designer Abayas & Modest Outerwear
  * Fashion Scarves, Stoles, and Shawls
  * Modest Dresses, Co-ord Sets, and Everyday Essentials
  * Accessories: Hijab Pins, Undercaps, Scrunchies, and Styling Magnets
- Key Highlights: Exceptional fabric quality, elegant craftsmanship, contemporary modest fashion, and worldwide online retail shipping.
""",

    "organic_food": """
Swift Sign Organic Food Division:
- Division Identity: Swift Sign Group's health and wellness consumer products division.
- Core Offerings:
  * 100% Pure & Raw Natural Honey (Sidr Honey, Acacia Honey, Multi-Flora Honey)
  * Premium Grade Dried Fruits & Nuts (Almonds, Walnuts, Pistachios, Figs, Pine Nuts)
  * Organic Health Staples, Grains, and Superfoods
  * Natural Cold-Pressed Edible Oils
- Quality Commitment: Directly sourced from certified organic farms, unadulterated, zero chemical preservatives, zero artificial additives, rigorously quality-tested and hygienically packaged.
"""
}

# Brand alias mapping for flexible brand-specific context resolution
BRAND_ALIASES: Dict[str, str] = {
    "it": "it_cyber",
    "it_cyber": "it_cyber",
    "cyber": "it_cyber",
    "software": "it_cyber",
    "tech": "it_cyber",
    "cctv": "it_cyber",
    "business": "business_mgmt",
    "business_mgmt": "business_mgmt",
    "setup": "business_mgmt",
    "uae": "business_mgmt",
    "company_formation": "business_mgmt",
    "shipping": "shipping_trading",
    "shipping_trading": "shipping_trading",
    "freight": "shipping_trading",
    "trading": "shipping_trading",
    "logistics": "shipping_trading",
    "pallets": "shipping_trading",
    "laila": "laila_hijab",
    "laila_hijab": "laila_hijab",
    "hijab": "laila_hijab",
    "fashion": "laila_hijab",
    "apparel": "laila_hijab",
    "food": "organic_food",
    "organic": "organic_food",
    "organic_food": "organic_food",
    "honey": "organic_food",
    "dry_fruits": "organic_food",
    "corporate": "corporate_info",
    "corporate_info": "corporate_info",
    "headquarters": "corporate_info",
    "group": "corporate_info",
    "all": "corporate_info"
}

def get_unified_knowledge() -> str:
    """Builds the comprehensive multi-division knowledge string."""
    sections = []
    for key, text in COMPANY_DATA.items():
        title = key.replace("_", " ").upper()
        sections.append(f"=== {title} ===\n{text.strip()}")
    return "\n\n".join(sections)

def get_company_context(brand: Optional[str] = None) -> str:
    """
    Returns full company context. If a brand is specified, ensures that division's
    focus is highlighted while retaining complete company knowledge.
    """
    full_kb = get_unified_knowledge()
    if not brand:
        return full_kb
    
    canonical_key = BRAND_ALIASES.get(brand.strip().lower())
    if canonical_key and canonical_key in COMPANY_DATA:
        preferred = COMPANY_DATA[canonical_key].strip()
        return f"[PRIMARY FOCUS DIVISION: {canonical_key.upper()}]\n{preferred}\n\n[FULL GROUP CONTEXT]\n{full_kb}"
    
    return full_kb

# Primary full knowledge string export
KNOWLEDGE_BASE = get_unified_knowledge()