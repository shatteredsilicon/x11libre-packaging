%{!?upstream_version:%{error:upstream_version must be defined, e.g. rpmbuild --define 'upstream_version <version>'}}

%global moduledir %(pkg-config xorg-server --variable=moduledir )
%global driverdir %{moduledir}/input
%global oldname xorg-x11-drv-wacom
%global reponame xf86-input-wacom

Summary:    XLibre wacom X11 input driver
Name:       xlibre-xf86-input-wacom
Version:    %{upstream_version}
Release:    1%{?dist}
URL :       https://github.com/X11Libre/%{reponame}
License:    GPL-2.0-or-later

Source0:    https://github.com/X11Libre/%{reponame}/archive/refs/tags/%{name}-%{version}.tar.gz

BuildRequires: make
BuildRequires: pkgconfig(xorg-server) >= 1.10.99.902
BuildRequires: xorg-x11-util-macros >= 1.3.0
BuildRequires: libX11-devel libXi-devel libXrandr-devel libXinerama-devel
BuildRequires: autoconf automake libtool
BuildRequires: systemd systemd-devel

Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires xinput)
Requires: %{name}-serial-support

Provides:  linuxwacom = %{version}-%{release}
Obsoletes: linuxwacom <= 0.8.4.3

Provides:  %{oldname} = %{version}-%{release}
Obsoletes: %{oldname} < %{version}-%{release}

%description
XLibre wacom X11 input driver for Wacom tablets.

%prep
%setup -q -n %{reponame}-%{name}-%{version}

%build
autoreconf --force -v --install || exit 1
%configure --disable-static --disable-silent-rules --enable-debug \
           --with-systemd-unit-dir=%{_unitdir} \
           --with-udev-rules-dir=%{_prefix}/lib/udev/rules.d/ \
           --with-xorg-module-dir="%{moduledir}"

make %{_smp_mflags}

%install
%make_install
find %{buildroot} -name "*.la" -delete
mv $RPM_BUILD_ROOT/%{_prefix}/lib/udev/rules.d/wacom.rules $RPM_BUILD_ROOT/%{_prefix}/lib/udev/rules.d/70-wacom.rules

%files
%doc AUTHORS
%license GPL
%{driverdir}/wacom_drv.so
%{_mandir}/man4/wacom.4*
%{_mandir}/man1/xsetwacom.1*
%{_datadir}/X11/xorg.conf.d/70-wacom.conf
%{_bindir}/xsetwacom

%package devel
Summary:    XLibre wacom X11 input driver development package

Requires: pkgconfig
Requires: pkgconfig(xorg-server) >= 1.7.0

Provides:  %{oldname}-devel = %{version}-%{release}
Obsoletes: %{oldname}-devel < %{version}-%{release}

%description devel
XLibre wacom X11 input driver development files.

%files devel
%license GPL
%{_libdir}/pkgconfig/xorg-wacom.pc
%{_includedir}/xorg/Xwacom.h
%{_includedir}/xorg/wacom-properties.h
%{_includedir}/xorg/wacom-util.h
%{_includedir}/xorg/isdv4.h
%{_bindir}/isdv4-serial-debugger

%package serial-support
Summary:    Files for enabling the wacom_w8001 kernel driver

Provides:  %{oldname}-serial-support = %{version}-%{release}
Obsoletes: %{oldname}-serial-support < %{version}-%{release}

%description serial-support
Files for enabling the wacom_w8001 kernel driver on Wacom
ISDv4-compatible serial tablets. If enabled, the serial tablet's device node
will be available as normal evdev node.

%files serial-support
%license GPL
%{_prefix}/lib/udev/rules.d/70-wacom.rules
%{_bindir}/isdv4-serial-inputattach
%{_unitdir}/wacom-inputattach@.service

%changelog
