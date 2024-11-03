#! /bin/bash -x

version="130.0.6723.91"

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

# Move all the source files into the parent directory for the COPR build system to find them
mv ./build/* ../
cd ../
ln -s /usr/src/chromium/chromium-$version-clean.tar.xz chromium-$version-clean.tar.xz
