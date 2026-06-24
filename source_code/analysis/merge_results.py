import argparse
from pathlib import Path

import pandas as pd

from utils.config import CSV_DIR, POSITION_ORDER


def tradeoff_type(asr: float, detection_score: float, asr_threshold: float = 0.8, score_threshold: float = 0.8) -> str:
    asr_level = "高 ASR" if asr >= asr_threshold else "低 ASR"
    score_level = "高检测分数" if detection_score >= score_threshold else "低检测分数"
    return f"{asr_level} + {score_level}"


def load_optional_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def merge_results(part1: Path, part2: Path, detection: Path, output: Path) -> pd.DataFrame:
    attack = pd.concat([load_optional_csv(part1), load_optional_csv(part2)], ignore_index=True)
    if attack.empty:
        raise FileNotFoundError("No attack result rows found.")
    if attack["Position"].duplicated().any():
        dupes = attack.loc[attack["Position"].duplicated(), "Position"].tolist()
        raise ValueError(f"Duplicate positions in attack results: {dupes}")

    missing_positions = [p for p in POSITION_ORDER if p not in set(attack["Position"])]
    if missing_positions:
        raise ValueError(f"Missing positions: {missing_positions}")

    detection_df = pd.read_csv(detection)
    merged = attack.merge(
        detection_df[["Position", "Detection Score", "Mask Norm", "Detection Difficulty"]],
        on="Position",
        how="left",
    )
    required_cols = ["Clean Accuracy", "ASR", "Detection Score", "Mask Norm", "Detection Difficulty"]
    if merged[required_cols].isna().any().any():
        raise ValueError("Merged results contain missing values in required columns.")

    merged["Position"] = pd.Categorical(merged["Position"], categories=POSITION_ORDER, ordered=True)
    merged = merged.sort_values("Position").reset_index(drop=True)
    merged["Tradeoff Type"] = merged.apply(
        lambda row: tradeoff_type(float(row["ASR"]), float(row["Detection Score"])),
        axis=1,
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(output, index=False, encoding="utf-8")
    return merged


def main() -> None:
    parser = argparse.ArgumentParser(description="Merge attack and detection CSV files into final_results.csv.")
    parser.add_argument("--part1", default=str(CSV_DIR / "asr_acc_results_part1.csv"))
    parser.add_argument("--part2", default=str(CSV_DIR / "asr_acc_results_part2.csv"))
    parser.add_argument("--detection", default=str(CSV_DIR / "detection_results.csv"))
    parser.add_argument("--output", default=str(CSV_DIR / "final_results.csv"))
    args = parser.parse_args()

    merged = merge_results(Path(args.part1), Path(args.part2), Path(args.detection), Path(args.output))
    print(merged)


if __name__ == "__main__":
    main()

