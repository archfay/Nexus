from PIL import Image, ImageDraw
import os

os.makedirs("assets", exist_ok=True)

# nexus_assets.png
img = Image.new('RGB', (256, 256), color='#1a1a2e')
draw = ImageDraw.Draw(img)
draw.text((50, 100), "ASSETS", fill='#00ff00')
img.save("assets/nexus_assets.png")

# nexus_logs.png
img = Image.new('RGB', (256, 256), color='#0f3460')
draw = ImageDraw.Draw(img)
draw.text((60, 100), "LOGS", fill='#e94560')
img.save("assets/nexus_logs.png")

# nexus_backups.png
img = Image.new('RGB', (256, 256), color='#16213e')
draw = ImageDraw.Draw(img)
draw.text((40, 100), "BACKUPS", fill='#0f3460')
img.save("assets/nexus_backups.png")

print("✅ Assets generated successfully!")
