%{!?upstream_version:%{error:upstream_version must be defined, e.g. rpmbuild --define 'upstream_version <version>'}}

%global moduledir %(pkg-config xorg-server --variable=moduledir )
%global driverdir %{moduledir}/drivers
%global oldname xorg-x11-drv-amdgpu
%global reponame xf86-video-amdgpu
%define _disable_source_fetch 0

# XLibre cannot load hardened build
%undefine _hardened_build

Name:       xlibre-xf86-video-amdgpu
Version:    %{upstream_version}
Release:    2%{?dist}

Summary:    XLibre amdgpu X11 video driver
License:    MIT

URL:        https://github.com/X11Libre/%{reponame}
Source0:    https://github.com/X11Libre/%{reponame}/archive/refs/tags/%{name}-%{version}.tar.gz

ExcludeArch: s390 s390x

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  kernel-headers
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(libdrm) >= 2.4.89
BuildRequires:  pkgconfig(libdrm_amdgpu) >= 2.4.76
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(xorg-server) >= 1.13
BuildRequires:  xorg-x11-util-macros

Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires videodrv)
Requires: libdrm >= 2.4.89

Provides:       %{oldname} = %{version}-%{release}
Obsoletes:      %{oldname} < %{version}-%{release}

%description
XLibre amdgpu X11 video driver.

%prep
%setup -q -n %{reponame}-%{name}-%{version}

%build
autoreconf -fiv
%configure --disable-static --enable-glamor --with-xorg-module-dir="%{moduledir}"
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

%files
%{driverdir}/video/amdgpu_drv.so
%{_datadir}/X11/xorg.conf.d/10-amdgpu.conf
%{_mandir}/man4/amdgpu.4*

%changelog
