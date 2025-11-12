import json

# Original data_ids dictionary
data_ids = {
    "3879": ("TG", "Female"),
    "3880": ("TG", "Female"),
    "3881": ("TG", "Male"),
    "3882": ("TG", "Male"),
    "3883": ("WT", "Male"),
    "3884": ("TG", "Male"),
    "3885": ("TG", "Female"),
    "3886": ("TG", "Male"),
    "3968": ("WT", "Female"),
    "3969": ("TG", "Female"),
    "3970": ("WT", "Male"),
    "3971": ("TG", "Male"),
    "3972": ("WT", "Male"),
    "3994": ("TG", "Female"),
    "3995": ("TG", "Male"),
    "3996": ("TG", "Male"),
    "3997": ("TG", "Male"),
    "3998": ("TG", "Male"),
    "3999": ("TG", "Male"),
    "2200_1L":   ("WT", "Male"),
    "2200_1R":   ("WT", "Male"),
    "2199_1R": ("WT", "Female"),
    "2221_1L": ("WT", "Female"),
    "2221_1R": ("WT", "Female"),
    "2221_1RL":  ("WT", "Female"),
    "2222_1L": ("WT", "Male"),
    "2222_1R": ("WT", "Male"),
    "2222_1RL":("WT", "Male"),
    "2273_1L": ("TG", "Female"),
    "2273_1R": ("TG", "Female"),
    "2273_1RL":("TG", "Female"),
    "2273_2R":   ("TG", "Female"),
    "2280_1R": ("WT", "Female"),
    "2280_1B":  ("WT", "Female"),
    "2512_1L": ("WT", "Male"),
    "2512_2R": ("WT", "Male"),
    "2517_1R": ("WT", "Male"),
    "2886": ("WT", "Male"),
    "2887": ("WT", "Male"),
    "3000": ("WT", "Female"),
    "3043": ("TG", "Female"),
    "1777_1R": ("WT", "Female"),
    "1777_2R": ("WT", "Female"),
    "3151": ("WT", "Female"),
    "3153": ("TG", "Male"),
    "1825_1R": ("TG", "Male"),
    "1825_2L": ("WT", "Male"),
    "3220": ("TG", "Female"),
    "3223": ("TG", "Male"),
    "3272": ("WT", "Female"),
    "3274": ("WT", "Female"),
    "3275": ("TG", "Female"),
    "3276": ("TG", "Female"),
    "3278": ("TG", "Male"),
    "3607": ("TG", "Female")
}

# Convert tuples to lists for JSON compatibility
data_ids_json_ready = {k: list(v) for k, v in data_ids.items()}

output_folder = input("Where do you want to save your json file? ")

# Save to JSON file
with open(output_folder+"/data_ids.json", "w", encoding="utf-8") as f:
    json.dump(data_ids_json_ready, f, indent=4)

print("✅ data_ids.json has been created successfully!")
