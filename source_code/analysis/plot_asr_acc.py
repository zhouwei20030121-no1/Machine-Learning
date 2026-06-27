import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

FIG_DIR = Path(__file__).resolve().parent.parent / "results" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

data = {
    "Position":[
        "top_left","top_center","top_right",
        "middle_left","center","middle_right",
        "bottom_left","bottom_center","bottom_right"
    ],
    "ACC":[
        0.7642,0.7261,0.7122,
        0.7639,0.7675,0.7240,
        0.7210,0.7591,0.7515
    ],
    "ASR":[
        0.9298,0.9535,0.9310,
        0.9747,0.9817,0.9820,
        0.9704,0.9764,0.9688
    ]
}

df = pd.DataFrame(data)

plt.figure(figsize=(12,6))

x = range(len(df))
width = 0.35

plt.bar(
    [i-width/2 for i in x],
    df["ACC"],
    width,
    label="Clean Accuracy"
)

plt.bar(
    [i+width/2 for i in x],
    df["ASR"],
    width,
    label="ASR"
)

plt.xticks(x, df["Position"], rotation=30)
plt.ylabel("Score")
plt.legend()

plt.tight_layout()
plt.savefig(FIG_DIR / "acc_asr_bar.png", dpi=300)
plt.show()