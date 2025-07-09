from datasets import load_dataset

# 1) Load the slice
small = load_dataset(
    "imageomics/TreeOfLife-10M",
    split="train[:2000]"
)

# 2) Save it to a local folder
small.save_to_disk("local_tree_of_life_2k")
