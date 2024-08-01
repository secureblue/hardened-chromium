#! /bin/bash -x

# Download this repo with its submodule https://src.fedoraproject.org/rpms/chromium.git inside the COPR build system
git clone --depth 1 --recurse-submodules https://github.com/secureblue/hardened-chromium.git
cd hardened-chromium

cp vanadium_patches/* ./chromium
cp patches/* ./chromium

# Patch the spec file to build with the hardening patches
patch -d ./chromium -p1 < hardening.patch

cd chromium
python3 chromium-latest.py --version 127.0.6533.88 --stable --ffmpegclean --ffmpegarm --cleansources
cd ..

# Move all the source files into the parent directory for the COPR build system to find them
mv ./chromium/* ../
