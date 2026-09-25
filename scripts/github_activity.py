import os
import requests
import datetime
from collections import Counter

# --- CONFIGURATION ---
USERNAME = "so-Subhadeep"  # Change this to your exact GitHub username
TOKEN = os.getenv("GH_TOKEN") 

def get_github_data():
    headers = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}
    
    # Fetch Repos for Languages
    repos_url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100"
    repos = requests.get(repos_url, headers=headers).json()
    
    langs = Counter()
    if isinstance(repos, list):
        for repo in repos:
            if repo.get("language") and not repo.get("fork"):
                langs[repo["language"]] += 1
    top_langs = langs.most_common(3)
    
    # Fetch Contributions (Simplified via User events/repos - for real heatmap use GraphQL, but this keeps it lightweight)
    user_url = f"https://api.github.com/users/{USERNAME}"
    user_data = requests.get(user_url, headers=headers).json()
    public_repos = user_data.get("public_repos", 0)
    followers = user_data.get("followers", 0)
    
    return top_langs, public_repos, followers

def generate_svg(top_langs, repos, followers):
    # Fallback languages if API fails
    if not top_langs:
        top_langs = [("Java", 60), ("Python", 30), ("JS", 10)]
        
    lang_elements = ""
    y_offset = 80
    colors = ["#ff79c6", "#bd93f9", "#8be9fd"]
    
    for i, (lang, count) in enumerate(top_langs):
        width = min(count * 5, 120) # Scale bar
        color = colors[i % len(colors)]
        lang_elements += f"""
        <text x="30" y="{y_offset}" class="text-bold" fill="#f8f8f2" font-size="14">{lang}</text>
        <rect x="90" y="{y_offset - 10}" width="{width}" height="10" rx="5" fill="{color}" class="bar-anim"/>
        """
        y_offset += 35

    svg_template = f"""<svg width="860" height="245" viewBox="0 0 860 245" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600;700&amp;display=swap');
            * {{ font-family: 'Segoe UI', Ubuntu, sans-serif; }}
            .bg {{ fill: #0b0c10; }}
            .card {{ fill: #1a1a2e; stroke: #ff79c6; stroke-width: 1.5; rx: 10; ry: 10; }}
            .text-title {{ fill: #ff79c6; font-size: 16px; font-weight: bold; letter-spacing: 2px; }}
            .text-bold {{ font-weight: 600; }}
            .glow {{ filter: drop-shadow(0 0 8px rgba(255, 121, 198, 0.6)); }}
            
            /* Animations */
            @keyframes float {{
                0% {{ transform: translateY(0px) rotate(0deg); opacity: 0; }}
                20% {{ opacity: 0.8; }}
                100% {{ transform: translateY(250px) rotate(360deg); opacity: 0; }}
            }}
            @keyframes pulse {{
                0%, 100% {{ stroke-opacity: 0.5; filter: drop-shadow(0 0 5px #ff79c6); }}
                50% {{ stroke-opacity: 1; filter: drop-shadow(0 0 15px #ff79c6); }}
            }}
            @keyframes barLoad {{
                0% {{ transform: scaleX(0); }}
                100% {{ transform: scaleX(1); }}
            }}
            @keyframes dash {{
                0% {{ stroke-dasharray: 0 1000; }}
                100% {{ stroke-dasharray: 220 1000; }}
            }}
            .sakura {{ animation: float 6s linear infinite; fill: #ffb7c5; }}
            .sakura-d1 {{ animation-delay: 1s; }}
            .sakura-d2 {{ animation-delay: 3s; }}
            .card-glow {{ animation: pulse 3s infinite; }}
            .bar-anim {{ transform-origin: left; animation: barLoad 1.5s ease-out forwards; }}
            .circle-anim {{ animation: dash 2s ease-out forwards; }}
        </style>
        <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#ff79c6;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#bd93f9;stop-opacity:1" />
        </linearGradient>
    </defs>

    <!-- Background -->
    <rect width="100%" height="100%" rx="15" class="bg glow"/>

    <!-- Decorative Top Line -->
    <text x="430" y="30" class="text-title" text-anchor="middle">🌸 GITHUB ACTIVITY 🌸</text>
    <text x="430" y="50" fill="#6272a4" font-size="12" text-anchor="middle" font-weight="600" letter-spacing="4px">CODE • BUILD • GROW</text>

    <!-- Cards -->
    <g transform="translate(30, 70)">
        <rect width="250" height="150" class="card card-glow"/>
        <text x="20" y="30" class="text-title">💻 LANGUAGES</text>
        {lang_elements}
    </g>

    <g transform="translate(305, 70)">
        <rect width="250" height="150" class="card card-glow"/>
        <text x="20" y="30" class="text-title">🔥 ACTIVITY RING</text>
        
        <!-- Circular Streak/Activity ring -->
        <circle cx="125" cy="95" r="40" fill="none" stroke="#282a36" stroke-width="8"/>
        <circle cx="125" cy="95" r="40" fill="none" stroke="url(#grad1)" stroke-width="8" stroke-dasharray="200" stroke-linecap="round" transform="rotate(-90 125 95)" class="circle-anim"/>
        
        <text x="125" y="90" fill="#f8f8f2" font-size="24" font-weight="bold" text-anchor="middle">{repos}</text>
        <text x="125" y="110" fill="#6272a4" font-size="10" font-weight="bold" text-anchor="middle">REPOS</text>
    </g>

    <g transform="translate(580, 70)">
        <rect width="250" height="150" class="card card-glow"/>
        <text x="20" y="30" class="text-title">📊 NETWORK</text>
        <text x="125" y="80" fill="#f8f8f2" font-size="32" font-weight="bold" text-anchor="middle" class="glow">{followers}</text>
        <text x="125" y="110" fill="#bd93f9" font-size="14" font-weight="bold" text-anchor="middle">FOLLOWERS</text>
        
        <!-- Mini Decorative grid to simulate contributions -->
        <g transform="translate(75, 125)">
            <rect x="0" y="0" width="8" height="8" fill="#ff79c6" rx="2" />
            <rect x="12" y="0" width="8" height="8" fill="#bd93f9" rx="2" />
            <rect x="24" y="0" width="8" height="8" fill="#ff79c6" rx="2" opacity="0.5"/>
            <rect x="36" y="0" width="8" height="8" fill="#bd93f9" rx="2" opacity="0.8"/>
            <rect x="48" y="0" width="8" height="8" fill="#ff79c6" rx="2" />
            <rect x="60" y="0" width="8" height="8" fill="#bd93f9" rx="2" opacity="0.3"/>
            <rect x="72" y="0" width="8" height="8" fill="#ff79c6" rx="2" />
            <rect x="84" y="0" width="8" height="8" fill="#bd93f9" rx="2" />
        </g>
    </g>

    <!-- Sakura Particles -->
    <circle cx="100" cy="-10" r="3" class="sakura"/>
    <circle cx="250" cy="-10" r="4" class="sakura sakura-d1"/>
    <circle cx="450" cy="-10" r="2.5" class="sakura sakura-d2"/>
    <circle cx="700" cy="-10" r="3.5" class="sakura sakura-d1"/>
    <circle cx="820" cy="-10" r="2" class="sakura"/>
</svg>"""

    # Ensure profile folder exists
    os.makedirs("profile", exist_ok=True)
    with open("profile/github-activity.svg", "w", encoding="utf-8") as f:
        f.write(svg_template)
    print("✨ Premium Sakura SVG Generated Successfully!")

if __name__ == "__main__":
    langs, repos, followers = get_github_data()
    generate_svg(langs, repos, followers)
