import sys
import os
import shutil
from funct import generate_pages_recursive
def remove_all_files(directory):
    if os.path.exists(directory):
        print(f"🧹 Eliminando contenido en: {directory}")
        shutil.rmtree(directory)
    os.makedirs(directory)
    print(f"📁 Carpeta recreada: {directory}")

def copy_static(source, destination):
    if not os.path.exists(destination):
        os.makedirs(destination)

    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        dest_path = os.path.join(destination, item)

        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
            print(f"📄 Copiado archivo: {source_path} → {dest_path}")
        elif os.path.isdir(source_path):
            copy_static(source_path, dest_path)

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    static_dir = os.path.join(base_dir, "static")
    public_dir = os.path.join(base_dir, "docs")
    content_dir = os.path.join(base_dir, "content")
    template_path = os.path.join(base_dir, "template.html")

    remove_all_files(public_dir)
    copy_static(static_dir, public_dir)

    generate_pages_recursive(content_dir, template_path, public_dir,basepath )


if __name__ == "__main__":
    main()
