%{!?upstream_version:%{error:upstream_version must be defined, e.g. rpmbuild --define 'upstream_version <version>'}}

Summary: X.Org X11 libXvMC runtime library
Name: libXvMC
Version: %{upstream_version}
Release: 10%{?dist}
License: MIT
URL: http://www.x.org

Source0: https://xorg.freedesktop.org/archive/individual/lib/%{name}-%{version}.tar.xz

Requires: libX11 >= 1.5.99.902

BuildRequires: make
BuildRequires: xorg-x11-util-macros
BuildRequires: autoconf automake libtool
BuildRequires: pkgconfig(videoproto) pkgconfig(xv)
BuildRequires: libX11-devel >= 1.5.99.902

%description
X.Org X11 libXvMC runtime library

%package devel
Summary: X.Org X11 libXvMC development package
Requires: %{name} = %{version}-%{release}

%description devel
X.Org X11 libXvMC development package

%prep
%autosetup -n %{name}-%{version}

%build
autoreconf -v --install --force
%configure --disable-static
%make_build

%install
%make_install INSTALL="install -p"

# do this ourself in %%doc so we get %%version
rm $RPM_BUILD_ROOT%{_docdir}/*/*.txt

# Touch XvMCConfig for rpm to package the ghost file. (#192254)
{
    mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/X11
    touch $RPM_BUILD_ROOT%{_sysconfdir}/X11/XvMCConfig
}

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%ldconfig_scriptlets

%files
%doc COPYING README.md
%{_libdir}/libXvMC.so.1
%{_libdir}/libXvMC.so.1.0.0
%{_libdir}/libXvMCW.so.1
%{_libdir}/libXvMCW.so.1.0.0
%ghost %config(missingok,noreplace) %verify (not md5 size mtime) %{_sysconfdir}/X11/XvMCConfig

%files devel
%doc XvMC_API.txt
%{_includedir}/X11/extensions/XvMClib.h
%{_includedir}/X11/extensions/vldXvMC.h
%{_libdir}/libXvMC.so
%{_libdir}/libXvMCW.so
%{_libdir}/pkgconfig/xvmc.pc
%{_libdir}/pkgconfig/xvmc-wrapper.pc

%changelog
