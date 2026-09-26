import os
import shutil
from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), "..", "images", "closet-organizer-hanger")
PROBLEM_SRC = r"C:\Users\Administrateur\.cursor\projects\c-Users-Administrateur-cursor\assets\c__Users_Administrateur_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_ChatGPT_Image_26_sept._2026__17_14_59-3b824f73-0433-447e-acaf-efe8fbb8a88a.png"
GIF_SRC = r"D:\download\V Shaped Double-Sided Closet\video.gif"
MAX = 1200
QUALITY = 85

os.makedirs(ROOT, exist_ok=True)

shutil.copy2(PROBLEM_SRC, os.path.join(ROOT, "story-problem.png"))
prob = Image.open(os.path.join(ROOT, "story-problem.png")).convert("RGBA")
if max(prob.size) > MAX:
    r = MAX / max(prob.size)
    prob = prob.resize((int(prob.width * r), int(prob.height * r)), Image.Resampling.LANCZOS)
prob.save(os.path.join(ROOT, "story-problem.webp"), "WEBP", quality=92, method=6)
print("story-problem ok")

gif = Image.open(GIF_SRC)
frames = []
durations = []
try:
    while True:
        frame = gif.copy().convert("RGBA")
        if max(frame.size) > MAX:
            r = MAX / max(frame.size)
            frame = frame.resize((int(frame.width * r), int(frame.height * r)), Image.Resampling.LANCZOS)
        frames.append(frame)
        durations.append(gif.info.get("duration", 80))
        gif.seek(gif.tell() + 1)
except EOFError:
    pass

if not frames:
    raise SystemExit("no gif frames")

poster = frames[0].copy()
poster.save(os.path.join(ROOT, "story-solution-poster.webp"), "WEBP", quality=88, method=6)

dur = durations[0] if durations else 80
frames[0].save(
    os.path.join(ROOT, "story-solution.webp"),
    save_all=True,
    append_images=frames[1:],
    duration=dur,
    loop=0,
    quality=QUALITY,
    method=6,
)
print("story-solution frames", len(frames))
