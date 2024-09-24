#! /bin/bash -x

version="129.0.6668.70"

# Download and enter this repo https://github.com/secureblue/hardened-chromium.git inside the COPR build system
git clone --depth 1 https://github.com/secureblue/hardened-chromium.git
cd hardened-chromium

# create prep dir
mkdir chromium

# copy hardened-chromium patches to chromium
cd patches/
patches=(*.patch)
for ((i=0; i<${#patches[@]}; i++)); do
	cp ${patches[i]} ../chromium/hardened-chromium-$((i+2000)).patch
done
cd ..

# copy vanadium patches to chromium
cd vanadium_patches/
patches=(*.patch)
for ((i=0; i<${#patches[@]}; i++)); do
	cp ${patches[i]} ../chromium/vanadium-$((i+3000)).patch
done
cd ..

# copy fedora patches to chromium
cp fedora_patches/*.patch ./chromium/

# download and clean chromium source
cd chromium
python3 chromium-latest.py --version $version --stable --ffmpegclean --ffmpegarm --cleansources
rm chromium-${version}.tar.xz
rm -rf ./chromium-${version}
cd ..

# Move all the source files into the parent directory for the COPR build system to find them
mv ./chromium/* ../
