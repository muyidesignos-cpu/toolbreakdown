"""
ToolBreakdown Keyword Scanner
Multi-niche keyword discovery for SaaS comparison content.

Strategy:
1. From seed tools, generate comparison keywords (X vs Y, X alternatives)
2. Expand with scenario-based long-tails (best X for Y)
3. Filter by estimated search volume & competition
4. Output prioritized queue for the content engine
"""

import json
import os
import urllib.request
import urllib.parse
from datetime import datetime

PROJECT_ROOT = os.path.expanduser("~/projects/toolbreakdown")
QUEUE_FILE = os.path.join(PROJECT_ROOT, "data", "content-queue.json")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ── Seed tools per niche ────────────────────────────────────────
NICHES = {
    "ai-writing": {
        "name": "AI Writing Tools",
        "tools": ["Jasper", "Copy.ai", "Writesonic", "Rytr", "Anyword", "Sudowrite", "Wordtune", "Quillbot", "Grammarly", "SurferSEO"],
        "scenarios": ["blog writing", "email copy", "social media captions", "seo content", "ad copy", "e-commerce product descriptions", "academic writing", "creative writing"],
    },
    "project-management": {
        "name": "Project Management",
        "tools": ["Asana", "Monday.com", "ClickUp", "Notion", "Linear", "Jira", "Basecamp", "Wrike", "Trello", "Airtable"],
        "scenarios": ["remote teams", "agile development", "marketing teams", "freelancers", "enterprise", "small business", "startups"],
    },
    "email-marketing": {
        "name": "Email Marketing",
        "tools": ["Mailchimp", "ConvertKit", "Beehiiv", "ActiveCampaign", "MailerLite", "Drip", "Klaviyo", "SendGrid", "Constant Contact", "Substack"],
        "scenarios": ["e-commerce", "newsletters", "automation", "small business", "creators", "B2B"],
    },
    "vpn": {
        "name": "VPN Services",
        "tools": ["NordVPN", "ExpressVPN", "Surfshark", "ProtonVPN", "CyberGhost", "PIA", "Windscribe", "Mullvad", "IPVanish", "Atlas VPN"],
        "scenarios": ["streaming", "gaming", "torrenting", "privacy", "China", "travel", "budget"],
    },
    "website-builders": {
        "name": "Website Builders",
        "tools": ["Wix", "Squarespace", "Webflow", "Shopify", "WordPress", "Framer", "Carrd", "Ghost", "Weebly", "Duda"],
        "scenarios": ["e-commerce", "portfolio", "blogging", "small business", "SEO", "designers"],
    },
    "hosting": {
        "name": "Web Hosting",
        "tools": ["SiteGround", "Bluehost", "Cloudways", "Kinsta", "WP Engine", "Hostinger", "GreenGeeks", "DreamHost", "DigitalOcean", "Vercel"],
        "scenarios": ["WordPress", "e-commerce", "budget", "managed hosting", "developers", "high traffic"],
    },
}


def generate_keywords_for_niche(niche_slug, niche_data):
    """Generate all keyword variants for a niche."""
    tools = niche_data["tools"]
    scenarios = niche_data["scenarios"]
    keywords = []
    
    # 1. Best-of keywords (highest value)
    for scenario in scenarios:
        keywords.append(f"best {niche_data['name'].lower() if niche_slug != 'ai-writing' else 'ai writing tools'} for {scenario}")
        keywords.append(f"best {niche_data['name'].lower() if niche_slug != 'ai-writing' else 'ai writing tools'} for {scenario} 2026")
    
    # Also general "best X" for each niche
    keywords.append(f"best {niche_data['name'].lower() if niche_slug != 'ai-writing' else 'ai writing tools'} 2026")
    keywords.append(f"top {niche_data['name'].lower() if niche_slug != 'ai-writing' else 'ai writing tools'}")
    
    # 2. VS keywords (high intent: user is ready to buy, just choosing)
    for i, t1 in enumerate(tools):
        for t2 in tools[i+1:]:
            # Only generate for top 8 tools per niche to keep count reasonable
            if tools.index(t1) < 8 and tools.index(t2) < 8:
                keywords.append(f"{t1} vs {t2}")
                keywords.append(f"{t1} vs {t2} comparison")
    
    # 3. Alternative keywords
    for tool in tools[:8]:
        keywords.append(f"{tool} alternatives")
        keywords.append(f"{tool} competitors")
    
    # 4. Cheap/budget variants
    keywords.append(f"cheap {niche_data['name'].lower() if niche_slug != 'ai-writing' else 'ai writing tools'}")
    keywords.append(f"free {niche_data['name'].lower() if niche_slug != 'ai-writing' else 'ai writing tools'}")
    
    return keywords


def deduplicate_keywords(all_keywords):
    """Remove duplicates and near-duplicates."""
    seen = set()
    unique = []
    for kw in all_keywords:
        kw_lower = kw.lower().strip()
        if kw_lower not in seen:
            seen.add(kw_lower)
            unique.append(kw)
    return unique


def estimate_volume_tier(keyword):
    """Quick heuristic: longer tail = lower volume tier."""
    words = keyword.split()
    if len(words) <= 3:
        return "high"       # e.g., "Jasper vs Copy.ai"
    elif len(words) <= 6:
        return "medium"     # e.g., "best ai writing tools for blog"
    else:
        return "low"        # e.g., "best ai writing tools for e-commerce product descriptions"


def classify_article_type(keyword):
    """Determine the article type based on keyword pattern."""
    kw = keyword.lower()
    if " vs " in kw:
        return "vs"
    if "alternative" in kw or "competitor" in kw or "like " in kw:
        return "alternative"
    if any(kw.startswith(p) for p in ["best ", "top ", "cheap ", "free ", "affordable "]):
        return "best"
    return "blog"


def extract_tools(keyword, niche_data):
    """Extract which tools are mentioned in the keyword."""
    tools_found = []
    for tool in niche_data["tools"]:
        if tool.lower() in keyword.lower():
            tools_found.append(tool)
    return tools_found


def build_queue():
    """Main function: generate the content queue."""
    all_keywords = []
    
    for niche_slug, niche_data in NICHES.items():
        niche_kw = generate_keywords_for_niche(niche_slug, niche_data)
        all_keywords.extend(niche_kw)
        print(f"[{niche_slug}] Generated {len(niche_kw)} keywords")
    
    all_keywords = deduplicate_keywords(all_keywords)
    print(f"\nTotal unique keywords: {len(all_keywords)}")
    
    # Build queue items
    queue = []
    for i, kw in enumerate(all_keywords):
        # Find which niche this belongs to
        niche_match = None
        for ns, nd in NICHES.items():
            for tool in nd["tools"]:
                if tool.lower() in kw.lower():
                    niche_match = ns
                    break
            if niche_match:
                break
        
        if not niche_match:
            # Try matching by name
            for ns, nd in NICHES.items():
                if nd["name"].lower() in kw.lower() or ns.replace("-", " ") in kw.lower():
                    niche_match = ns
                    break
        
        if not niche_match:
            niche_match = list(NICHES.keys())[0]  # default fallback
        
        article_type = classify_article_type(kw)
        volume_tier = estimate_volume_tier(kw)
        tools = extract_tools(kw, NICHES[niche_match]) if niche_match in NICHES else []
        
        # Priority scoring
        priority = 0
        if article_type == "vs":
            priority += 30       # VS articles = highest conversion intent
        elif article_type == "best":
            priority += 20       # Best-of = high volume, good conversion
        elif article_type == "alternative":
            priority += 15       # Alternative = medium intent
        
        if volume_tier == "high":
            priority += 10
        elif volume_tier == "medium":
            priority += 5
        
        if len(tools) >= 2:
            priority += 5        # Multiple tools mentioned = richer comparison
        
        queue.append({
            "id": i + 1,
            "keyword": kw,
            "niche": niche_match,
            "type": article_type,
            "tools": tools,
            "volume_tier": volume_tier,
            "priority": priority,
            "status": "pending",
            "created_at": datetime.utcnow().isoformat(),
        })
    
    # Sort by priority descending
    queue.sort(key=lambda x: x["priority"], reverse=True)
    
    # Re-id after sort
    for i, item in enumerate(queue):
        item["id"] = i + 1
    
    # Write queue
    with open(QUEUE_FILE, "w") as f:
        json.dump({"generated_at": datetime.utcnow().isoformat(), "total": len(queue), "items": queue}, f, indent=2)
    
    print(f"\nQueue written to {QUEUE_FILE}")
    
    # Print summary
    print("\n=== QUEUE SUMMARY ===")
    print(f"Total items: {len(queue)}")
    by_type = {}
    by_niche = {}
    for item in queue:
        by_type[item["type"]] = by_type.get(item["type"], 0) + 1
        by_niche[item["niche"]] = by_niche.get(item["niche"], 0) + 1
    
    print("\nBy type:")
    for t, c in sorted(by_type.items(), key=lambda x: x[1], reverse=True):
        print(f"  {t}: {c}")
    
    print("\nBy niche:")
    for n, c in sorted(by_niche.items(), key=lambda x: x[1], reverse=True):
        print(f"  {NICHES[n]['name']}: {c}")
    
    # Top 10
    print("\n=== TOP 10 PRIORITY ===")
    for item in queue[:10]:
        print(f"  #{item['id']} [{item['priority']}] {item['keyword']} ({item['type']}, {item['niche']})")


if __name__ == "__main__":
    build_queue()
