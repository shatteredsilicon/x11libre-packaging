%{!?upstream_version:%{error:upstream_version must be defined, e.g. rpmbuild --define 'upstream_version <version>'}}

%global moduledir %(pkg-config xorg-server --variable=moduledir )
%global driverdir %{moduledir}/drivers
%global oldname xorg-x11-drv-qxl
%global reponame xf86-video-qxl
%define _disable_source_fetch 0

%undefine _hardened_build

# Xspice is x86_64 and ARM only since spice-server is x86_64 / ARM only
%ifarch %{ix86} x86_64 %{arm} aarch64
%define with_xspice 1
%else
%define with_xspice 0
%endif

Summary:    XLibre qxl X11 video driver
Name:       xlibre-xf86-video-qxl
Version:    %{upstream_version}
Release:    2%{?dist}
URL:        https://github.com/X11Libre/%{reponame}
License:    MIT

Source0:    https://github.com/X11Libre/%{reponame}/archive/refs/tags/%{name}-%{version}.tar.gz
Patch1:     0001-worst-hack-of-all-time-to-qxl-driver.patch
# This shebang patch is currently downstream-only
Patch2:     0005-Xspice-Adjust-shebang-to-explicitly-mention-python3.patch

ExcludeArch: s390 s390x

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  git-core
BuildRequires:  libtool
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libdrm) >= 2.4.46
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(xfont2)
BuildRequires:  pkgconfig(xorg-server) >= 1.0.99.901
BuildRequires:  pkgconfig(pciaccess) >= 0.10
BuildRequires:  pkgconfig(spice-protocol) >= 0.12.0
%if %{with_xspice}
BuildRequires:  pkgconfig(libcacard)
BuildRequires:  pkgconfig(libpcsclite)
BuildRequires:  pkgconfig(spice-server) >= 0.6.3
%endif

Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires videodrv)

Provides:       %{oldname} = %{version}-%{release}
Obsoletes:      %{oldname} < %{version}-%{release}

%description
XLibre qxl X11 video driver.

%if %{with_xspice}
%package -n     xlibre-server-Xspice
Summary:        XSpice is an X server that can be accessed by a Spice client
Requires:       Xorg %(xserver-sdk-abi-requires ansic)
Requires:       Xorg %(xserver-sdk-abi-requires videodrv)
Requires:       xlibre-server-Xorg
Requires:       pcsc-lite-ccid

Provides:       xorg-x11-server-Xspice = %{version}-%{release}
Obsoletes:      xorg-x11-server-Xspice < %{version}-%{release}

%description -n xlibre-server-Xspice
XSpice is both an X and a Spice server.
%endif

%prep
%setup -q -n %{reponame}-%{name}-%{version}
%patch -P1 -p1 -b .worst-hack-of-all-time
%patch -P2 -p1 -b .Xspice-python3-shebang

%build
autoreconf -vif
%if %{with_xspice}
%define enable_xspice --enable-ccid --enable-xspice
%endif
%configure --disable-static %{?enable_xspice} --with-xorg-module-dir="%{moduledir}"
%make_build

%install
%make_install

find %{buildroot} -name "*.la" -delete
rm -f %{buildroot}%{_docdir}/xf86-video-qxl/spiceqxl.xorg.conf.example
rm -f %{buildroot}%{_docdir}/xlibre-xf86-video-qxl/spiceqxl.xorg.conf.example

%if %{with_xspice}
mkdir -p %{buildroot}%{_sysconfdir}/X11
install -p -m 644 examples/spiceqxl.xorg.conf.example \
    %{buildroot}%{_sysconfdir}/X11/spiceqxl.xorg.conf
%endif


%files
%doc COPYING README.md
%{driverdir}/qxl_drv.so

%if %{with_xspice}
%files -n xlibre-server-Xspice
%doc COPYING README.xspice README.md examples/spiceqxl.xorg.conf.example
%config(noreplace) %{_sysconfdir}/X11/spiceqxl.xorg.conf
%{_bindir}/Xspice
%{driverdir}/spiceqxl_drv.so
%{_libdir}/pcsc/drivers/serial/libspiceccid.so*
%endif


%changelog
