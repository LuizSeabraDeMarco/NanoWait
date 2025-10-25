from nano_wait.vision import VisionMode

# Marque regiões interativamente
regiao1 = VisionMode.mark_region()
regiao2 = VisionMode.mark_region()
regioes = [regiao1, regiao2]

# Modo observe
vision = VisionMode(mode="observe")
vision.run(regioes)

# Modo decision
vision = VisionMode(mode="decision")
vision.run(regioes)

# Modo learn
vision = VisionMode(mode="learn")
vision.run(regioes)
