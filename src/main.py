import os
import shutil

from generator import generate_page, generate_all
from textnode import TextNode, TextType

def main():
    copy_from_directory("static", "public")
    #page = generate_page("content/index.md", "template.html", "public/index.html")
    generate_all("content", "template.html", "public")



def copy_from_directory(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)
    if not os.path.exists(source):
        return
    for filename in os.listdir(source):
        if os.path.isfile(os.path.join(source, filename)):
            shutil.copy(os.path.join(source, filename), destination)
            with open("log.txt", "a") as f:
                f.write(f"Copied {filename} from {source} to {destination}\n")
        elif os.path.isdir(os.path.join(source, filename)):
            copy_from_directory(os.path.join(source, filename), os.path.join(destination, filename))

main()