#! /bin/bash -x

version="129.0.6668.70"

git clone --depth 1 https://github.com/secureblue/hardened-chromium.git
cd hardened-chromium

# copy hardened-chromium patches to build
cd patches/
patches=(*.patch)
for ((i=0; i<${#patches[@]}; i++)); do
	cp ${patches[i]} ../build/hardened-chromium-$((i+2000)).patch
done
cd ..

# copy vanadium patches to build
cd vanadium_patches/
patches=(*.patch)
for ((i=0; i<${#patches[@]}; i++)); do
	cp ${patches[i]} ../build/vanadium-$((i+3000)).patch
done
cd ..

# copy fedora patches to the build dir
cp fedora_patches/*.patch ./build/

# download and clean chromium source
cd build
python3 ./chromium-latest.py --version $version --stable --ffmpegclean --ffmpegarm --cleansources
rm chromium-${version}.tar.xz
rm -rf ./chromium-${version}
cd ..

# Move all the source files into the parent directory for the COPR build system to find them
mv ./build/* ../
