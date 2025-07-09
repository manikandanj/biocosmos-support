from pygbif import species

variation_1 = "chlosyne_gaudealis"
variation_2 = "chlosyne_gaudialis"

variation_1 = variation_1.replace("_", " ")
variation_2 = variation_2.replace("_", " ")

non_strict_result = species.name_backbone(name=variation_1, verbose=True, strict=False)
print(f"{variation_1}: {non_strict_result}")
print("\n")
non_strict_result = species.name_backbone(name=variation_2, verbose=True, strict=False)
print(f"{variation_2}: {non_strict_result}")
print("\n\n")

strict_result = species.name_backbone(name=variation_1, verbose=True, strict=True)
print(f"{variation_1}: {strict_result}")
print("\n")
strict_result = species.name_backbone(name=variation_2, verbose=True, strict=True)
print(f"{variation_2}: {strict_result}")

# species.mat