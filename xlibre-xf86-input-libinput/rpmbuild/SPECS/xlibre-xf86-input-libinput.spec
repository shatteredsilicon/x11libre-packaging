%{!?upstream_version:%{error:upstream_version must be defined, e.g. rpmbuild --define 'upstream_version <version>'}}

%global moduledir %(pkg-config xorg-server --variable=moduledir )
%global driverdir %{moduledir}/input
%global oldname xorg-x11-drv-libinput
%global reponame xf86-input-libinput
%define _disable_source_fetch 0

Summary:    XLibre libinput X11 input driver
Name:       xlibre-xf86-input-libinput
Version:    %{upstream_version}
Release:    1%{?dist}
URL :       https://github.com/X11Libre/%{reponame}
# SPDX
License:    MIT

Source0:    https://github.com/X11Libre/%{reponame}/archive/refs/tags/%{name}-%{version}.tar.gz
Source1:    71-libinput-overrides-wacom.conf

# Fedora-only hack for hidpi screens
# https://bugzilla.redhat.com/show_bug.cgi?id=1413306
Patch01:    xlibre-xf86-input-libinput-1.5.0.1-Add-a-DPIScaleFactor-option-as-temporary-solution-to.patch

BuildRequires: make
BuildRequires: autoconf automake libtool
BuildRequires: xlibre-xserver-devel >= 1.14.0
BuildRequires: libudev-devel libevdev-devel libinput-devel >= 0.6.0-3
BuildRequires: xorg-x11-util-macros
BuildRequires: libinput-devel >= 0.6.0-3

Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires xinput)
Requires: xkeyboard-config
Requires: libinput >= 0.21.0

Provides:  %{oldname} = %{version}-%{release}
Obsoletes: %{oldname} < %{version}-%{release}

Provides: xorg-x11-drv-synaptics = 1.9.0-3
Obsoletes: xorg-x11-drv-synaptics < 1.9.0-3

%description
A generic X11 input driver for the XLibre X server based on libinput,
supporting all devices.

%prep
%setup -q -n %{reponame}-%{name}-%{version}
%patch -P1 -p1 -b .DPIScaleFactor

%build
autoreconf --force -v --install || exit 1
%configure --disable-static --disable-silent-rules --with-xorg-module-dir="%{moduledir}"
make %{?_smp_mflags}

%install
%make_install

find %{buildroot} -name "*.la" -delete

cp %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/X11/xorg.conf.d/

%files
%doc COPYING
%{driverdir}/libinput_drv.so
%{_datadir}/X11/xorg.conf.d/40-libinput.conf
%{_datadir}/X11/xorg.conf.d/71-libinput-overrides-wacom.conf
%{_mandir}/man4/libinput.4*

%package devel
Summary:        XLibre libinput X11 input driver development package.
Requires:       pkgconfig

Provides:       %{oldname}-devel = %{version}-%{release}
Obsoletes:      %{oldname}-devel < %{version}-%{release}

%description devel
XLibre libinput X11 input driver development files.

%files devel
%doc COPYING
%{_libdir}/pkgconfig/xorg-libinput.pc
%dir %{_includedir}/xorg/
%{_includedir}/xorg/libinput-properties.h


%changelog
