import os

# EDIT: set this to the folder that contains archive5, archive6, ... or point to each dataset root
ARCHIVE_ROOT = r"D:\Khushi\project\mini project - 5th sem\agrovision_2\dataset"  

def scan_folder(root):
    class_counts = {}
    total = 0
    for dirpath, dirnames, filenames in os.walk(root):
        # skip nested traversal into image files directly, only count when we are in a class folder
        if dirpath == root:
            continue
        # consider a folder a class folder if it contains images
        img_files = [f for f in filenames if f.lower().endswith(('.jpg','.jpeg','.png','.bmp'))]
        if img_files:
            cls = os.path.relpath(dirpath, root)
            class_counts[cls] = class_counts.get(cls, 0) + len(img_files)
            total += len(img_files)
    return class_counts, total

if __name__ == "__main__":
    print("Scanning archives in:", ARCHIVE_ROOT)
    grand_classes = {}
    grand_total = 0
    # scan every archive folder inside ARCHIVE_ROOT
    for archive_name in sorted(os.listdir(ARCHIVE_ROOT)):
        archive_path = os.path.join(ARCHIVE_ROOT, archive_name)
        if os.path.isdir(archive_path):
            classes, total = scan_folder(archive_path)
            print(f"\n{archive_name}: {len(classes)} classes, {total} images")
            # accumulate
            for k,v in classes.items():
                grand_classes[k] = grand_classes.get(k, 0) + v
            grand_total += total

    print("\nCombined classes:", len(grand_classes))
    print("Total images:", grand_total)
    print("\nSample class counts (first 30):")
    for i, (k,v) in enumerate(sorted(grand_classes.items(), key=lambda x:-x[1])):
        print(f"{k} -> {v}")
        if i>=29: break
