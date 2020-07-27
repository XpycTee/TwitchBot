import os

all_mods = []
for file in os.listdir("modules"):
    if file.endswith(".py"):
        if file != "__init__.py":
            #print(file.replace('.py', ''))
            all_mods.insert(len(all_mods), file.replace('.py', ''))
__all__ = all_mods