#! /bin/bash -x

version="130.0.6723.58"

cd hardened-chromium

# copy Fedora patches to the build dir
cd fedora_patches/
patches=(*.patch)
for ((i=0; i<${#patches[@]}; i++)); do
	cp ${patches[i]} ../build/fedora-$((i+1000)).patch
done
cd ..

# copy Vanadium patches to the build dir
cd vanadium_patches/
patches=(*.patch)
for ((i=0; i<${#patches[@]}; i++)); do
	cp ${patches[i]} ../build/vanadium-$((i+2000)).patch
done
cd ..

# copy hardened-chromium patches to the build dir
cd patches/
patches=(*.patch)
for ((i=0; i<${#patches[@]}; i++)); do
	cp ${patches[i]} ../build/hardened-chromium-$((i+3000)).patch
done
cd ..

# download and clean chromium source
cd build
git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
export PATH="$(pwd)/depot_tools:$PATH"
mkdir chromium
cd chromium
fetch --nohooks --no-history chromium
cd src
gclient runhooks
git checkout "$version"

# clean
rm -rf ./build/linux/debian_bullseye_amd64-sysroot ./build/linux/debian_bullseye_i386-sysroot ./third_party/node/linux/node-linux-x64 ./third_party/rust-toolchain ./third_party/rust-src

./clean_ffmpeg.sh . 0
find ./third_party/openh264/src -type f -not -name '*.h' -delete

tar -cJf "chromium-$version-clean.tar.xz" .

cp chromium-*.tar.xz ../..
cd ../../..

# Move all the source files into the parent directory for the COPR build system to find them
mv ./build/* ../
