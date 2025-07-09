import pandas as pd
import os

input_dir = "C:\\Mani\\learn\\Courses\\BioCosmos\\Butterfly_Project\\Data\\nymphalidae_whole_specimen-v240606"


def missing_metadata(df):
    """Find images that exist but don't have corresponding metadata records"""
    # Get all metadata records as a set for faster lookup
    metadata_records = set()
    for _, row in df.iterrows():
        metadata_records.add(f"{row['species']}/{row['mask_name']}")
    
    # Find all images in the directory structure
    images_dir = os.path.join(input_dir, "images")
    found_images = set()
    missing_metadata_list = []
    
    if os.path.exists(images_dir):
        # Iterate through species directories
        for species_folder in os.listdir(images_dir):
            species_path = os.path.join(images_dir, species_folder)
            if os.path.isdir(species_path):
                # Iterate through images in each species folder
                for image_file in os.listdir(species_path):
                    if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                        image_key = f"{species_folder}/{image_file}"
                        found_images.add(image_key)
                        if image_key not in metadata_records:
                            missing_metadata_list.append({
                                'species': species_folder,
                                'mask_name': image_file,
                                'full_path': os.path.join(species_path, image_file)
                            })
    
    print(f"Total images found: {len(found_images)}")
    print(f"Images missing metadata: {len(missing_metadata_list)}")
    if missing_metadata_list:
        print("\nFirst 10 images missing metadata:")
        for i, item in enumerate(missing_metadata_list[:10]):
            print(f"{i+1}. {item['species']}/{item['mask_name']}")
    
    return missing_metadata_list


def missing_image(df):
    """Find metadata records that don't have corresponding image files"""
    images_dir = os.path.join(input_dir, "images")
    missing_images = []
    
    # Check each metadata record for corresponding image file
    for _, row in df.iterrows():
        species = row['species']
        mask_name = row['mask_name']
        
        # Construct the expected image path
        expected_path = os.path.join(images_dir, species, mask_name)
        
        # Check if the image file exists
        if not os.path.exists(expected_path):
            missing_images.append({
                'species': species,
                'mask_name': mask_name,
                'expected_path': expected_path
            })
    
    # Add a column to the dataframe indicating if image exists
    df['image_exists'] = df.apply(lambda row: os.path.exists(
        os.path.join(images_dir, row['species'], row['mask_name'])
    ), axis=1)
    
    print(f"Total metadata records: {len(df)}")
    print(f"Records missing images: {len(missing_images)}")
    if missing_images:
        print("\nFirst 10 records missing images:")
        for i, item in enumerate(missing_images[:10]):
            print(f"{i+1}. {item['species']}/{item['mask_name']}")
    
    return missing_images


def main():
    metadata_file = os.path.join(input_dir, "metadata", "data_meta-nymphalidae_whole_specimen-v240606_subset.csv")
    df = pd.read_csv(metadata_file)
    
    print("=== Checking for missing images ===")
    missing_imgs = missing_image(df)
    
    print("\n=== Checking for missing metadata ===")
    missing_meta = missing_metadata(df)
    
    # Optional: Save results to files
    if missing_imgs:
        missing_imgs_df = pd.DataFrame(missing_imgs)
        missing_imgs_df.to_csv(os.path.join(input_dir, "missing_images_report.csv"), index=False)
        print(f"\nMissing images report saved to: {os.path.join(input_dir, 'missing_images_report.csv')}")
    
    if missing_meta:
        missing_meta_df = pd.DataFrame(missing_meta)
        missing_meta_df.to_csv(os.path.join(input_dir, "missing_metadata_report.csv"), index=False)
        print(f"Missing metadata report saved to: {os.path.join(input_dir, 'missing_metadata_report.csv')}")


if __name__ == "__main__":
    main()