Name:           java-rpm-macros
Version:        1
Release:        %autorelease
Summary:        Common Java RPM macros
License:        MIT-0
BuildArch:      noarch

Source1:        macros.java-srpm

%description
RPM macros for building Java RPM packages.

%package -n java-srpm-macros
Summary:        RPM macros for building Java source packages
Requires:       rpm

%description -n java-srpm-macros
RPM macros for building Java source packages.

%install
install -D -p -m 644 %{SOURCE1} %{buildroot}%{rpmmacrodir}/macros.java-srpm

%files -n java-srpm-macros
%{rpmmacrodir}/macros.java-srpm

%changelog
%autochangelog
