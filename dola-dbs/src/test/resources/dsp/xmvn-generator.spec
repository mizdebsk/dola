%global debug_package %{nil}
%bcond_with bootstrap

Name:           xmvn-generator
Version:        2.0.2^20250414.071740.git.9cf5182
Release:        %autorelease
Summary:        RPM dependency generator for Java
License:        Apache-2.0
URL:            https://github.com/fedora-java/xmvn-generator
ExclusiveArch:  %{java_arches}

Source:         xmvn-generator-snapshot-20250414.071740-9cf5182.tar.zst

BuildRequires:  gcc
BuildRequires:  lujavrite
BuildRequires:  rpm-devel
%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.commons:commons-compress)
BuildRequires:  mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires:  mvn(org.easymock:easymock)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter)
BuildRequires:  mvn(org.ow2.asm:asm)
BuildRequires:  maven4-lib
BuildRequires:  xmvn5-minimal
%endif
Requires:       java-21-openjdk-headless
Requires:       lujavrite
Requires:       xmvn5-minimal
Requires:       dola-gleaner
Requires:       rpm-build
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 2.0.2-9
Provides:       maven-declarative-build-support

%description
XMvn Generator is a dependency generator for RPM Package Manager
written in Java and Lua, that uses LuJavRite library to call Java code
from Lua.

%prep
%autosetup -p1 -C
%mvn_file : %{name}

%build
%mvn_build -j -- -P\!quality

%install
%mvn_install
install -D -p -m 644 src/main/lua/xmvn-generator.lua %{buildroot}%{_rpmluadir}/xmvn-generator.lua
install -D -p -m 644 src/main/rpm/macros.xmvngen %{buildroot}%{_rpmmacrodir}/macros.xmvngen
install -D -p -m 644 src/main/rpm/macros.xmvngenhook %{buildroot}%{_sysconfdir}/rpm/macros.xmvngenhook
install -D -p -m 644 src/main/rpm/xmvngen.attr %{buildroot}%{_fileattrsdir}/xmvngen.attr
install -D -p -m 644 src/main/conf/xmvn-generator.conf %{buildroot}%{_javaconfdir}/xmvn-generator.conf

%files -f .mfiles
%{_rpmluadir}/*
%{_rpmmacrodir}/*
%{_fileattrsdir}/*
%{_sysconfdir}/rpm/*
%{_javaconfdir}/*
%license LICENSE NOTICE
%doc README.md

%changelog
%autochangelog
