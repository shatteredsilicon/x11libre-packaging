%{!?upstream_version:%{error:upstream_version must be defined, e.g. rpmbuild --define 'upstream_version <version>'}}

%global moduledir %(pkg-config xorg-server --variable=moduledir )
%global driverdir %{moduledir}/drivers
%global oldname xorg-x11-drv-dummy
%global reponame xf86-video-dummy
%define _disable_source_fetch 0

%undefine _hardened_build

Summary:   XLibre dummy X11 video driver
Name:      xlibre-xf86-video-dummy
Version:   %{upstream_version}
Release:   1%{?dist}
URL:       https://github.com/X11Libre/%{reponame}
License:   MIT AND X11

Source0:   https://github.com/X11Libre/%{reponame}/archive/refs/tags/%{name}-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconfig(xorg-server) >= 1.4.99.901

Provides:       %{oldname} = %{version}-%{release}
Obsoletes:      %{oldname} < %{version}-%{release}

Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires videodrv)

%description 
XLibre dummy X11 video driver.

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
%doc README.md
%{driverdir}/dummy_drv.so

%changelog
