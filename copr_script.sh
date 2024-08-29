#! /bin/bash -x

# Download this repo with its submodule https://github.com/secureblue/hardened-chromium.git inside the COPR build system
git clone --depth 1 --recurse-submodules https://github.com/secureblue/hardened-chromium.git
cd hardened-chromium

cd patches/
patches=(*.patch)
for ((i=0; i<${#patches[@]}; i++)); do
	cp ${patches[i]} ../chromium/hardened-chromium-$((i+2000)).patch
done
cd ..
cd vanadium_patches/
patches=(*.patch)
for ((i=0; i<${#patches[@]}; i++)); do
	cp ${patches[i]} ../chromium/vanadium-$((i+3000)).patch
done
cd ..

version="128.0.6613.113"

cd chromium
python3 chromium-latest.py --version $version --stable --ffmpegclean --ffmpegarm --cleansources
rm chromium-${version}.tar.xz
rm -rf ./chromium-${version}
cd ..

# Move all the source files into the parent directory for the COPR build system to find them
mv ./chromium/* ../
