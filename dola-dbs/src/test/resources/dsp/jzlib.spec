Name:           jzlib
Version:        1.1.3
Release:        %autorelease
Summary:        Re-implementation of zlib in pure Java
License:        BSD-3-Clause
URL:            http://www.jcraft.com/jzlib/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/ymnk/jzlib/archive/%{version}.tar.gz

# This patch is sent upstream: https://github.com/ymnk/jzlib/pull/15
Patch:          jzlib-javadoc-fixes.patch

BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 1.1.3-37

%description
The zlib is designed to be a free, general-purpose, legally unencumbered 
-- that is, not covered by any patents -- loss-less data-compression 
library for use on virtually any computer hardware and operating system. 
The zlib was written by Jean-loup Gailly (compression) and Mark Adler 
(decompression). 

%package demo
Summary:        Examples for %{name}
Requires:       %{name} = %{version}-%{release}

%description demo
%{summary}.

%prep
%autosetup -p1 -C

%pom_xpath_set "pom:plugin[pom:artifactId='maven-compiler-plugin']/pom:configuration/pom:source" 1.8
%pom_xpath_set "pom:plugin[pom:artifactId='maven-compiler-plugin']/pom:configuration/pom:target" 1.8

# Make into OSGi bundle
%pom_xpath_inject "pom:project" "<packaging>bundle</packaging>"
%pom_add_plugin "org.apache.felix:maven-bundle-plugin" . "<extensions>true</extensions>"

%mvn_file : %{name}

%build
%mvn_build -j

%install
%mvn_install

# examples
install -dm 755 %{buildroot}%{_datadir}/%{name}
cp -pr example/* %{buildroot}%{_datadir}/%{name}

%files -f .mfiles
%license LICENSE.txt

%files demo
%doc %{_datadir}/%{name}

%changelog
%autochangelog
