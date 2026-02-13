import os

names=[]

for f in os.listdir("sounds"):
    filename=os.path.splitext(f)[0]
    text=f'"{filename}":pygame.mixer.Sound("sounds/{filename}.mp3"),'
    names.append(text)

names.sort()

print("\n".join(names))