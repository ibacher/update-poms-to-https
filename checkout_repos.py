from github3 import login, GitHub
from github3.exceptions import NotFoundError
import os
import sys
from time import sleep, time
from typing import List, AnyStr


def main(args: List[AnyStr]) -> None:
    if len(args) < 1:
        g = GitHub()

    try:
        g = login(token=args[0])
    except Exception:
        g = GitHub()

    omrs = g.organization("openmrs")
    repo_iter = omrs.repositories("public")
    for repo in repo_iter:
        try:
            repo.file_contents("pom.xml")
        except NotFoundError:
            continue

        repo.refresh()

        os.system(f"git clone --depth=1 {repo.git_url}")
        if g.ratelimit_remaining <= 1:
            sleep(repo_iter.last_response.headers["X-RateLimit-Reset"] - time())


if __name__ == "__main__":
    main(sys.argv[1:])
