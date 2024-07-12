#! /bin/bash -x

# Download this repo with its submodule https://src.fedoraproject.org/rpms/chromium.git inside the COPR build system
git clone --depth 1 --recurse-submodules https://github.com/qoijjj/chromium-copr-experimental.git
cd chromium-copr-experimental

# Download chromium-%{version}-clean.tar.xz from the Fedora's server
rpkg --path ./chromium sources

cp vanadium_patches/* ./chromium

# Patch the spec file to build with the hardening patches
patch -d ./chromium -p1 < hardening.patch

# Move all the source files into the parent directory for the COPR build system to find them
mv ./chromium/* ../
