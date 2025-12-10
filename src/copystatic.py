import os
import shutil
import sys


def copy_directory_contents(src_dir, dst_dir):
    # Logging start of operation
    print(f"starting copy from '{src_dir} to {dst_dir}")

    # Delete all contents of destination dir if it exists
    if os.path.exists(dst_dir) and os.path.isdir(dst_dir):
        print(f"Cleaning destination dir: {dst_dir}")
        try:
            shutil.rmtree(dst_dir)
            print(f"Successfully cleaned {dst_dir}")
        except Exception as e:
            print(f"Error cleaning {dst_dir}: {e}")
            sys.exit(1)

    # Create destination dir
    try:
        os.mkdir(dst_dir)
        print(f"Created destination dir: {dst_dir}")
    except Exception as e:
        print(f"Error creating {dst_dir}: {e}")
        sys.exit(1)

    # Helper function to Recursively copy all contents
    def copy_recursive(curr_src, curr_dst):
        # Ensure destination dir exists
        if not os.path.exists(curr_dst):
            os.mkdir(curr_dst)

        # List all items in the current src dir
        items = os.listdir(curr_src)
        for item in items:
            src_path = os.path.join(curr_src, item)
            dst_path = os.path.join(curr_dst, item)

            # Check if it's a file
            if os.path.isfile(src_path):
                # Copy the file
                shutil.copy(src_path, dst_path)
                print(f"Copied file: {src_path} -> {dst_path}")

            # its not a file so we create it and copy its contents recursively
            else:
                print(f"Creating dir: {dst_path}")
                os.mkdir(dst_path)
                copy_recursive(src_path, dst_path)

    copy_recursive(src_dir, dst_dir)
    print(f"\nSuccessfully copied all contents from '{src_dir}' to '{dst_dir}'")
