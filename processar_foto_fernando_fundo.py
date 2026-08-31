from pathlib import Path

import cv2
import numpy as np


ROOT = Path(__file__).resolve().parent
SOURCE = Path("/data/.openclaw/workspace/media/inbound/openclaw-staged-61bab1d7-3bbd-400f-949d-8edded389b66/d2dbf90c-68c5-47a3-85f1-e8840cbdc008.jpg")
BACKGROUND = Path("/data/.openclaw/agents/main/agent/codex-home/generated_images/01a055b0-78ab-7253-9c39-6f360860bfa5/exec-4fb2eec6-d4ce-499b-adc6-dd705c442c35.png")
OUTPUT = ROOT / "assets/instrutor-fernando-fundo-curso.png"


original = cv2.imread(str(SOURCE), cv2.IMREAD_COLOR)
background = cv2.imread(str(BACKGROUND), cv2.IMREAD_COLOR)
if original is None or background is None:
    raise SystemExit("Imagem de origem ou fundo não encontrada.")

h, w = original.shape[:2]
background = cv2.resize(background, (w, h), interpolation=cv2.INTER_LANCZOS4)

# Segmentação conservadora: a pessoa ocupa o centro e a metade inferior da foto.
mask = np.full((h, w), cv2.GC_PR_BGD, np.uint8)
bg_model = np.zeros((1, 65), np.float64)
fg_model = np.zeros((1, 65), np.float64)

# Bordas são fundo certo; pequenas sementes internas marcam pessoa certa.
mask[:25, :] = cv2.GC_BGD
mask[:, :25] = cv2.GC_BGD
mask[:, -25:] = cv2.GC_BGD
cv2.ellipse(mask, (w // 2, 430), (165, 285), 0, 0, 360, cv2.GC_FGD, -1)
cv2.ellipse(mask, (w // 2, 190), (150, 105), 0, 0, 360, cv2.GC_FGD, -1)
body_seed = np.array([[210, h - 20], [235, 890], [370, 785], [625, 790], [790, 930], [900, h - 20]], np.int32)
cv2.fillPoly(mask, [body_seed], cv2.GC_FGD)
cv2.grabCut(original, mask, None, bg_model, fg_model, 12, cv2.GC_INIT_WITH_MASK)

foreground = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0).astype("uint8")

# Suavização mínima apenas na borda do recorte. O interior mantém os pixels originais.
kernel = np.ones((3, 3), np.uint8)
foreground = cv2.morphologyEx(foreground, cv2.MORPH_CLOSE, kernel, iterations=2)
foreground = cv2.erode(foreground, kernel, iterations=2)
alpha = cv2.GaussianBlur(foreground, (0, 0), 1.1).astype(np.float32) / 255.0
alpha = alpha[:, :, None]

composite = original.astype(np.float32) * alpha + background.astype(np.float32) * (1.0 - alpha)
cv2.imwrite(str(OUTPUT), np.clip(composite, 0, 255).astype(np.uint8), [cv2.IMWRITE_PNG_COMPRESSION, 3])
print(OUTPUT)
