%{!?upstream_version:%{error:upstream_version must be defined, e.g. rpmbuild --define 'upstream_version <version>'}}

%global moduledir %(pkg-config xorg-server --variable=moduledir )
%global driverdir %{moduledir}/input
%global oldname xorg-x11-drv-synaptics
%global reponame xf86-input-synaptics
%define _disable_source_fetch 0

Name:           xlibre-xf86-input-synaptics
Summary:        XLibre synaptics X11 input driver for Synaptics touchpads
Version:        %{upstream_version}
Release:        1%{?dist}
URL :           https://github.com/X11Libre/%{reponame}
# SPDX
License:        MIT

Source0:        https://github.com/X11Libre/%{reponame}/archive/refs/tags/%{name}-%{version}.tar.gz
Source1:        70-synaptics.conf
Source2:        70-touchpad-quirks.rules

ExcludeArch:    s390 s390x

BuildRequires:  make
BuildRequires:  autoconf automake libtool pkgconfig
BuildRequires:  xorg-x11-server-devel >= 1.10.99.902
BuildRequires:  libX11-devel libXi-devel libXtst-devel
BuildRequires:  xorg-x11-util-macros >= 1.8.0
BuildRequires:  libevdev-devel
BuildRequires:  systemd

Requires:       Xorg %(xserver-sdk-abi-requires ansic)
Requires:       Xorg %(xserver-sdk-abi-requires xinput)
Requires:       libevdev
Requires:       libXi libXtst

Provides:       synaptics = %{version}-%{release}
Obsoletes:      synaptics < 0.15.0

Provides:       %{oldname} = %{version}-%{release}
Obsoletes:      %{oldname} < %{version}-%{release}

Provides:       %{oldname}-legacy = %{version}-%{release}
Obsoletes:      %{oldname}-legacy < %{version}-%{release}

%description
This is the Synaptics touchpad driver for the XLibre X server. The following
touchpad models are supported:
* Synaptics
* appletouch (Post February 2005 and October 2005 Apple Aluminium Powerbooks)
* Elantech (EeePC)
* bcm5974 (Macbook Air (Jan 2008), Macbook Pro Penryn (Feb 2008), iPhone
  (2007), iPod Touch (2008)

Note that support for appletouch, elantech and bcm5974 requires the respective
kernel module.
A touchpad by default operates in compatibility mode by emulating a standard
mouse. However, by using a dedicated driver, more advanced features of the
touchpad become available.

Features:

    * Movement with adjustable, non-linear acceleration and speed.
    * Button events through short touching of the touchpad ("tapping").
    * Double-Button events through double short touching of the touchpad.
    * Dragging through short touching and holding down the finger on the
      touchpad.
    * Middle and right button events on the upper and lower corner of the
      touchpad.
    * Vertical scrolling (button four and five events) through moving the
      finger on the right side of the touchpad.
    * The up/down button sends button four/five events.
    * Horizontal scrolling (button six and seven events) through moving the
      finger on the lower side of the touchpad.
    * The multi-buttons send button four/five events, and six/seven events for
      horizontal scrolling.
    * Adjustable finger detection.
      Multifinger taps: two finger for middle button and three finger for
      right button events. (Needs hardware support. Not all models implement
      this feature.)
    * Run-time configuration using shared memory. This means you can change
      parameter settings without restarting the X server.

%prep
%setup -q -n %{reponame}-%{name}-%{version}

%build
autoreconf -v --install --force || exit 1
%configure --disable-static --disable-silent-rules --with-xorg-module-dir="%{moduledir}"
make %{?_smp_mflags}

%install
%make_install
find %{buildroot} -name "*.la" -delete

# Remove upstream synaptics.conf as we've several special fixes in ours
rm $RPM_BUILD_ROOT%{_datadir}/X11/xorg.conf.d/70-synaptics.conf

install -d $RPM_BUILD_ROOT%{_datadir}/X11/xorg.conf.d
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/X11/xorg.conf.d/70-synaptics.conf

install -d $RPM_BUILD_ROOT%{_udevrulesdir}
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_udevrulesdir}/70-touchpad-quirks.rules

%post
udevadm control --reload-rules || :

%postun
udevadm control --reload-rules || :

%files
%doc README.md
%license COPYING
%{_datadir}/X11/xorg.conf.d/70-synaptics.conf
%{driverdir}/synaptics_drv.so
%{_bindir}/synclient
%{_bindir}/syndaemon
%{_mandir}/man4/synaptics.4*
%{_mandir}/man1/synclient.1*
%{_mandir}/man1/syndaemon.1*
%{_udevrulesdir}/70-touchpad-quirks.rules

%package devel
Summary:        XLibre synaptics X11 input driver development package
Requires:       pkgconfig

Provides:       %{oldname}-devel = %{version}-%{release}
Obsoletes:      %{oldname}-devel < %{version}-%{release}

%description devel
Development files for the Synaptics TouchPad X11 input driver for XLibre.

%files devel
%license COPYING
%dir %{_includedir}/xorg
%{_includedir}/xorg/synaptics-properties.h

%changelog
