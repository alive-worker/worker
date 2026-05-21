#!/bin/sh
# Build the Trae-ready notebox image on Linux/macOS/WSL.
#
# Usage:
#   ./build.sh                              # build image "notebox-trae"
#   IMAGE=my-name ./build.sh                # custom image name
#   HTTP_PROXY=http://host:port HTTPS_PROXY=http://host:port ./build.sh
#
# Steps: materialise ../repo.zip into ./repo/, then `docker build`.
set -eu

IMAGE="${IMAGE:-notebox-trae}"
here="$(cd "$(dirname "$0")" && pwd)"
cd "$here"

zip="../repo.zip"
[ -f "$zip" ] || { echo "repo.zip not found at $zip" >&2; exit 1; }

echo "[build] materialising repo/ from $zip"
rm -rf repo
mkdir -p repo
if command -v unzip >/dev/null 2>&1; then
    unzip -q "$zip" -d repo
else
    python3 -c "import zipfile,sys; zipfile.ZipFile('$zip').extractall('repo')"
fi

set -- build -t "$IMAGE"
[ -n "${HTTP_PROXY:-}" ]  && set -- "$@" --build-arg "HTTP_PROXY=$HTTP_PROXY"
[ -n "${HTTPS_PROXY:-}" ] && set -- "$@" --build-arg "HTTPS_PROXY=$HTTPS_PROXY"
set -- "$@" .

echo "[build] docker $*"
docker "$@"

echo
echo "[build] done. Start it with:"
echo "    docker run -d -p 2222:22 --name notebox $IMAGE"
