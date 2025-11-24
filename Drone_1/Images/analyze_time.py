import json
import math
import matplotlib.pyplot as plt
from collections import defaultdict

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def mean_of_list(lst):
    if not lst:
        return float('nan')
    return sum(lst) / len(lst)

def plot_models(data, mission_name):
    grouped = defaultdict(lambda: {"Hailo8": defaultdict(list),
                                   "Hailo8L": defaultdict(list),
                                   "images_order": []})

    color_map = {
        "Hailo8": "blue",
        "Hailo8L": "red"
    }

    for entry in data:
        model_full = entry.get("model_name", "")
        exec_time = entry.get("execution_time")
        image = entry.get("image")

        if exec_time is None or image is None or not model_full:
            continue

        if model_full.endswith("_Hailo8"):
            model_base = model_full[:-7]
            grouped[model_base]["Hailo8"][image].append(exec_time)
        elif model_full.endswith("_Hailo8L"):
            model_base = model_full[:-8]
            grouped[model_base]["Hailo8L"][image].append(exec_time)
        else:
            continue

        if image not in grouped[model_base]["images_order"]:
            grouped[model_base]["images_order"].append(image)

    for model_base, measures in grouped.items():
        images = measures["images_order"]

        y_hailo8 = []
        y_hailo8l = []

        means_hailo8_per_image = []
        means_hailo8l_per_image = []

        for img in images:
            times_h8 = measures["Hailo8"].get(img, [])
            times_h8l = measures["Hailo8L"].get(img, [])

            if model_base == "Grape_Diseases":
                mean_h8 = mean_of_list(times_h8) if times_h8 else float('nan')
                mean_h8l = mean_of_list(times_h8l) if times_h8l else float('nan')
                y_hailo8.append(mean_h8)
                y_hailo8l.append(mean_h8l)
                if times_h8:
                    means_hailo8_per_image.append(mean_h8)
                if times_h8l:
                    means_hailo8l_per_image.append(mean_h8l)
            else:
                mean_h8 = mean_of_list(times_h8) if times_h8 else float('nan')
                mean_h8l = mean_of_list(times_h8l) if times_h8l else float('nan')
                y_hailo8.append(mean_h8)
                y_hailo8l.append(mean_h8l)

        if model_base == "Grape_Diseases":
            mean_hailo8 = mean_of_list([m for m in means_hailo8_per_image if not math.isnan(m)]) if means_hailo8_per_image else None
            mean_hailo8l = mean_of_list([m for m in means_hailo8l_per_image if not math.isnan(m)]) if means_hailo8l_per_image else None
        else:
            all_h8_times = []
            all_h8l_times = []
            for img in images:
                all_h8_times.extend(measures["Hailo8"].get(img, []))
                all_h8l_times.extend(measures["Hailo8L"].get(img, []))
            mean_hailo8 = mean_of_list(all_h8_times) if all_h8_times else None
            mean_hailo8l = mean_of_list(all_h8l_times) if all_h8l_times else None

        # Convert everything to milliseconds multiplying by 1000
        y_hailo8_ms = [v * 1000 if not math.isnan(v) else float('nan') for v in y_hailo8]
        y_hailo8l_ms = [v * 1000 if not math.isnan(v) else float('nan') for v in y_hailo8l]
        mean_hailo8_ms = mean_hailo8 * 1000 if mean_hailo8 is not None else None
        mean_hailo8l_ms = mean_hailo8l * 1000 if mean_hailo8l is not None else None

        plt.figure(figsize=(10, 6))

        if any(not math.isnan(v) for v in y_hailo8_ms):
            plt.plot(images, y_hailo8_ms, marker='o', label="Hailo8", color=color_map["Hailo8"])
        if any(not math.isnan(v) for v in y_hailo8l_ms):
            plt.plot(images, y_hailo8l_ms, marker='o', label="Hailo8L", color=color_map["Hailo8L"])

        if mean_hailo8_ms is not None:
            plt.axhline(mean_hailo8_ms, linestyle='--', color=color_map["Hailo8"], alpha=0.6, label=f"Mean Hailo8 {mean_hailo8_ms:.2f} ms")
        if mean_hailo8l_ms is not None:
            plt.axhline(mean_hailo8l_ms, linestyle='--', color=color_map["Hailo8L"], alpha=0.6, label=f"Mean Hailo8L {mean_hailo8l_ms:.2f} ms")

        plt.xlabel("Image")
        plt.ylabel("Execution Time (ms)")
        plt.title(f"{mission_name}_{model_base}_Comparison")
        plt.xticks(rotation=45, ha="right")
        plt.legend()
        plt.grid(True, color='gray', linestyle='--', alpha=0.5)
        plt.tight_layout()

        output_name = f"{mission_name}_{model_base}_Comparison.png"
        plt.savefig(output_name)
        plt.close()
        print(f"Saved plot: {output_name}")

def main():
    mission1_data = load_json("analyze_time_mission1.json")
    mission2_data = load_json("analyze_time_mission2.json")

    plot_models(mission1_data, "Mission1")
    plot_models(mission2_data, "Mission2")

if __name__ == "__main__":
    main()
