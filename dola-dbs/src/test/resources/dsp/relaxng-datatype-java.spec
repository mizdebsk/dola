Name:           relaxng-datatype-java
Version:        2011.1
Release:        %autorelease
Summary:        The relaxng datatype library for Java
# License file is not present in the source repository, the file was retrieved
# from SourceForge where the previous version is hosted
# https://sourceforge.net/projects/relaxng/files/datatype%20%28java%29/Ver.1.0/relaxngDatatype-1.0.zip/download
License:        BSD-3-Clause
URL:            https://relaxng.org/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/java-schema-utilities/%{name}/archive/refs/tags/relaxngDatatype-%{version}.tar.gz
Source1:        copying.txt

BuildRequires:  maven-local
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 2011.1-14

%description
Interface between RELAX NG validators and datatype libraries.

%prep
%autosetup -p1 -C
cp %{SOURCE1} .

%pom_remove_parent

%pom_xpath_remove 'pom:build/pom:extensions'

%mvn_alias com.github.relaxng:relaxngDatatype relaxngDatatype:relaxngDatatype

%build
%mvn_build -j -- -Dmaven.compiler.release=8

%install
%mvn_install

%files -f .mfiles
%license copying.txt

%changelog
%autochangelog
