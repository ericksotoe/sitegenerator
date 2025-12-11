import os
import pathlib
import shutil
import sys

from markdown_blocks import extract_title, markdown_to_html_node


def copy_directory_contents(src_dir, dst_dir):
    # Logging start of operation
    print(f"starting copy from '{src_dir}' to '{dst_dir}'")

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
        os.makedirs(dst_dir, exist_ok=True)
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


def generate_page(from_path, template_path, dest_path):
    print(
        f"Generating page from: {from_path}\nto: {dest_path}\nusing the {template_path} template"
    )
    markdown_text = ""
    template_file = ""
    try:
        with open(from_path, "r") as file:
            markdown_text = file.read()
        with open(template_path, "r") as file:
            template_file = file.read()
    except FileNotFoundError:
        print(f"Error: the file {from_path} was not found")
        sys.exit(1)

    html_string = markdown_to_html_node(markdown_text).to_html()
    page_title = extract_title(markdown_text)
    filled = template_file.replace("{{ Title }}", page_title)
    filled = filled.replace("{{ Content }}", html_string)

    dir_path = os.path.dirname(dest_path)
    if dir_path != "":
        os.makedirs(dir_path, exist_ok=True)
    try:
        with open(dest_path, "w") as file:
            file.write(filled)
    except Exception as e:
        print(f"Error writing to file path: {e}")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(
        f"Generating page from: {dir_path_content}\nto: {dest_dir_path}\n using {template_path} template"
    )
    source_dirs = os.listdir(dir_path_content)
    for dir in source_dirs:
        source_path = os.path.join(dir_path_content, dir)
        if os.path.isfile(source_path):
            dest_path_obj = pathlib.Path(os.path.join(dest_dir_path, dir))
            dest_new_file_path = dest_path_obj.with_suffix(".html")
            generate_page(source_path, template_path, dest_new_file_path)
        else:
            dest_subdir = os.path.join(dest_dir_path, dir)
            generate_pages_recursive(source_path, template_path, dest_subdir)
