"""Erase the existing name from certificate.png. The name area lies on a
nearly uniform background, so we sample the background color from the empty
left/right margin at the same vertical band as the name, and gradient-fill
the area row by row using only those side-margin samples (which are guaranteed
to be free of text)."""

from PIL import Image
import numpy as np

SRC = "certificate.png"
DST = "certificate-clean.png"

img = Image.open(SRC).convert("RGB")
W, H = img.size
print(f"Source: {W}x{H}")

# Name vertical span with safety padding
NAME_TOP    = int(H * 0.368)
NAME_BOTTOM = int(H * 0.462)
print(f"Erase band: y={NAME_TOP}..{NAME_BOTTOM} ({NAME_BOTTOM-NAME_TOP}px)")

# For each row in the erase band, we sample background color from the
# horizontal margins on the LEFT and RIGHT of where the name appears.
# In the original, the name spans roughly x=900..4500 (5461 width).
# So x=600..880 (left margin) and x=4520..4800 (right margin) are pure
# background at every y in the name region — clean of any text.

LEFT_X1, LEFT_X2   = int(W * 0.110), int(W * 0.160)   # ~600..874
RIGHT_X1, RIGHT_X2 = int(W * 0.840), int(W * 0.890)   # ~4587..4860

arr = np.array(img)  # shape (H, W, 3)

for y in range(NAME_TOP, NAME_BOTTOM):
    left_avg  = arr[y, LEFT_X1:LEFT_X2].mean(axis=0)
    right_avg = arr[y, RIGHT_X1:RIGHT_X2].mean(axis=0)
    # Linear gradient from left color to right color across the row
    row = np.linspace(left_avg, right_avg, W).astype(np.uint8)
    arr[y, :] = row

Image.fromarray(arr).save(DST, "PNG", optimize=True)
print(f"Saved: {DST}")
