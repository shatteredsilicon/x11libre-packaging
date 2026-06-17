%{!?upstream_version:%{error:upstream_version must be defined, e.g. rpmbuild --define 'upstream_version <version>'}}

%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir %{moduledir}/drivers
%global oldname xorg-x11-drv-nouveau
%global reponame xf86-video-nouveau

%define _disable_source_fetch 0

%undefine _hardened_build

Summary:   XLibre nouveau X11 video driver for NVIDIA graphics chipsets
Name:      xlibre-xf86-video-nouveau
Version:   %{upstream_version}
Release:   1%{?dist}
URL:       https://github.com/X11Libre/%{reponame}
License:   MIT

Source0:   https://github.com/X11Libre/%{reponame}/archive/refs/tags/%{name}-%{version}.tar.gz

ExcludeArch: s390 s390x

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  mesa-libGL-devel
BuildRequires:  pkgconfig(xorg-server) >= 1.8
BuildRequires:  pkgconfig(libdrm) >= 2.4.60
BuildRequires:  pkgconfig(libdrm_nouveau) >= 2.4.25
BuildRequires:  pkgconfig(pciaccess) >= 0.10
BuildRequires:  pkgconfig(libudev)

Requires:   Xorg %(xserver-sdk-abi-requires ansic)
Requires:   Xorg %(xserver-sdk-abi-requires videodrv)
Requires:   libdrm >= 2.4.33-0.1

Provides:       %{oldname} = 1:%{version}-%{release}
Obsoletes:      %{oldname} < 1:%{version}-%{release}

%description 
XLibre nouveau X11 video driver.

%prep
%setup -q -n %{reponame}-%{name}-%{version}

%build
autoreconf -v --install --force
%configure --disable-static --with-xorg-module-dir="%{moduledir}"
%make_build

%install
%make_install
find %{buildroot} -name "*.la" -delete

%files
%{driverdir}/nouveau_drv.so
%{_mandir}/man4/nouveau.4*

%changelog
