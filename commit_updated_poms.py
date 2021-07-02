from git import Repo
import os


def main():
    for path in os.listdir(os.curdir):
        abs_path = os.path.join(os.curdir, path)
        if os.path.isdir(abs_path) and os.path.isdir(os.path.join(abs_path, ".git")):
            r = Repo(abs_path)
            diffs = r.head.commit.diff(None)
            if len(diffs) > 0:
                diff = diffs[0]
                if diff.change_type == "M" and diff.a_path == "pom.xml":
                    print(f"Handing {path}")
                    index = r.index
                    index.add(["pom.xml"])
                    index.commit(
                        "Updating repository URLs to HTTPS\n\n"
                        "For details on why this change is happening see this Talk post: "
                        "https://talk.openmrs.org/t/maven-3-8-1-and-http-repositories/33364\n\n"
                        "If this commit causes issues, please feel free to revert"
                    )
                    r.remote().push()


if __name__ == "__main__":
    main()
