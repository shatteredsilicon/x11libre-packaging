%{!?upstream_version:%{error:upstream_version must be defined, e.g. rpmbuild --define 'upstream_version <version>'}}

%global moduledir %(pkg-config xorg-server --variable=moduledir )
%global driverdir	%{moduledir}/drivers
%global oldname xorg-x11-drv-vmware
%global reponame xf86-video-vmware
%define _disable_source_fetch 0

%undefine _hardened_build

Summary:    XLibre vmware X11 video driver
Name:       xlibre-xf86-video-vmware
Version:    %{upstream_version}
Release:    2%{?dist}
URL:        https://github.com/X11Libre/%{reponame}
License:    MIT AND X11

Source0:    https://github.com/X11Libre/%{reponame}/archive/refs/tags/%{name}-%{version}.tar.gz

ExclusiveArch: %{ix86} x86_64 x86_64_v2 ia64

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(libdrm) >= 2.4.96
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(pciaccess) >= 0.8.0
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xatracker) >= 0.4.0
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xorg-server) >= 1.12

Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires videodrv)
Requires: mesa-compat-libxatracker

Provides:       %{oldname} = %{version}-%{release}
Obsoletes:      %{oldname} < %{version}-%{release}

%description
XLibre vmware X11 video driver.

%prep
%setup -q -n %{reponame}-%{name}-%{version}

%build
autoreconf -vif
%configure --disable-static --with-xorg-module-dir="%{moduledir}"
%make_build

%install
%make_install
find %{buildroot} -name "*.la" -delete

%files
%{driverdir}/vmware_drv.so
%{_mandir}/man4/vmware.4*

%changelog
