%{!?upstream_version:%{error:upstream_version must be defined, e.g. rpmbuild --define 'upstream_version <version>'}}

%global moduledir %(pkg-config xorg-server --variable=moduledir )
%global driverdir %{moduledir}/input
%global oldname xorg-x11-drv-evdev
%global reponame xf86-input-evdev
%define _disable_source_fetch 0

Summary:    XLibre evdev X11 input driver
Name:       xlibre-xf86-input-evdev
Version:    %{upstream_version}
Release:    1%{?dist}
URL :       https://github.com/X11Libre/%{reponame}
License:    HPND-sell-variant AND MIT

Source0:    https://github.com/X11Libre/%{reponame}/archive/refs/tags/%{name}-%{version}.tar.gz

BuildRequires: make
BuildRequires: autoconf automake libtool
BuildRequires: xorg-x11-server-devel >= 1.10.99.902
BuildRequires: libudev-devel mtdev-devel libevdev-devel
BuildRequires: xorg-x11-util-macros >= 1.3.0

Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires xinput)
Requires: xkeyboard-config >= 1.4-1
Requires: mtdev

Provides:  %{oldname} = %{version}-%{release}
Obsoletes: %{oldname} < %{version}-%{release}

Obsoletes: xorg-x11-drv-mouse < 1.9.0-8
Obsoletes: xorg-x11-drv-keyboard < 1.8.0-6

%description
XLibre evdev X11 input driver.

%prep
%setup -q -n %{reponame}-%{name}-%{version}

%build
autoreconf --force -v --install || exit 1
%configure --disable-static --disable-silent-rules --with-xorg-module-dir="%{moduledir}"
make %{?_smp_mflags}

%install
%make_install

find %{buildroot} -name "*.la" -delete

%files
%doc COPYING
%{driverdir}/evdev_drv.so
%{_mandir}/man4/evdev.4*
%{_datadir}/X11/xorg.conf.d/10-evdev.conf

%package devel
Summary:    XLibre evdev X11 input driver development package.
Requires:   pkgconfig

Provides:   %{oldname}-devel = %{version}-%{release}
Obsoletes:  %{oldname}-devel < %{version}-%{release}

%description devel
XLibre evdev X11 input driver development files.

%files devel
%doc COPYING
%dir %{_includedir}/xorg
%{_includedir}/xorg/evdev-properties.h


%changelog
