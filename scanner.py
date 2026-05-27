"""
ToolBreakdown Smarter Scanner
Generates unique, high-value keywords with smart dedup.
"""

import json
import os
from datetime import datetime

PROJECT_ROOT = os.path.expanduser("~/projects/toolbreakdown")
QUEUE_FILE = os.path.join(PROJECT_ROOT, "data", "content-queue.json")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

NICHES = {
    "ai-writing": {
        "name": "AI Writing Tools",
        "tools": ["Jasper", "Copy.ai", "Writesonic", "Rytr", "Anyword", "Sudowrite", "Wordtune", "Quillbot"],
        "scenarios": ["blog writing", "email marketing", "social media", "SEO content", "ad copy", "e-commerce"],
    },
    "project-management": {
        "name": "Project Management",
        "tools": ["Asana", "Monday.com", "ClickUp", "Notion", "Jira", "Linear", "Wrike", "Basecamp"],
        "scenarios": ["remote teams", "agile", "marketing", "freelancers", "enterprise", "startups"],
    },
    "email-marketing": {
        "name": "Email Marketing",
        "tools": ["Mailchimp", "ConvertKit", "Beehiiv", "ActiveCampaign", "MailerLite", "Klaviyo", "Drip", "Substack"],
        "scenarios": ["e-commerce", "newsletters", "automation", "small business", "creators", "B2B"],
    },
    "vpn": {
        "name": "VPN Services",
        "tools": ["NordVPN", "ExpressVPN", "Surfshark", "ProtonVPN", "CyberGhost", "Mullvad", "IPVanish", "PIA"],
        "scenarios": ["streaming", "gaming", "torrenting", "privacy", "travel", "budget"],
    },
    "website-builders": {
        "name": "Website Builders",
        "tools": ["Wix", "Squarespace", "Webflow", "Shopify", "Framer", "Carrd", "WordPress", "Duda"],
        "scenarios": ["e-commerce", "portfolio", "blogging", "small business", "SEO", "designers"],
    },
    "hosting": {
        "name": "Web Hosting",
        "tools": ["SiteGround", "Cloudways", "Kinsta", "WP Engine", "Hostinger", "DigitalOcean", "Vercel", "Netlify"],
        "scenarios": ["WordPress", "e-commerce", "budget", "managed", "developers", "high traffic"],
    },
}


def generate_keywords():
    """Generate deduplicated keywords."""
    seen = set()
    items = []
    
    for niche_slug, niche_data in NICHES.items():
        tools = niche_data["tools"]
        name = niche_data["name"]
        scenarios = niche_data["scenarios"]
        
        # 1. VS pairs (ensure each pair is unique regardless of order)
        for i, t1 in enumerate(tools):
            for t2 in tools[i+1:]:
                pair = tuple(sorted([t1.lower(), t2.lower()]))
                if pair not in seen:
                    seen.add(pair)
                    keyword = f"{t1} vs {t2}"
                    items.append({
                        "keyword": keyword,
                        "niche": niche_slug,
                        "type": "vs",
                        "tools": [t1, t2],
                        "volume_tier": "medium" if len(tools) > 7 else "low",
                        "priority": 40,
                    })
        
        # 2. Best-of per scenario (one per scenario, not one per tool)
        for scenario in scenarios:
            kw = f"best {name.lower()} for {scenario}"
            kw_key = kw.lower().strip()
            if kw_key not in seen:
                seen.add(kw_key)
                items.append({
                    "keyword": kw,
                    "niche": niche_slug,
                    "type": "best",
                    "tools": [],
                    "volume_tier": "medium",
                    "priority": 25,
                })
        
        # 3. General best-of (one per niche)
        kw = f"best {name.lower()} 2026"
        if kw.lower() not in seen:
            seen.add(kw.lower())
            items.append({
                "keyword": kw,
                "niche": niche_slug,
                "type": "best",
                "tools": [],
                "volume_tier": "high",
                "priority": 30,
            })
        
        # 4. Alternatives (only for top 4 tools per niche)
        for tool in tools[:4]:
            kw = f"{tool} alternatives"
            if kw.lower() not in seen:
                seen.add(kw.lower())
                items.append({
                    "keyword": kw,
                    "niche": niche_slug,
                    "type": "alternative",
                    "tools": [tool],
                    "volume_tier": "medium",
                    "priority": 20,
                })
    
    # Sort by priority
    items.sort(key=lambda x: (-x["priority"], x["keyword"]))
    
    # Assign IDs
    for i, item in enumerate(items):
        item["id"] = i + 1
        item["status"] = "pending"
        item["created_at"] = datetime.utcnow().isoformat()
    
    # Save
    queue = {
        "generated_at": datetime.utcnow().isoformat(),
        "total": len(items),
        "items": items,
    }
    
    with open(QUEUE_FILE, "w") as f:
        json.dump(queue, f, indent=2)
    
    # Summary
    print(f"Generated {len(items)} unique keywords")
    by_type = {}
    by_niche = {}
    for item in items:
        by_type[item["type"]] = by_type.get(item["type"], 0) + 1
        by_niche[item["niche"]] = by_niche.get(item["niche"], 0) + 1
    
    print("\nBy type:")
    for t, c in sorted(by_type.items()):
        print(f"  {t}: {c}")
    
    print("\nBy niche:")
    for n, c in sorted(by_niche.items()):
        print(f"  {NICHES[n]['name']}: {c}")
    
    print(f"\nTop 10:")
    for item in items[:10]:
        print(f"  #{item['id']} [{item['type']}] {item['keyword']} ({item['niche']})")
    
    return items


if __name__ == "__main__":
    generate_keywords()
