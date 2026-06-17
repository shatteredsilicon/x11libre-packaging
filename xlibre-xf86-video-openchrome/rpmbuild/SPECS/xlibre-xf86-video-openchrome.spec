%{!?upstream_version:%{error:upstream_version must be defined, e.g. rpmbuild --define 'upstream_version <version>'}}

%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir %{moduledir}/drivers
%global oldname xorg-x11-drv-openchrome
%global reponame xf86-video-openchrome

%undefine _hardened_build

Summary:        X.Org X11 openchrome video driver rebuilt for XLibre
Name:           xlibre-xf86-video-openchrome
Version:        %{upstream_version}
Release:        1%{?dist}
URL:            http://www.freedesktop.org/wiki/Openchrome/
License:        MIT

Source0:        https://github.com/X11Libre/%{reponame}/archive/refs/tags/%{name}-%{version}.tar.gz

ExclusiveArch:  %{ix86} x86_64 x86_64_v2

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  mesa-libGL-devel
BuildRequires:  pkgconfig(libdrm) >= 2.2
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(pciaccess) >= 0.8.0
BuildRequires:  pkgconfig(xorg-server)

Requires:       Xorg %(xserver-sdk-abi-requires ansic)
Requires:       Xorg %(xserver-sdk-abi-requires videodrv)
Requires:       xorg-x11-server-wrapper

Obsoletes:      %{oldname}-devel < %{version}-%{release}
Provides:       %{oldname}-devel = %{version}-%{release}

Obsoletes:      %{oldname} < %{version}-%{release}
Provides:       %{oldname} = %{version}-%{release}

%description
A build of the X.Org X11 openchrome video driver recompiled against the XLibre
X server.

%prep
%setup -q -n %{reponame}-%{name}-%{version}

%build
autoreconf -vif
%configure --disable-static --enable-viaregtool --with-xorg-module-dir="%{moduledir}"
%make_build

%install
%make_install
find %{buildroot} -name "*.la" -delete

%files
%doc NEWS README
%license COPYING
%{driverdir}/openchrome_drv.so
%{_mandir}/man4/openchrome.4.gz
%{_sbindir}/via_regs_dump


%changelog
