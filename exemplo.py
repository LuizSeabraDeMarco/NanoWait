from nano_wait.vision import VisionMode
import time

# =======================
# Marcação interativa de regiões
# =======================
print("\n================ MARCAR REGIÕES =================\n")
# Vamos marcar duas regiões como exemplo
coords1 = VisionMode.mark_region()
coords2 = VisionMode.mark_region()

# Use as coordenadas capturadas
regioes = [coords1, coords2]

# =======================
# Modo OBSERVE
# =======================
print("\n================ MODE: OBSERVE ================\n")
vision_observe = VisionMode(mode="observe")
results_observe = vision_observe.capture_numbers(regioes)

for reg, nums in results_observe.items():
    print(f"👁 Região {reg}: números detectados = {nums}")

time.sleep(1)

# =======================
# Modo DECISION
# =======================
print("\n================ MODE: DECISION ================\n")
vision_decision = VisionMode(mode="decision")
vision_decision.run(regioes)

time.sleep(1)

# =======================
# Modo LEARN
# =======================
print("\n================ MODE: LEARN ================\n")
vision_learn = VisionMode(mode="learn")
vision_learn.run(regioes)

print("\n✅ Exemplo concluído! Ajuste as regiões conforme necessário para capturar os números corretamente.\n")
