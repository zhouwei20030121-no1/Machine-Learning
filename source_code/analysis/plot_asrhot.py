import matplotlib.pyplot as plt
import numpy as np

asr = np.array([
    [0.9298,0.9535,0.9310],
    [0.9747,0.9817,0.9820],
    [0.9704,0.9764,0.9688]
])

plt.figure(figsize=(7,6))

im = plt.imshow(
    asr,
    cmap="YlOrRd"
)

plt.xticks(
    [0,1,2],
    ["Top Left","Top Center","Top Right"]
)

plt.yticks(
    [0,1,2],
    ["Top","Middle","Bottom"]
)

for i in range(3):
    for j in range(3):

        color = "white" if asr[i,j] > 0.96 else "black"

        plt.text(
            j,
            i,
            f"{asr[i,j]:.3f}",
            ha="center",
            va="center",
            color=color,
            fontsize=12,
            fontweight="bold"
        )

plt.colorbar(label="ASR")

plt.title("ASR Heatmap")

plt.tight_layout()

plt.savefig("asr_heatmap.png", dpi=300)

plt.show()