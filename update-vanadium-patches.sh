#!/bin/bash

repo_directory=$(pwd)
readonly patches_path="./vanadium_patches/"
readonly vanadium_url="https://github.com/GrapheneOS/Vanadium.git"
current_patches=()
truncated_patches=()
remote_patches=()
truncated_remote_patches=()

get_current_patches() {
	cd $patches_path
	current_patches=(*.patch)
	for ((i=0; i<${#current_patches[@]}; i++)); do
		truncated_patches[$i]="${current_patches[$i]:4}"
	done
	cd $repo_directory
}

get_remote_patches() {
	cd vanadium-patches-tmp/
	retry=0
	while [ true ]; do
		git clone $vanadium_url
		if [ ! -d Vanadium/patches/ ]; then
			rm -rf Vanadium/
			echo "ERROR! git operation failed!"
			if [[ $retry > 0 ]]; then
				echo "Failed to clone $((retry+1)) times..."
			fi
			if [[ $retry == 2 ]]; then
				echo "Aborting!"
				cd $repo_directory
				rm -rf vanadium-patches-tmp/
				exit 1
			fi
			echo "Retrying..."
			retry=$((retry+1))
		else
			break
		fi
	done
	cd Vanadium/patches/
	remote_patches=(*.patch)
	for ((i=0; i<${#remote_patches[@]}; i++)); do
		if [[ ${remote_patches[$i]} =~ ^[0-9]{4}[\-] ]]; then
			truncated_remote_patches[$i]="${remote_patches[$i]:4}"
		else
			echo "ERROR! Remote patch ${remote_patches[$i]} does match expected naming scheme!"
			echo "Aborting!"
			cd $repo_directory
			rm -rf vanadium-patches-tmp/
			exit 1
		fi
	done
	cd $repo_directory
}

update_patches() {
	get_current_patches
	get_remote_patches
	cd $patches_path
	updated_counter=0
	removed_counter=0
	patch_not_found_counter=0
	for ((i=0; i<${#truncated_patches[@]}; i++)); do
		for ((j=0; j<${#truncated_remote_patches[@]}; j++)); do
			if [[ "${truncated_remote_patches[$j]}" == "${truncated_patches[$i]}" ]]; then
				if [[ "${remote_patches[$j]}" == "${current_patches[$i]}" ]]; then
					echo "Updating patch ${current_patches[$i]}"
					echo "	No name change"
				else
					echo "Updating patch ${current_patches[$i]}"
					echo "	Patch renamed to: ${remote_patches[$j]}"
				fi
				rm ${current_patches[$i]}
				cp $repo_directory/vanadium-patches-tmp/Vanadium/patches/${remote_patches[$j]} ./
				updated_counter=$((updated_counter+1))
			else
				patch_not_found_counter=$((patch_not_found_counter+1))
			fi
		done
		# Assume, since the patch has not been found, the patch has been removed
		if [[ $patch_not_found_counter == ${#truncated_remote_patches[@]} ]]; then
			echo "Removing ${patches[i]}"
			echo "	Patch has been removed in Vanadium"
			rm ${patches[$i]}
			removed_counter=$((removed_counter+1))
		fi
		patch_not_found_counter=0
	done
	echo ""
	echo "Updated $updated_counter patches."
	echo "Removed $removed_counter patches."
	cd $repo_directory
}

mkdir vanadium-patches-tmp/ # create a temporary directory for cloning the Vanadium patches
update_patches
rm -rf vanadium-patches-tmp/ # cleanup
exit 0
