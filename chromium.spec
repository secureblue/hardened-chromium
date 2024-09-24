%define _lto_cflags %{nil}
%global _default_patch_fuzz 2
%global numjobs %{_smp_build_ncpus}

# Fancy build status
%global build_target() \
	export NINJA_STATUS="[%2:%f/%t] " ; \
	ninja -j %{numjobs} -C '%1' '%2'

%global nodejs_version v20.6.1
%global esbuild_version 0.19.2
%global chromium_pybin %{__python3}
%global chromebuilddir out/Release
%global debug_package %{nil}
%global debug_level 0
%global chromium_channel %{nil}
%global chromium_menu_name Chromium
%global chromium_browser_channel chromium-browser%{chromium_channel}
%global chromium_path %{_libdir}/chromium-browser%{chromium_channel}

# To generate this list, go into %%{buildroot}%%{chromium_path} and run
# for i in `find . -name "*.so" | sort`; do NAME=`basename -s .so $i`; printf "$NAME|"; done
%global __provides_exclude_from ^(%{chromium_path}/.*\\.so|%{chromium_path}/.*\\.so.*)$
%global __requires_exclude ^(%{chromium_path}/.*\\.so|%{chromium_path}/.*\\.so.*)$


Name:	hardened-chromium%{chromium_channel}
Version: 129.0.6668.58
Release: 1%{?dist}
Summary: A WebKit (Blink) powered web browser that Google doesn't want you to use
Url: http://www.chromium.org/Home
License: BSD-3-Clause AND LGPL-2.1-or-later AND Apache-2.0 AND IJG AND MIT AND GPL-2.0-or-later AND ISC AND OpenSSL AND (MPL-1.1 OR GPL-2.0-only OR LGPL-2.0-only)

### Chromium Fedora Patches ###
Patch0: chromium-70.0.3538.67-sandbox-pie.patch

# Use /etc/chromium for initial_prefs
Patch1: chromium-115-initial_prefs-etc-path.patch

# debian patches
# disable font-test 
Patch20: chromium-disable-font-tests.patch
# don't download binary blob
Patch21: chromium-123-screen-ai-service.patch

# patch for using system brotli
Patch89: chromium-125-system-brotli.patch

# patch for using system opus
Patch91: chromium-108-system-opus.patch

# fix tab crash with SIGTRAP error when using system ffmpeg
Patch132: chromium-118-sigtrap_system_ffmpeg.patch
# disable FFmpegAllowLists by default to allow external ffmpeg
Patch134: chromium-125-disable-FFmpegAllowLists.patch
# revert, it causes build error: use of undeclared identifier 'AVFMT_FLAG_NOH264PARSE'            
Patch135: chromium-129-disable-H.264-video-parser-during-demuxing.patch            

# add correct path for Qt6Gui header and libs
Patch150: chromium-124-qt6.patch

# enable fstack-protector-strong
Patch312: chromium-123-fstack-protector-strong.patch

# add -ftrivial-auto-var-init=zero and -fwrapv
Patch316: chromium-122-clang-build-flags.patch

# set clang_lib path
Patch358: chromium-127-rust-clanglib.patch

# hardening patches
%{lua:
    rpm.execute("pwd")
    os.execute("echo 'Current home: $HOME'")
	if posix.getenv("HOME") == "/builddir" then
		hpatches = rpm.glob('/builddir/build/SOURCES/hardened-chromium-*.patch')
		vpatches = rpm.glob('/builddir/build/SOURCES/vanadium-*.patch')
	else
	    hpatches = rpm.glob(macros['_sourcedir']..'/hardened-chromium-*.patch')
		vpatches = rpm.glob(macros['_sourcedir']..'/vanadium-*.patch')
	end
	
	local count = 2000
    local printPatch = ""
	for p in ipairs(hpatches) do
        os.execute("echo 'Patching in "..hpatches[p].."'")
		printPatch = "Patch"..count..": hardened-chromium-"..count..".patch"
        rpm.execute("echo", printPatch)
		print(printPatch.."\n")
		count = count + 1
	end
	rpm.define("_hardeningPatchCount "..count-1)
	
	count = 3000
    printPatch = ""
	for p in ipairs(vpatches) do
        os.execute("echo 'Patching in "..vpatches[p].."'")
		printPatch = "Patch"..count..": vanadium-"..count..".patch"
        rpm.execute("echo", printPatch)
		print(printPatch.."\n")
		count = count + 1
	end
    rpm.define("_vanadiumPatchCount "..count-1)

	os.execute("echo 'Autopatch H: "..macros['_hardeningPatchCount'].."'")
    os.execute("echo 'Autopatch V: "..macros['_vanadiumPatchCount'].."'")
}

# Use chromium-latest.py to generate clean tarball from released build tarballs, found here:
# http://build.chromium.org/buildbot/official/
# For Chromium Fedora use chromium-latest.py --stable --ffmpegclean --ffmpegarm
# If you want to include the ffmpeg arm sources append the --ffmpegarm switch
# https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%%{version}.tar.xz
Source0: chromium-%{version}-clean.tar.xz
Source1: README.fedora
Source2: chromium.conf
Source3: chromium-browser.sh
Source4: %{chromium_browser_channel}.desktop
Source5: clean_ffmpeg.sh
Source6: chromium-latest.py
Source9: chromium-browser.xml
Source11: master_preferences

BuildRequires: golang-github-evanw-esbuild
BuildRequires: clang
BuildRequires: clang-tools-extra
BuildRequires: llvm
BuildRequires: lld
BuildRequires: rustc
BuildRequires: bindgen-cli
BuildRequires: libzstd-devel
BuildRequires: pkgconfig(libavcodec)
BuildRequires: pkgconfig(libavfilter)
BuildRequires: pkgconfig(libavformat)
BuildRequires: pkgconfig(libavutil)
Conflicts: libavformat-free%{_isa} < 6.0.1
Conflicts: ffmpeg-libs%{_isa} < 6.0.1-2
BuildRequires: pkgconfig(openh264)
BuildRequires:	alsa-lib-devel
BuildRequires:	atk-devel
BuildRequires:	bison
BuildRequires:	cups-devel
BuildRequires:	dbus-devel
BuildRequires:	desktop-file-utils
BuildRequires:	expat-devel
BuildRequires:	flex
BuildRequires:	fontconfig-devel
BuildRequires:	glib2-devel
BuildRequires:	glibc-devel
BuildRequires:	gperf
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: pkgconfig(Qt5Widgets)
BuildRequires: pkgconfig(Qt6Core)
BuildRequires: pkgconfig(Qt6Widgets)
BuildRequires: compiler-rt
BuildRequires:	harfbuzz-devel >= 2.4.0
BuildRequires: libatomic
BuildRequires:	libcap-devel
BuildRequires:	libcurl-devel
BuildRequires:	libdrm-devel
BuildRequires:	libgcrypt-devel
BuildRequires:	libudev-devel
BuildRequires:	libuuid-devel
BuildRequires:	libusb-compat-0.1-devel
BuildRequires:	libutempter-devel
BuildRequires:	libXdamage-devel
BuildRequires:	libXtst-devel
BuildRequires:	xcb-proto
BuildRequires:	mesa-libgbm-devel
BuildRequires: nodejs
BuildRequires: gn
BuildRequires:	nss-devel >= 3.26
BuildRequires:	pciutils-devel
BuildRequires:	pulseaudio-libs-devel
BuildRequires:	pipewire-devel
BuildRequires: libappstream-glib

# Fedora tries to use system libs whenever it can.
BuildRequires:	bzip2-devel
BuildRequires:	dbus-glib-devel
# For eu-strip
BuildRequires:	elfutils
BuildRequires:	elfutils-libelf-devel
BuildRequires:	flac-devel
BuildRequires:	freetype-devel
BuildRequires: google-crc32c-devel
BuildRequires: libdav1d-devel
BuildRequires: highway-devel
BuildRequires: libsecret-devel
BuildRequires: double-conversion-devel
BuildRequires: libXNVCtrl-devel
# One of the python scripts invokes git to look for a hash. So helpful.
BuildRequires:	/usr/bin/git
BuildRequires:	hwdata
BuildRequires:	kernel-headers
BuildRequires:	libevent-devel
BuildRequires:	libffi-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires: openjpeg2-devel
BuildRequires: lcms2-devel
BuildRequires: libtiff-devel
BuildRequires:	libudev-devel
Requires: libusbx >= 1.0.21-0.1.git448584a
BuildRequires: libusbx-devel >= 1.0.21-0.1.git448584a
BuildRequires:	libva-devel
BuildRequires:	libwebp-devel
BuildRequires:	libxslt-devel
BuildRequires:	libxshmfence-devel
BuildRequires:	mesa-libGL-devel
BuildRequires:	opus-devel
BuildRequires: %{chromium_pybin}
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires: python3-jinja2
BuildRequires: brotli-devel
BuildRequires: speech-dispatcher-devel
BuildRequires: yasm
BuildRequires: zlib-devel
BuildRequires:	systemd
BuildRequires: ninja-build
BuildRequires: libevdev-devel

Requires: nss%{_isa} >= 3.26
Requires: nss-mdns%{_isa}
Requires: libcanberra-gtk3%{_isa}
Requires: u2f-hidraw-policy
Requires: hardened-chromium-common%{_isa} = %{version}-%{release}

ExclusiveArch: x86_64

Provides: bundled(angle) = 2422
Provides: bundled(bintrees) = 1.0.1
Provides: bundled(boringssl)
Provides: bundled(bspatch)
Provides: bundled(cacheinvalidation) = 20150720
Provides: bundled(colorama) = 799604a104
Provides: bundled(crashpad)
Provides: bundled(dmg_fp)
Provides: bundled(expat) = 2.2.0
Provides: bundled(fdmlibm) = 5.3
Provides: bundled(libaom)
Provides: bundled(fips181) = 2.2.3
Provides: bundled(gperftools) = svn144
Provides: bundled(hunspell) = 1.6.0
Provides: bundled(iccjpeg)
Provides: bundled(icu) = 58.1
Provides: bundled(kitchensink) = 1
Provides: bundled(leveldb) = 1.20
Provides: bundled(libaddressinput) = 0
Provides: bundled(libevent) = 1.4.15
Provides: bundled(libjingle) = 9564
Provides: bundled(libphonenumber) = a4da30df63a097d67e3c429ead6790ad91d36cf4
Provides: bundled(libsrtp) = 2cbd85085037dc7bf2eda48d4cf62e2829056e2d
Provides: bundled(libvpx) = 1.6.0
Provides: bundled(libyuv) = 1651
Provides: bundled(lzma) = 15.14
Provides: bundled(libudis86) = 1.7.1
Provides: bundled(mesa) = 9.0.3
Provides: bundled(NSBezierPath) = 1.0
Provides: bundled(mozc)
Provides: bundled(ots) = 8d70cffebbfa58f67a5c3ed0e9bc84dccdbc5bc0
Provides: bundled(protobuf) = 3.0.0.beta.3
Provides: bundled(qcms) = 4
Provides: bundled(re2)
Provides: bundled(sfntly) = 04740d2600193b14aa3ef24cd9fbb3d5996b9f77
Provides: bundled(skia)
Provides: bundled(SMHasher) = 0
Provides: bundled(snappy) = 1.1.4-head
Provides: bundled(speech-dispatcher) = 0.7.1
Provides: bundled(sqlite) = 3.17patched
Provides: bundled(superfasthash) = 0
Provides: bundled(talloc) = 2.0.1
Provides: bundled(usrsctp) = 0
Provides: bundled(v8) = 5.9.211.31
Provides: bundled(webrtc) = 90usrsctp
Provides: bundled(woff2) = 445f541996fe8376f3976d35692fd2b9a6eedf2d
Provides: bundled(xdg-mime)
Provides: bundled(xdg-user-dirs)

# For selinux scriptlet
Requires(post): /usr/sbin/semanage
Requires(post): /usr/sbin/restorecon

%description
Chromium is an open-source web browser, powered by WebKit (Blink).

%package common
Summary: Files needed for both the headless_shell and full Chromium
%description common
%{summary}.

%package qt5-ui
Summary: Qt5 UI built from Chromium
Requires: hardened-chromium%{_isa} = %{version}-%{release}

%description qt5-ui
Qt5 UI for chromium.

%package qt6-ui
Summary: Qt6 UI built from Chromium
Requires: hardened-chromium%{_isa} = %{version}-%{release}

%description qt6-ui
Qt6 UI for chromium.

%prep
%setup -q -n chromium-%{version}

### Chromium Fedora Patches ###
%patch -P0 -p1 -b .sandboxpie
%patch -P1 -p1 -b .etc
%patch -P20 -p1 -b .disable-font-test
%patch -P21 -p1 -b .screen-ai-service
%patch -P89 -p1 -b .system-brotli
%patch -P91 -p1 -b .system-opus
%patch -P132 -p1 -b .sigtrap_system_ffmpeg
%patch -P134 -p1 -b .disable-FFmpegAllowLists
%patch -P135 -p1 -b .disable-H.264-video-parser-during-demuxing
%patch -P150 -p1 -b .qt6
%patch -P312 -p1 -b .fstack-protector-strong
%patch -P316 -p1 -b .clang-build-flags
%patch -P358 -p1 -b .rust-clang_lib

%autopatch -p1 -m 2000 -M %{_hardeningPatchCount}
%autopatch -p1 -m 3000 -M %{_vanadiumPatchCount}

# Change shebang in all relevant files in this directory and all subdirectories
# See `man find` for how the `-exec command {} +` syntax works
find -type f \( -iname "*.py" \) -exec sed -i '1s=^#! */usr/bin/\(python\|env python\)[23]\?=#!%{chromium_pybin}=' {} +

# Add correct path for nodejs binary
mkdir -p third_party/node/linux/node-linux-x64/bin
ln -s %{_bindir}/node third_party/node/linux/node-linux-x64/bin/node

# Get rid of the bundled esbuild
ln -sf %{_bindir}/esbuild third_party/devtools-frontend/src/third_party/esbuild/esbuild

# Get rid of the pre-built eu-strip binary, it is x86_64 and of mysterious origin
rm -rf buildtools/third_party/eu-strip/bin/eu-strip
  
# Replace it with a symlink to the Fedora copy
ln -s %{_bindir}/eu-strip buildtools/third_party/eu-strip/bin/eu-strip

rm -rf third_party/libusb/src/libusb/libusb.h
# we _shouldn't need to do this, but it looks like we do.
cp -a %{_includedir}/libusb-1.0/libusb.h third_party/libusb/src/libusb/libusb.h

# Hard code extra version
sed -i 's/getenv("CHROME_VERSION_EXTRA")/"hardened-chromium"/' chrome/common/channel_info_posix.cc

# bz#2265957, add correct platform
sed -i "s/Linux x86_64/Linux %{_arch}/" content/common/user_agent.cc

cp -a third_party/dav1d/version/version.h third_party/dav1d/libdav1d/include/dav1d/

%build

# reduce warnings
FLAGS=' -Wno-deprecated-declarations -Wno-unknown-warning-option -Wno-unused-command-line-argument'
FLAGS+=' -Wno-unused-but-set-variable -Wno-unused-result -Wno-unused-function -Wno-unused-variable'
FLAGS+=' -Wno-unused-const-variable -Wno-unneeded-internal-declaration -Wno-unknown-attributes -Wno-unknown-pragmas'

CFLAGS="$FLAGS"
CXXFLAGS="$FLAGS"

# reduce the size of relocations
LDFLAGS="$LDFLAGS -Wl,-z,pack-relative-relocs"
RUSTFLAGS=${RUSTFLAGS/--cap-lints/-Clink-arg=-Wl,-z,pack-relative-relocs --cap-lints}
RUSTFLAGS=${RUSTFLAGS/debuginfo=?/debuginfo=0}

export CC=clang
export CXX=clang++
export AR=llvm-ar
export NM=llvm-nm
export READELF=llvm-readelf
export CFLAGS
export CXXFLAGS
export LDFLAGS
export RUSTFLAGS

export RUSTC_BOOTSTRAP=1
rustc_version="$(rustc --version)"
rust_bindgen_root="%{_prefix}"

# set clang version
clang_version="$(clang --version | sed -n 's/clang version //p' | cut -d. -f1)"
clang_base_path="$(clang --version | grep InstalledDir | cut -d' ' -f2 | sed 's#/bin##')"

CHROMIUM_GN_DEFINES=""
CHROMIUM_GN_DEFINES+=' custom_toolchain="//build/toolchain/linux/unbundle:default"'
CHROMIUM_GN_DEFINES+=' host_toolchain="//build/toolchain/linux/unbundle:default"'
CHROMIUM_GN_DEFINES+=' is_debug=false dcheck_always_on=false dcheck_is_configurable=false'
CHROMIUM_GN_DEFINES+=' enable_nacl=false'
CHROMIUM_GN_DEFINES+=' system_libdir="%{_lib}"'
CHROMIUM_GN_DEFINES+=' is_official_build=true'
sed -i 's|OFFICIAL_BUILD|GOOGLE_CHROME_BUILD|g' tools/generate_shim_headers/generate_shim_headers.py
CHROMIUM_GN_DEFINES+=' chrome_pgo_phase=0'
CHROMIUM_GN_DEFINES+=' is_cfi=true use_thin_lto=true'
CHROMIUM_GN_DEFINES+=' enable_reporting=false'
CHROMIUM_GN_DEFINES+=' enable_remoting=false'
CHROMIUM_GN_DEFINES+=' is_clang=true'
CHROMIUM_GN_DEFINES+=" clang_base_path=\"$clang_base_path\""
CHROMIUM_GN_DEFINES+=" clang_version=\"$clang_version\""
CHROMIUM_GN_DEFINES+=' clang_use_chrome_plugins=false'
CHROMIUM_GN_DEFINES+=' use_lld=true'
CHROMIUM_GN_DEFINES+=' rust_sysroot_absolute="%{_prefix}"'
CHROMIUM_GN_DEFINES+=" rust_bindgen_root=\"$rust_bindgen_root\""
CHROMIUM_GN_DEFINES+=" rustc_version=\"$rustc_version\""
CHROMIUM_GN_DEFINES+=' use_sysroot=false'
CHROMIUM_GN_DEFINES+=' icu_use_data_file=true'
CHROMIUM_GN_DEFINES+=' target_os="linux"'
CHROMIUM_GN_DEFINES+=' current_os="linux"'
CHROMIUM_GN_DEFINES+=' treat_warnings_as_errors=false'
CHROMIUM_GN_DEFINES+=' enable_iterator_debugging=false'
CHROMIUM_GN_DEFINES+=' enable_vr=false'
CHROMIUM_GN_DEFINES+=' enable_arcore=false'
CHROMIUM_GN_DEFINES+=' enable_openxr=false'
CHROMIUM_GN_DEFINES+=' enable_cardboard=false'
CHROMIUM_GN_DEFINES+=' build_dawn_tests=false enable_perfetto_unittests=false'
CHROMIUM_GN_DEFINES+=' disable_fieldtrial_testing_config=true'
CHROMIUM_GN_DEFINES+=' symbol_level=%{debug_level} blink_symbol_level=%{debug_level}'
CHROMIUM_GN_DEFINES+=' angle_has_histograms=false'
CHROMIUM_GN_DEFINES+=' safe_browsing_use_unrar=false'
CHROMIUM_GN_DEFINES+=' ffmpeg_branding="Chrome" proprietary_codecs=true is_component_ffmpeg=true enable_ffmpeg_video_decoders=true media_use_ffmpeg=true'
CHROMIUM_GN_DEFINES+=' media_use_openh264=true'
CHROMIUM_GN_DEFINES+=' rtc_use_h264=true'
CHROMIUM_GN_DEFINES+=' use_kerberos=true'
CHROMIUM_GN_DEFINES+=' use_qt=true moc_qt5_path="%{_libdir}/qt5/bin/"'
CHROMIUM_GN_DEFINES+=' use_qt6=true moc_qt6_path="%{_libdir}/qt6/libexec/"'
CHROMIUM_GN_DEFINES+=' use_gio=true use_pulseaudio=true'
CHROMIUM_GN_DEFINES+=' enable_widevine=false'
CHROMIUM_GN_DEFINES+=' use_vaapi=true'
CHROMIUM_GN_DEFINES+=' rtc_use_pipewire=true rtc_link_pipewire=true'
CHROMIUM_GN_DEFINES+=' use_system_libjpeg=true'
CHROMIUM_GN_DEFINES+=' use_system_libpng=true'
CHROMIUM_GN_DEFINES+=' use_system_libopenjpeg2=true'
CHROMIUM_GN_DEFINES+=' use_system_lcms2=true'
CHROMIUM_GN_DEFINES+=' use_system_libtiff=true'
CHROMIUM_GN_DEFINES+=' use_system_libffi=true'
export CHROMIUM_GN_DEFINES

# use system libraries
system_libs=()
system_libs+=(brotli)
system_libs+=(crc32c)
system_libs+=(dav1d)
system_libs+=(highway)
system_libs+=(fontconfig)
system_libs+=(ffmpeg)
system_libs+=(freetype)
system_libs+=(harfbuzz-ng)
system_libs+=(libdrm)
system_libs+=(libevent)
system_libs+=(libjpeg)
system_libs+=(libpng)
system_libs+=(libusb)
system_libs+=(libwebp)
system_libs+=(libxml)
system_libs+=(libxslt)
system_libs+=(opus)
system_libs+=(double-conversion)
system_libs+=(libsecret)
system_libs+=(libXNVCtrl)
system_libs+=(flac)
system_libs+=(zstd)
system_libs+=(openh264)

build/linux/unbundle/replace_gn_files.py --system-libraries ${system_libs[@]}

# Check that there is no system 'google' module, shadowing bundled ones:
if python3 -c 'import google ; print google.__path__' 2> /dev/null ; then \
    echo "Python 3 'google' module is defined, this will shadow modules of this build"; \
    exit 1 ; \
fi

mkdir -p %{chromebuilddir} && cp -a %{_bindir}/gn %{chromebuilddir}/

%{chromebuilddir}/gn --script-executable=%{chromium_pybin} gen --args="$CHROMIUM_GN_DEFINES" %{chromebuilddir}

%build_target %{chromebuilddir} chrome
%build_target %{chromebuilddir} chrome_sandbox
%build_target %{chromebuilddir} policy_templates

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir} \
         %{buildroot}%{chromium_path}/locales \
         %{buildroot}%{_sysconfdir}/chromium

# install system wide chromium config
cp -a %{SOURCE2} %{buildroot}%{_sysconfdir}/chromium/chromium.conf
cp -a %{SOURCE3} %{buildroot}%{chromium_path}/%{chromium_browser_channel}.sh

export BUILD_TARGET=`cat /etc/redhat-release`
export CHROMIUM_PATH=%{chromium_path}
export CHROMIUM_BROWSER_CHANNEL=%{chromium_browser_channel}

sed -i "s|@@BUILD_TARGET@@|$BUILD_TARGET|g" %{buildroot}%{chromium_path}/%{chromium_browser_channel}.sh
sed -i "s|@@CHROMIUM_PATH@@|$CHROMIUM_PATH|g" %{buildroot}%{chromium_path}/%{chromium_browser_channel}.sh
sed -i "s|@@CHROMIUM_BROWSER_CHANNEL@@|$CHROMIUM_BROWSER_CHANNEL|g" %{buildroot}%{chromium_path}/%{chromium_browser_channel}.sh

ln -s ../..%{chromium_path}/%{chromium_browser_channel}.sh %{buildroot}%{_bindir}/%{chromium_browser_channel}
mkdir -p %{buildroot}%{_mandir}/man1/

pushd %{chromebuilddir}
	cp -a icudtl.dat %{buildroot}%{chromium_path}
	cp -a chrom*.pak resources.pak %{buildroot}%{chromium_path}
	cp -a locales/*.pak %{buildroot}%{chromium_path}/locales/
  cp -a libvk_swiftshader.so %{buildroot}%{chromium_path}
  cp -a libvulkan.so.1 %{buildroot}%{chromium_path}
  cp -a vk_swiftshader_icd.json %{buildroot}%{chromium_path}
	cp -a chrome %{buildroot}%{chromium_path}/%{chromium_browser_channel}
	cp -a chrome_sandbox %{buildroot}%{chromium_path}/chrome-sandbox
	cp -a chrome_crashpad_handler %{buildroot}%{chromium_path}/chrome_crashpad_handler
	cp -a ../../chrome/app/resources/manpage.1.in %{buildroot}%{_mandir}/man1/%{chromium_browser_channel}.1
	sed -i "s|@@PACKAGE@@|%{chromium_browser_channel}|g" %{buildroot}%{_mandir}/man1/%{chromium_browser_channel}.1
	sed -i "s|@@MENUNAME@@|%{chromium_menu_name}|g" %{buildroot}%{_mandir}/man1/%{chromium_browser_channel}.1

	# V8 initial snapshots
	# https://code.google.com/p/chromium/issues/detail?id=421063
	cp -a v8_context_snapshot.bin %{buildroot}%{chromium_path}

	# This is ANGLE, not to be confused with the similarly named files under swiftshader/
	cp -a libEGL.so libGLESv2.so %{buildroot}%{chromium_path}
  cp -a libqt5_shim.so %{buildroot}%{chromium_path}
  cp -a libqt6_shim.so %{buildroot}%{chromium_path}
popd

pushd %{buildroot}%{chromium_path}/
for f in *.so *.so.1 chrome_crashpad_handler chrome-sandbox chromium-browser headless_shell chromedriver ; do
   [ -f $f ] && strip $f
done
popd

# Add directories for policy management
mkdir -p %{buildroot}%{_sysconfdir}/chromium/policies/managed
mkdir -p %{buildroot}%{_sysconfdir}/chromium/policies/recommended

cp -a out/Release/gen/chrome/app/policy/common/html/en-US/*.html .
cp -a out/Release/gen/chrome/app/policy/linux/examples/chrome.json .

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
cp -a chrome/app/theme/chromium/product_logo_256.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{chromium_browser_channel}.png
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
cp -a chrome/app/theme/chromium/product_logo_128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{chromium_browser_channel}.png
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/64x64/apps
cp -a chrome/app/theme/chromium/product_logo_64.png %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{chromium_browser_channel}.png
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/48x48/apps
cp -a chrome/app/theme/chromium/product_logo_48.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{chromium_browser_channel}.png
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/24x24/apps
cp -a chrome/app/theme/chromium/product_logo_24.png %{buildroot}%{_datadir}/icons/hicolor/24x24/apps/%{chromium_browser_channel}.png

# Install the master_preferences file
install -m 0644 %{SOURCE11} %{buildroot}%{_sysconfdir}/chromium/

mkdir -p %{buildroot}%{_datadir}/applications/
desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE4}

install -D -m0644 chrome/installer/linux/common/chromium-browser/chromium-browser.appdata.xml \
  ${RPM_BUILD_ROOT}%{_datadir}/metainfo/%{chromium_browser_channel}.appdata.xml
appstream-util validate-relax --nonet ${RPM_BUILD_ROOT}%{_datadir}/metainfo/%{chromium_browser_channel}.appdata.xml

mkdir -p %{buildroot}%{_datadir}/gnome-control-center/default-apps/
cp -a %{SOURCE9} %{buildroot}%{_datadir}/gnome-control-center/default-apps/

# README.fedora
cp %{SOURCE1} .

%post
# Set SELinux labels - semanage itself will adjust the lib directory naming
# But only do it when selinux is enabled, otherwise, it gets noisy.
if selinuxenabled; then
	semanage fcontext -a -t bin_t /usr/lib/%{chromium_browser_channel} &>/dev/null || :
	semanage fcontext -a -t bin_t /usr/lib/%{chromium_browser_channel}/%{chromium_browser_channel}.sh &>/dev/null || :
	semanage fcontext -a -t chrome_sandbox_exec_t /usr/lib/chrome-sandbox &>/dev/null || :
	restorecon -R -v %{chromium_path}/%{chromium_browser_channel} &>/dev/null || :
fi

%files
%doc AUTHORS README.fedora
%doc chrome_policy_list.html *.json
%license LICENSE
%config(noreplace) %{_sysconfdir}/chromium/chromium.conf
%config %{_sysconfdir}/chromium/master_preferences
%config %{_sysconfdir}/chromium/policies/
%{_bindir}/%{chromium_browser_channel}
%{chromium_path}/*.bin
%{chromium_path}/chrome_*.pak
%{chromium_path}/chrome_crashpad_handler
%{chromium_path}/resources.pak
%{chromium_path}/%{chromium_browser_channel}
%{chromium_path}/%{chromium_browser_channel}.sh
%attr(4755, root, root) %{chromium_path}/chrome-sandbox
%{_mandir}/man1/%{chromium_browser_channel}.*
%{_datadir}/icons/hicolor/*/apps/%{chromium_browser_channel}.png
%{_datadir}/applications/*.desktop
%{_datadir}/metainfo/*.appdata.xml
%{_datadir}/gnome-control-center/default-apps/chromium-browser.xml

%files qt5-ui
%{chromium_path}/libqt5_shim.so

%files qt6-ui
%{chromium_path}/libqt6_shim.so

%files common
%{chromium_path}/libvk_swiftshader.so*
%{chromium_path}/libvulkan.so*
%{chromium_path}/vk_swiftshader_icd.json
%{chromium_path}/libEGL.so*
%{chromium_path}/libGLESv2.so*
%{chromium_path}/icudtl.dat
%dir %{chromium_path}/
%dir %{chromium_path}/locales/
%lang(af) %{chromium_path}/locales/af.pak
%lang(am) %{chromium_path}/locales/am.pak
%lang(ar) %{chromium_path}/locales/ar.pak
%lang(bg) %{chromium_path}/locales/bg.pak
%lang(bn) %{chromium_path}/locales/bn.pak
%lang(ca) %{chromium_path}/locales/ca.pak
%lang(cs) %{chromium_path}/locales/cs.pak
%lang(da) %{chromium_path}/locales/da.pak
%lang(de) %{chromium_path}/locales/de.pak
%lang(el) %{chromium_path}/locales/el.pak
%lang(en_GB) %{chromium_path}/locales/en-GB.pak
# Chromium _ALWAYS_ needs en-US.pak as a fallback
# This means we cannot apply the lang code here.
# Otherwise, it is filtered out on install.
%{chromium_path}/locales/en-US.pak
%lang(es) %{chromium_path}/locales/es.pak
%lang(es) %{chromium_path}/locales/es-419.pak
%lang(et) %{chromium_path}/locales/et.pak
%lang(fa) %{chromium_path}/locales/fa.pak
%lang(fi) %{chromium_path}/locales/fi.pak
%lang(fil) %{chromium_path}/locales/fil.pak
%lang(fr) %{chromium_path}/locales/fr.pak
%lang(gu) %{chromium_path}/locales/gu.pak
%lang(he) %{chromium_path}/locales/he.pak
%lang(hi) %{chromium_path}/locales/hi.pak
%lang(hr) %{chromium_path}/locales/hr.pak
%lang(hu) %{chromium_path}/locales/hu.pak
%lang(id) %{chromium_path}/locales/id.pak
%lang(it) %{chromium_path}/locales/it.pak
%lang(ja) %{chromium_path}/locales/ja.pak
%lang(kn) %{chromium_path}/locales/kn.pak
%lang(ko) %{chromium_path}/locales/ko.pak
%lang(lt) %{chromium_path}/locales/lt.pak
%lang(lv) %{chromium_path}/locales/lv.pak
%lang(ml) %{chromium_path}/locales/ml.pak
%lang(mr) %{chromium_path}/locales/mr.pak
%lang(ms) %{chromium_path}/locales/ms.pak
%lang(nb) %{chromium_path}/locales/nb.pak
%lang(nl) %{chromium_path}/locales/nl.pak
%lang(pl) %{chromium_path}/locales/pl.pak
%lang(pt_BR) %{chromium_path}/locales/pt-BR.pak
%lang(pt_PT) %{chromium_path}/locales/pt-PT.pak
%lang(ro) %{chromium_path}/locales/ro.pak
%lang(ru) %{chromium_path}/locales/ru.pak
%lang(sk) %{chromium_path}/locales/sk.pak
%lang(sl) %{chromium_path}/locales/sl.pak
%lang(sr) %{chromium_path}/locales/sr.pak
%lang(sv) %{chromium_path}/locales/sv.pak
%lang(sw) %{chromium_path}/locales/sw.pak
%lang(ta) %{chromium_path}/locales/ta.pak
%lang(te) %{chromium_path}/locales/te.pak
%lang(th) %{chromium_path}/locales/th.pak
%lang(tr) %{chromium_path}/locales/tr.pak
%lang(uk) %{chromium_path}/locales/uk.pak
%lang(ur) %{chromium_path}/locales/ur.pak
%lang(vi) %{chromium_path}/locales/vi.pak
%lang(zh_CN) %{chromium_path}/locales/zh-CN.pak
%lang(zh_TW) %{chromium_path}/locales/zh-TW.pak