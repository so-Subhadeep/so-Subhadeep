import os
import requests

USERNAME = "so-Subhadeep"

# We fetch the exact layout you want, styled with your premium theme colors
STREAK_URL = (
    f"https://github-readme-streak-stats.herokuapp.com/?user={USERNAME}"
    "&hide_border=true"
    "&background=0a0512"
    "&ring=ff79c6"
    "&fire=ff79c6"
    "&currStreakNum=f8f8f2"
    "&sideNums=f8f8f2"
    "&currStreakLabel=bd93f9"
    "&sideLabels=6272a4"
    "&dates=6272a4"
)

def generate_animated_streak():
    # 1. Fetch the generated SVG from the Streak API
    response = requests.get(STREAK_URL)
    if response.status_code != 200:
        print("Failed to fetch streak data.")
        return
        
    svg_content = response.text
    
    # 2. Define our classy, minimal Sakura animation
    sakura_css = """
    <style>
        @keyframes float {
            0% { transform: translate(0, -30px) rotate(0deg); opacity: 0; }
            20% { opacity: 0.7; }
            80% { opacity: 0.7; }
            100% { transform: translate(25px, 220px) rotate(360deg); opacity: 0; }
        }
        .petal { animation: float 6s linear infinite; fill: #ffb7c5; opacity: 0.7; }
        .d1 { animation-delay: -1s; animation-duration: 5s; }
        .d2 { animation-delay: -3s; animation-duration: 7s; }
        .d3 { animation-delay: -2s; animation-duration: 6s; }
        
        /* Subtle glow for the main stats */
        .stat, .curr-streak { filter: drop-shadow(0 0 5px rgba(255, 121, 198, 0.4)); }
    </style>
    """
    
    sakura_defs = """
    <defs>
        <path id="sakura" d="M10,0 C15,-5 20,5 10,15 C0,5 5,-5 10,0 Z" />
    </defs>
    """
    
    # 3. Position the petals across the streak card (Width is 495px)
    sakura_petals = """
    <use href="#sakura" x="40" y="-20" class="petal d1" transform="scale(0.8)" />
    <use href="#sakura" x="140" y="-20" class="petal d2" />
    <use href="#sakura" x="240" y="-20" class="petal d3" transform="scale(1.2)" />
    <use href="#sakura" x="350" y="-20" class="petal d1" transform="scale(0.9)" />
    <use href="#sakura" x="430" y="-20" class="petal d2" transform="scale(1.1)" />
    """
    
    # 4. Inject our custom code right before the closing </svg> tag
    injection = sakura_css + sakura_defs + sakura_petals + "</svg>"
    final_svg = svg_content.replace("</svg>", injection)
    
    # 5. Save the final masterpiece
    os.makedirs("profile", exist_ok=True)
    with open("profile/github-activity.svg", "w", encoding="utf-8") as f:
        f.write(final_svg)
    print("✨ Classy Sakura Streak SVG Generated!")

if __name__ == "__main__":
    generate_animated_streak()
