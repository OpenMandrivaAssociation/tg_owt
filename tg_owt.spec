%global commit0 62321fd7128ab2650b459d4195781af8185e46b5
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date 20250603

%define major 0
%define libname %mklibname %{name}
%define oldlibname %mklibname %{name} 0
%define devname %mklibname -d %{name}

Name: tg_owt
Version: 0
Release: 4

# Main project - BSD
# abseil-cpp - ASL 2.0
# libsrtp - BSD
# libyuv - BSD
# pffft - BSD
# rnnoise - BSD
# usrsctp - BSD
License: BSD and ASL 2.0
Summary: WebRTC library for the Telegram messenger
URL: https://github.com/desktop-app/tg_owt
Source0: https://github.com/desktop-app/tg_owt/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz
#Source1: https://github.com/cisco/libsrtp/archive/refs/tags/v2.6.0.tar.gz

Patch1: https://github.com/desktop-app/tg_owt/pull/162.patch
Patch2: tg_owt-system-yuv.patch
Patch3: tg_owt-20211226-system-absl.patch
Patch4: https://github.com/desktop-app/tg_owt/pull/161.patch
#Patch5: https://github.com/desktop-app/tg_owt/pull/123.patch

BuildRequires: pkgconfig(alsa)
BuildRequires: pkgconfig(libavcodec)
BuildRequires: pkgconfig(libavformat)
BuildRequires: pkgconfig(libavutil)
BuildRequires: pkgconfig(libjpeg)
BuildRequires: pkgconfig(libpulse)
BuildRequires: pkgconfig(libswscale)
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(opus)
BuildRequires: pkgconfig(protobuf)
BuildRequires: pkgconfig(openh264)
BuildRequires: pkgconfig(vpx)
BuildRequires: pkgconfig(libyuv)
BuildRequires: pkgconfig(libevent)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xcomposite)
BuildRequires: pkgconfig(xdamage)
BuildRequires: pkgconfig(xext)
BuildRequires: pkgconfig(xfixes)
BuildRequires: pkgconfig(xrender)
BuildRequires: pkgconfig(xrandr)
BuildRequires: pkgconfig(xtst)
BuildRequires: pkgconfig(libpipewire-0.3)
BuildRequires: pkgconfig(gbm)
BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(gl)
BuildRequires: pkgconfig(egl)
BuildRequires: pkgconfig(libsrtp2)
BuildRequires: cmake(absl)
BuildRequires: cmake(Crc32c)

BuildRequires: cmake
BuildRequires: ninja
BuildRequires: yasm

%description
Special fork of the OpenWebRTC library for the Telegram messenger.

#################################################

%package -n %{libname}
Provides: bundled(base64) = 0~git
Provides: bundled(fft) = 0~git
Provides: bundled(fft4g) = 0~git
Provides: bundled(g711) = 0~git
Provides: bundled(g722) = 0~git
Provides: bundled(pffft) = 0~git483453d
Provides: bundled(portaudio) = 0~git
Provides: bundled(sigslot) = 0~git
Provides: bundled(spl_sqrt_floor) = 0~git
Provides: bundled(usrsctp) = 1.0.0~gitbee946a
Summary:	OpenWebRTC library for the Telegram messenger
Group:		System/Libraries
# Renamed 2025-02-26 before 6.0
%rename %{oldlibname}

%description -n %{libname}
%{summary}.

##################################################

%package -n %{devname}
Summary: Development files for %{name}
Requires: %{libname} = %{EVRD}
Requires: pkgconfig(alsa)
Requires: pkgconfig(libavcodec)
Requires: pkgconfig(libavformat)
Requires: pkgconfig(libavutil)
Requires: pkgconfig(libjpeg)
Requires: pkgconfig(libpulse)
Requires: pkgconfig(libswscale)
Requires: pkgconfig(openssl)
Requires: pkgconfig(opus)
Requires: pkgconfig(protobuf)
Requires: pkgconfig(openh264)
Requires: pkgconfig(vpx)
Requires: pkgconfig(libyuv)
Requires: pkgconfig(libevent)
Requires: pkgconfig(x11)
Requires: pkgconfig(xcomposite)
Requires: pkgconfig(xdamage)
Requires: pkgconfig(xext)
Requires: pkgconfig(xfixes)
Requires: pkgconfig(xrender)
Requires: pkgconfig(xrandr)
Requires: pkgconfig(xtst)
Requires: pkgconfig(libpipewire-0.3)
Requires: cmake(absl)

%description -n %{devname}
%{summary}.

%prep
%autosetup -n %{name}-%{commit0} -p1 
#-a 1
# Make sure nothing pulls in superfluous bundled libraries
rm -rf src/third_party/libvpx cmake/libvpx.cmake src/third_party/openh264 cmake/libopenh264.cmake src/third_party/libyuv cmake/libyuv.cmake src/third_party/abseil-cpp cmake/libabsl.cmake
#mv crc32c-*/* src/third_party/crc32c/src
#rm -rf crc32c-*
#rmdir src/third_party/libsrtp
#mv libsrtp-* src/third_party/libsrtp

%build
# CMAKE_BUILD_TYPE should always be Release due to some hardcoded checks.
CFLAGS="%{optflags} -DPROTOBUF_USE_DLLS" \
CPPFLAGS="-DPROTOBUF_USE_DLLS" \
CXXFLAGS="%{optflags} -std=gnu++20 -DPROTOBUF_USE_DLLS" \
LDFLAGS="%{optflags} -std=gnu++20 -DPROTOBUF_USE_DLLS" \
%cmake -G Ninja \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=ON \
	-DCMAKE_CXX_STANDARD=20 \
	-DTG_OWT_USE_PROTOBUF:BOOL=ON \
	-DTG_OWT_PACKAGED_BUILD:BOOL=ON \
	-DTG_OWT_BUILD_AUDIO_BACKENDS:BOOL=ON \
	-DTG_OWT_USE_PIPEWIRE:BOOL=ON

# Protobuf headers are generated correctly, but looked for in the wrong place
mkdir -p logging/rtc_event_log
ln -s ../../cmake/protobuf/rtc_event_log2.pb.h logging/rtc_event_log/

%ninja_build

%install
%ninja_install -C  build

%files -n %{libname}
%{_libdir}/lib%{name}.so.0*

%files -n %{devname}
%doc src/AUTHORS src/OWNERS
%license LICENSE src/PATENTS
%{_includedir}/%{name}
%{_libdir}/cmake/%{name}
%{_libdir}/lib%{name}.so
