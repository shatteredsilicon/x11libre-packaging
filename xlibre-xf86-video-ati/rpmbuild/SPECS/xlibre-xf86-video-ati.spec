%{!?upstream_version:%{error:upstream_version must be defined, e.g. rpmbuild --define 'upstream_version <version>'}}

%global moduledir %(pkg-config xorg-server --variable=moduledir )
%global driverdir	%{moduledir}/drivers
%global oldname xorg-x11-drv-ati
%global reponame xf86-video-ati

%undefine _hardened_build

Summary:   XLibre ati X11 video driver
Name:      xlibre-xf86-video-ati
Version:   %{upstream_version}
Release:   1%{?dist}
URL:       https://github.com/X11Libre/%{reponame}
License:   MIT

Source0:   https://github.com/X11Libre/%{reponame}/archive/refs/tags/%{name}-%{version}.tar.gz

ExcludeArch: s390 s390x

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  kernel-headers
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconfig(pciaccess) >= 0.8.0
BuildRequires:  pkgconfig(gbm) >= 10.6
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(libdrm) >= 2.4.89
BuildRequires:  pkgconfig(libdrm_radeon)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(xorg-server) >= 1.16

Requires: libdrm >= 2.4.89
Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires videodrv)

Provides:       %{oldname} = %{version}-%{release}
Obsoletes:      %{oldname} < %{version}-%{release}

%description
XLibre ati X11 video driver.

%prep
%setup -q -n %{reponame}-%{name}-%{version}

%build
autoreconf -iv
%configure --disable-static --enable-glamor --with-xorg-module-dir="%{moduledir}"
%make_build

%install
%make_install
find %{buildroot} -name "*.la" -delete

%files
%{driverdir}/ati_drv.so
%{driverdir}/radeon_drv.so
%{_mandir}/man4/ati.4*
%{_mandir}/man4/radeon.4*
%{_datadir}/X11/xorg.conf.d/10-radeon.conf

%changelog
