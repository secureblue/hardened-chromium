#! /bin/bash -x

# Download this repo with its submodule https://src.fedoraproject.org/rpms/chromium.git inside the COPR build system
git clone --depth 1 --recurse-submodules https://github.com/wojnilowicz/ungoogled-chromium-copr.git
cd ungoogled-chromium-copr

# Download chromium-%{version}-clean.tar.xz from the Fedora's server
rpkg --path ./chromium sources

# Patch the spec file to build with the ungoogled-chromium patches
patch -d ./chromium -p1 < modify.patch

# Rename files that are called chromium-browser to ungoogled-chromium to avoid name clashes
patch -d ./chromium -p1 < rename.patch

# Move all the source files into the parent directory for the COPR build system to find them
mv ./chromium/* ../