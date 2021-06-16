import os
from xml.etree import ElementTree as ET
from urllib.parse import urlparse, urlunparse
import traceback


def update_urls(e: ET.Element) -> None:
    if e.text:
        result = urlparse(e.text)
        if result.hostname == "rubygems-proxy.torquebox.org":
            return

        path = result.path
        if len(path) > 0 and path[-1] == "/":
            path = path[0:-1]

        if result.hostname == "mavenrepo.openmrs.org":
            path = path.split("/")[-1]

        if result.scheme != "https":
            e.text = urlunparse(
                (
                    "https",
                    result[1],
                    path,
                    result[3],
                    result[4],
                    result[5],
                )
            )


def main():
    ET.register_namespace("", "http://maven.apache.org/POM/4.0.0")

    for entry in os.scandir(os.curdir):
        if entry.name[0] != "." and entry.is_dir():
            file_name = os.path.join(os.curdir, entry.name, "pom.xml")

            if not os.path.exists(file_name):
                continue

            print(f"Handling {entry.name}")

            try:
                pom = ET.parse(
                    file_name,
                    parser=ET.XMLParser(target=ET.TreeBuilder(insert_comments=True)),
                )

                for repo in pom.iter("{http://maven.apache.org/POM/4.0.0}repository"):
                    for e in repo.iter("{http://maven.apache.org/POM/4.0.0}url"):
                        update_urls(e)

                for repo in pom.iter(
                    "{http://maven.apache.org/POM/4.0.0}snapshotRepository"
                ):
                    for e in repo.iter("{http://maven.apache.org/POM/4.0.0}url"):
                        update_urls(e)

                for repo in pom.iter(
                    "{http://maven.apache.org/POM/4.0.0}pluginRepository"
                ):
                    for e in repo.iter("{http://maven.apache.org/POM/4.0.0}url"):
                        update_urls(e)

                with open(file_name, "w") as f:
                    print('<?xml version="1.0" encoding="UTF-8"?>', file=f)
                    pom.write(f, encoding="unicode")
                    print("", file=f)
            except Exception:
                traceback.print_exc()


if __name__ == "__main__":
    main()
