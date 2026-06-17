%{!?upstream_version:%{error:upstream_version must be defined, e.g. rpmbuild --define 'upstream_version <version>'}}

%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers
%global oldname xorg-x11-drv-intel
%global reponame xf86-video-intel
%define _disable_source_fetch 0

%undefine _hardened_build

Summary:   XLibre intel X11 video driver
Name:      xlibre-xf86-video-intel
Version:   %{upstream_version}
Release:   1%{?dist}
URL:       https://github.com/X11Libre/%{reponame}
License:   MIT

Source0:   https://github.com/X11Libre/%{reponame}/archive/refs/tags/%{name}-%{version}.tar.gz

Patch0:	    intel-gcc-pr65873.patch
# https://bugs.freedesktop.org/show_bug.cgi?id=96255#c11
Patch1:     0001-sna-Avoid-clobbering-output-physical-size-with-xf86O.patch
Patch2:     intel-meson-has-present.patch


ExclusiveArch: %{ix86} x86_64 x86_64_v2

BuildRequires:  cairo-devel
BuildRequires:  gcc
BuildRequires:  kernel-headers
BuildRequires:  libXfont2-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXv-devel
BuildRequires:  make
BuildRequires:  mesa-libGL-devel >= 6.5-9
BuildRequires:  meson
BuildRequires:  pkgconfig(libdrm) >= 2.4.20
BuildRequires:  pkgconfig(libdrm_intel) >= 2.4.52
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(pciaccess) >= 0.10
BuildRequires:  pkgconfig(pixman-1) >= 0.27.1
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(x11-xcb)
BuildRequires:  pkgconfig(xcb-aux)
BuildRequires:  pkgconfig(xcb-dri3)
BuildRequires:  pkgconfig(xcb-present)
BuildRequires:  pkgconfig(xcb-sync)
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xorg-server) >= 1.6
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(xscrnsaver)
BuildRequires:  pkgconfig(xshmfence)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(xvmc)
BuildRequires:  pkgconfig(xxf86vm)

Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires videodrv)
Requires: polkit

Provides:       %{oldname} = %{version}-%{release}
Obsoletes:      %{oldname} < %{version}-%{release}

%description
XLibre intel X11 video driver.

%prep
%setup -q -n %{reponame}-%{name}-%{version}
%patch -P0 -p1 -b .gcc-pr65873
%patch -P1 -p1 -b .sna-avoid-clobbering-physical-size
%patch -P2 -p1 -b .meson-has-present


%build
# This package causes LTO to thrash sucking up enormous amounts of VM.  This
# is almost certainly a GCC bug that will need to be analyzed/fixed.  Until
# then, disable LTO.
%define _lto_cflags %{nil}

%meson \
    -D async-swap=false \
    -D backlight-helper=true \
    -D backlight=true \
    -D default-accel=sna \
    -D default-dri=3 \
    -D dri1=false \
    -D dri2=true \
    -D dri3=true \
    -D internal-debug=no \
    -D kms=true \
    -D present=true \
    -D sna=true \
    -D tearfree=false \
    -D tools=true \
    -D ums=false \
    -D use-create2=false \
    -D uxa=true \
    -D valgrind=false \
    -D xorg-module-dir="%(realpath -m --relative-to="%{_prefix}" "%{moduledir}")" \
    -D xvmc=true

%meson_build

%install
%meson_install

find %{buildroot} -name "*.la" -delete

# libXvMC opens the versioned file name, these are useless
rm -f %{buildroot}%{_libdir}/libI*XvMC.so

%files
%doc COPYING
%{driverdir}/intel_drv.so
%{_libdir}/libIntelXvMC.so.1*
%{_libexecdir}/xf86-video-intel-backlight-helper
%{_datadir}/polkit-1/actions/org.x.xf86-video-intel.backlight-helper.policy
%{_mandir}/man4/i*
%{_bindir}/intel-virtual-output

%changelog
