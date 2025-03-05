from build_page import *

def main():
    copy_static_to_public()
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()