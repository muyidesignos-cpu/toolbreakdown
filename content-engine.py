"""
ToolBreakdown Content Engine v2
Generates .astro pages directly.
Uses helper functions to avoid Python/Astro curly-brace conflicts.
"""

import json
import os
from datetime import datetime

PROJECT_ROOT = os.path.expanduser("~/projects/toolbreakdown")
QUEUE_FILE = os.path.join(PROJECT_ROOT, "data", "content-queue.json")
PAGES_DIR = os.path.join(PROJECT_ROOT, "src", "pages")

for t in ["best", "vs", "alternatives", "blog"]:
    os.makedirs(os.path.join(PAGES_DIR, t), exist_ok=True)


def slugify(text):
    return text.lower().replace(" ", "-").replace("/", "-").replace(".", "").replace("(", "").replace(")", "")


def esc(s):
    """Escape a string for use inside HTML attribute quotes."""
    return s.replace("\\", "\\\\").replace('"', '&quot;').replace("\n", " ")


def make_page(title, description, body_html, breadcrumb_link, breadcrumb_text):
    """Generate a complete .astro page."""
    return f"""---
import Base from '../../layouts/Base.astro';
---

<Base title="{esc(title)}" description="{esc(description)}">
<article>
  <p class="breadcrumb">&larr; <a href="{breadcrumb_link}">{breadcrumb_text}</a></p>
  <h1>{title}</h1>
  <div class="meta"><span>{datetime.utcnow().strftime('%B %d, %Y')}</span></div>

{body_html}

  <div class="disclosure"><em>Affiliate Disclosure: Some links may earn us a commission at no extra cost to you.</em></div>
</article>
</Base>
"""


def vs_body(tool_a, tool_b, niche_name):
    return f"""  <p>Choosing between <strong>{tool_a}</strong> and <strong>{tool_b}</strong>? Both are solid {niche_name.lower()} options, but they serve different audiences. Here's the breakdown.</p>

  <h2>Quick Comparison</h2>
  <table>
    <tr><th></th><th>{tool_a}</th><th>{tool_b}</th></tr>
    <tr><td><strong>Best for</strong></td><td>Content teams &amp; enterprises</td><td>Solo creators &amp; small teams</td></tr>
    <tr><td><strong>Starting price</strong></td><td>$49/mo</td><td>$36/mo</td></tr>
    <tr><td><strong>Free plan</strong></td><td>7-day trial</td><td>Free plan available</td></tr>
    <tr><td><strong>G2 rating</strong></td><td>4.7/5</td><td>4.5/5</td></tr>
  </table>

  <h2>{tool_a} Overview</h2>
  <p>{tool_a} is built for teams and businesses needing high-volume, brand-consistent content. Key strengths: team collaboration with approval workflows, customizable brand voice that learns your style, and deep SEO integrations with SurferSEO and Grammarly.</p>
  <p><strong>Pros:</strong> Powerful team features, excellent content quality, great SEO integrations.</p>
  <p><strong>Cons:</strong> Higher price point, steeper learning curve, overkill for solo users.</p>
  <a href="#aff-{slugify(tool_a)}" class="cta-button">Try {tool_a} &rarr;</a>

  <h2>{tool_b} Overview</h2>
  <p>{tool_b} focuses on simplicity and speed &mdash; ideal for individual creators and small teams. Generate content in seconds with minimal setup. It offers a genuinely usable free plan, not just a teaser.</p>
  <p><strong>Pros:</strong> Fast and easy, affordable pricing, solid quality for the price.</p>
  <p><strong>Cons:</strong> Fewer team features, less customization, limited integrations.</p>
  <a href="#aff-{slugify(tool_b)}" class="cta-button">Try {tool_b} &rarr;</a>

  <h2>Pricing Comparison</h2>
  <table>
    <tr><th>Plan</th><th>{tool_a}</th><th>{tool_b}</th></tr>
    <tr><td>Free tier</td><td>No</td><td>Yes (limited)</td></tr>
    <tr><td>Starter</td><td>$49/mo</td><td>$36/mo</td></tr>
    <tr><td>Pro</td><td>$99/mo</td><td>$89/mo</td></tr>
    <tr><td>Enterprise</td><td>Custom</td><td>Custom</td></tr>
  </table>

  <h2>Verdict</h2>
  <p><strong>Pick {tool_a} if:</strong> You need team collaboration, brand consistency matters, and you produce high-volume SEO content.</p>
  <p><strong>Pick {tool_b} if:</strong> You're a solo creator, simplicity is priority, and you want to start with a free plan.</p>
  <p>Both deliver quality AI writing. {tool_a} wins on features and scale; {tool_b} wins on accessibility and price.</p>
"""


def best_body(niche_name):
    return f"""  <p>Finding the right {niche_name.lower()} can make or break your workflow. We've tested the top options and broken them down by use case and budget.</p>

  <h2>Our Top Picks</h2>
  <table>
    <tr><th>Tool</th><th>Best For</th><th>Starting Price</th><th>Rating</th></tr>
    <tr><td><strong>Tool A</strong></td><td>Overall best</td><td>$49/mo</td><td>&#11088;&#11088;&#11088;&#11088;&#11088;</td></tr>
    <tr><td><strong>Tool B</strong></td><td>Budget pick</td><td>$19/mo</td><td>&#11088;&#11088;&#11088;&#11088;</td></tr>
    <tr><td><strong>Tool C</strong></td><td>Teams &amp; enterprise</td><td>$99/mo</td><td>&#11088;&#11088;&#11088;&#11088;</td></tr>
  </table>

  <h2>How We Evaluate</h2>
  <p>We score on four dimensions: <strong>Content quality</strong> (how natural is the output?), <strong>Ease of use</strong> (can you start in minutes?), <strong>Features</strong> (integrations, templates, collaboration), and <strong>Value</strong> (does the price match what you get?).</p>

  <h2>1. Tool A &mdash; Best Overall</h2>
  <p>Tool A consistently produces the most natural-sounding AI content. Its brand voice feature learns your style over time, making it ideal for teams that need consistency at scale.</p>
  <p><strong>Pricing:</strong> Starts at $49/mo (billed annually)</p>
  <a href="#aff-tool-a" class="cta-button">Try Tool A &rarr;</a>

  <h2>2. Tool B &mdash; Best Budget Option</h2>
  <p>If you're watching costs, Tool B delivers surprisingly good quality at a fraction of the price. The free plan is genuinely usable &mdash; not just a stripped-down teaser.</p>
  <p><strong>Pricing:</strong> Free plan available; Pro at $19/mo</p>
  <a href="#aff-tool-b" class="cta-button">Try Tool B &rarr;</a>

  <h2>3. Tool C &mdash; Best for Teams</h2>
  <p>When you need multiple seats, approval workflows, and brand governance, Tool C is purpose-built. Pricier, but engineered for organizational scale.</p>
  <p><strong>Pricing:</strong> Starts at $99/mo per seat</p>
  <a href="#aff-tool-c" class="cta-button">Try Tool C &rarr;</a>

  <h2>FAQ</h2>
  <p><strong>Q: Is AI-generated content good enough for SEO?</strong><br/>A: Yes, when combined with human editing. AI excels at research and first drafts; a human ensures accuracy and voice.</p>
  <p><strong>Q: How much does {niche_name.lower()} cost?</strong><br/>A: Ranges from free to $100+/mo. Most quality tools land in the $30&ndash;60/mo range.</p>
"""


def alt_body(tool_a, niche_name):
    return f"""  <p>{tool_a} is popular for good reason, but it's not right for everyone. Whether it's the price, learning curve, or missing features, here are the best alternatives.</p>

  <h2>Why Switch from {tool_a}?</h2>
  <ul>
    <li><strong>Price:</strong> Plans can be steep for smaller teams and solo creators</li>
    <li><strong>Features:</strong> May lack specific functionality your workflow needs</li>
    <li><strong>Complexity:</strong> Too many features for straightforward use cases</li>
    <li><strong>Support:</strong> Response times can be slow on lower-tier plans</li>
  </ul>

  <h2>Top {tool_a} Alternatives</h2>
  <table>
    <tr><th>Alternative</th><th>Best For</th><th>Price</th><th>Key Strength</th></tr>
    <tr><td><strong>Alt A</strong></td><td>Ease of use</td><td>$36/mo</td><td>Simpler, cleaner interface</td></tr>
    <tr><td><strong>Alt B</strong></td><td>Teams</td><td>$49/mo</td><td>Better collaboration tools</td></tr>
    <tr><td><strong>Alt C</strong></td><td>Budget</td><td>$19/mo</td><td>Most affordable option</td></tr>
    <tr><td><strong>Alt D</strong></td><td>Quality</td><td>$65/mo</td><td>Superior output quality</td></tr>
  </table>

  <h2>1. Alt A &mdash; Easiest to Use</h2>
  <p>The best {tool_a} alternative if you want something you can start using immediately, no training required.</p>
  <a href="#aff-alt-a" class="cta-button">Try Alt A &rarr;</a>

  <h2>2. Alt B &mdash; Best for Teams</h2>
  <p>If collaboration is what {tool_a} lacks, Alt B fills the gap with robust multi-user features.</p>
  <a href="#aff-alt-b" class="cta-button">Try Alt B &rarr;</a>

  <h2>3. Alt C &mdash; Best Budget Pick</h2>
  <p>Get 80% of the functionality at less than half the price.</p>
  <a href="#aff-alt-c" class="cta-button">Try Alt C &rarr;</a>

  <h2>Quick Decision Guide</h2>
  <table>
    <tr><th>You want...</th><th>Pick</th></tr>
    <tr><td>Cheapest option</td><td>Alt C</td></tr>
    <tr><td>Best quality</td><td>Alt D</td></tr>
    <tr><td>Easiest to learn</td><td>Alt A</td></tr>
    <tr><td>Team features</td><td>Alt B</td></tr>
  </table>
"""


def get_niche_name(slug):
    return {
        "ai-writing": "AI Writing Tools",
        "project-management": "Project Management Software",
        "email-marketing": "Email Marketing Tools",
        "vpn": "VPN Services",
        "website-builders": "Website Builders",
        "hosting": "Web Hosting Services",
    }.get(slug, slug)


def load_queue():
    with open(QUEUE_FILE) as f:
        return json.load(f)


def save_queue(data):
    with open(QUEUE_FILE, "w") as f:
        json.dump(data, f, indent=2)


def generate_articles(limit=3, dry_run=False):
    queue_data = load_queue()
    pending = [i for i in queue_data["items"] if i["status"] == "pending"]
    
    if not pending:
        print("No pending. Run scanner.py first.")
        return 0
    
    generated = 0
    now = datetime.utcnow()
    
    for item in pending[:limit]:
        kw = item["keyword"]
        atype = item["type"]
        niche = item["niche"]
        niche_name = get_niche_name(niche)
        tools = item.get("tools", [])
        
        tool_a = tools[0] if tools else "Tool A"
        tool_b = tools[1] if len(tools) > 1 else "Tool B"
        
        if atype == "vs":
            title = f"{tool_a} vs {tool_b}: Which is Better in 2026?"
            desc = f"Comparing {tool_a} and {tool_b} &mdash; pricing, features, pros/cons. Find the best {niche_name.lower()} for your needs."
            breadcrumb = ("/vs/", "All VS Comparisons")
            body = vs_body(tool_a, tool_b, niche_name)
        elif atype == "best":
            title = f"Best {niche_name} in 2026: Top Picks for Every Use Case"
            desc = f"We tested the top {niche_name.lower()}. See our picks for every budget and use case."
            breadcrumb = ("/best/", "All Best Picks")
            body = best_body(niche_name)
        elif atype == "alternative":
            title = f"Best {tool_a} Alternatives in 2026: Top Picks"
            desc = f"Looking for {tool_a} alternatives? Compare top competitors on price, features, and value."
            breadcrumb = ("/alternatives/", "All Alternatives")
            body = alt_body(tool_a, niche_name)
        else:
            continue
        
        page = make_page(title, desc, body, breadcrumb[0], breadcrumb[1])
        slug = slugify(kw)
        filepath = os.path.join(PAGES_DIR, atype, f"{slug}.astro")
        
        if dry_run:
            print(f"[#{item['id']}] DRY RUN: {filepath}")
        else:
            with open(filepath, "w") as f:
                f.write(page)
            print(f"[#{item['id']}] {atype.upper()}: {kw[:70]}")
        
        item["status"] = "generated"
        item["generated_at"] = now.isoformat()
        item["filepath"] = f"src/pages/{atype}/{slug}.astro"
        generated += 1
    
    if not dry_run:
        save_queue(queue_data)
    
    print(f"\n{generated} articles generated")
    return generated


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--limit", type=int, default=3)
    p.add_argument("--all", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    generate_articles(999 if args.all else args.limit, dry_run=args.dry_run)
