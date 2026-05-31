import urllib.request
import re

# Your actual Play Store URL
url = "https://play.google.com/store/apps/developer?id=AnAk+Tech+Solutions&hl=en"

# Disguise the script request so Google permits the connection
req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
)

try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
except Exception as e:
    print(f"Error fetching data: {e}")
    exit(1)

# Search your page to find individual App ID links and Title texts
# Google Play Store structural link pattern: /store/apps/details?id=your.package.name
apps_found = re.findall(r'/store/apps/details\?id=([^"&\s>]+)', html)
# Clean up duplicate matches
unique_app_ids = list(dict.fromkeys(apps_found))

# Base structure for our newly generated app grid
apps_html_cards = ""

if not unique_app_ids:
    # Backup placeholder code if Google applies scraping protection blocks
    apps_html_cards = """
    <div class="app-card">
        <div class="app-icon">🤖</div>
        <h3>Explore Our Store Profile</h3>
        <p>Live applications are actively served directly on Google Play.</p>
        <a href="https://play.google.com/store/apps/developer?id=AnAk+Tech+Solutions&hl=en" target="_blank" class="btn-secondary">View Applications</a>
    </div>
    """
else:
    for app_id in unique_app_ids:
        # Generate clean human-readable names from package names for presentation
        display_name = app_id.split('.')[-1].replace('_', ' ').replace('-', ' ').title()
        
        apps_html_cards += f"""
        <div class="app-card">
            <div class="app-icon">📱</div>
            <h3>{display_name}</h3>
            <p>Package ID: {app_id}. Get the official, verified release build straight from the Google Play Store.</p>
            <a href="https://play.google.com/store/apps/details?id={app_id}&hl=en" target="_blank" class="btn-secondary">Download App</a>
        </div>
        """

# Define the comprehensive template to write over index.html
full_page_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AnAk Tech Solutions - Android Apps</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <header>
        <div class="container">
            <h1>AnAk Tech Solutions</h1>
            <p>Innovative, Reliable Android Applications</p>
            <a href="https://play.google.com/store/apps/developer?id=AnAk+Tech+Solutions&hl=en" target="_blank" class="btn-primary">View Developer Profile</a>
        </div>
    </header>

    <main class="container">
        <h2>Our Google Play Store Apps (Auto-Updated)</h2>
        <div class="apps-grid">
            {apps_html_cards}
        </div>
    </main>

    <footer>
        <p>&copy; 2026 AnAk Tech Solutions. All rights reserved.</p>
    </footer>

</body>
</html>"""

# Overwrite index.html automatically
with open("index.html", "w", encoding="utf-8") as file:
    file.write(full_page_content)

print("index.html successfully synchronized with Google Play Store!")
