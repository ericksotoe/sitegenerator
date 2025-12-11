import sys

from copystatic import copy_directory_contents, generate_pages_recursive


def main():
    # default to root if no arg is passed
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    copy_directory_contents("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()
