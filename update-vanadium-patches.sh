#!/bin/bash

gpwd=$(pwd)
readonly path="./vanadium_patches/"
readonly url=https://raw.githubusercontent.com/GrapheneOS/Vanadium/main/patches
patches=() # current patch names
smallpatches=() # truncated version of the patches for comparison
vpatches=() # vanadium patches
svpatches=() # truncated version for comparisons

# gets the current patches
get_patches() {
	cd $path
	patches=(*.patch)
	for ((i=0; i<${#patches[@]}; i++)); do
		smallpatches[$i]="${patches[$i]:4}"
	done
	cd $gpwd
}

# gets Vanadium patches by cloning the repository temporarily
get_vpatches() {
	cd uvp-tmp/
	retry=0
	while [ true ]; do
		git clone https://github.com/GrapheneOS/Vanadium.git
		if [ ! -d Vanadium/patches/ ]; then
			rm -rf Vanadium/
			echo "ERROR! git operation failed!"
			if [[ $retry > 0 ]]; then
				echo "Failed to clone $((retry+1)) times..."
			fi
			if [[ $retry == 2 ]]; then
				echo "Aborting!"
				cd $gpwd
				rm -rf uvp-tmp/
				exit 1
			fi
			echo "Retrying..."
			retry=$((retry+1))
		else
			break
		fi
	done
	cd Vanadium/patches/
	vpatches=(*.patch)
	for ((i=0; i<${#vpatches[@]}; i++)); do
		svpatches[$i]="${vpatches[$i]:4}"
	done
	cd $gpwd
}

update_patches() {
	get_patches
	get_vpatches
	cd $path
	counterU=0 # updated counter
	counterR=0 # removed counter
	counterNF=0 # not found counter, used to determine if it should be removed
	for ((i=0; i<${#smallpatches[@]}; i++)); do
		for ((j=0; j<${#svpatches[@]}; j++)); do
			if [[ "${svpatches[$j]}" == "${smallpatches[$i]}" ]]; then
				if [[ "${vpatches[$j]}" == "${patches[$i]}" ]]; then
					echo "Updating patch ${patches[$i]}"
					echo "	No name change"
				else
					echo "Updating patch ${patches[$i]}"
					echo "	Patch (would have been) renamed to: ${vpatches[$j]}"
				fi
				cp $gpwd/uvp-tmp/Vanadium/patches/${vpatches[$j]} ${patches[$i]}
				counterU=$((counterU+1))
			else
				counterNF=$((counterNF+1))
			fi
		done
		# Assume, since the patch has not been found, the patch has been removed
		if [[ $counterNF == ${#svpatches[@]} ]]; then
			echo "Removing ${patches[i]}"
			echo "	Patch has been removed in Vanadium"
			rm ${patches[$i]}
			counterR=$((counterR+1))
		fi
		counterNF=0
	done
	echo ""
	echo "Updated $counterU patches."
	echo "Removed $counterR patches."
	cd $gpwd
}

mkdir uvp-tmp/ # create a temporary directory for cloning the Vanadium patches
update_patches
rm -rf uvp-tmp/ # cleanup
exit 0
