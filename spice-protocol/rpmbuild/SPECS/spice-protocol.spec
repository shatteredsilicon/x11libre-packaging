%{!?upstream_version:%{error:upstream_version must be defined, e.g. rpmbuild --define 'upstream_version <version>'}}

Name:           spice-protocol
Version:        %{upstream_version}
Release:        1%{?dist}
Summary:        Spice protocol header files

License:        BSD-3-Clause AND LGPL-2.1-or-later
URL:            https://www.spice-space.org/
Source0:        https://www.spice-space.org/download/releases/%{name}-%{version}.tar.xz

BuildArch:      noarch

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Header files describing the SPICE protocol and the para-virtual QXL graphics
card.

%prep
%autosetup

%build
%meson
%meson_build

%install
%meson_install

%files
%license COPYING
%doc CHANGELOG.md README.md
%{_includedir}/spice-1/
%{_datadir}/pkgconfig/spice-protocol.pc

%changelog
