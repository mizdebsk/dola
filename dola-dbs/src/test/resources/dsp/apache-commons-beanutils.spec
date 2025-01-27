%bcond_with bootstrap

Name:           apache-commons-beanutils
Version:        1.9.4
Release:        %autorelease
Summary:        Java utility methods for accessing and modifying the properties of arbitrary JavaBeans
License:        Apache-2.0
URL:            https://commons.apache.org/proper/commons-beanutils/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        http://archive.apache.org/dist/commons/beanutils/source/commons-beanutils-%{version}-src.tar.gz

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(commons-collections:commons-collections)
BuildRequires:  mvn(commons-logging:commons-logging)
BuildRequires:  mvn(org.apache.commons:commons-parent:pom:)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 1.9.4-40

%description
The scope of this package is to create a package of Java utility methods
for accessing and modifying the properties of arbitrary JavaBeans.  No
dependencies outside of the JDK are required, so the use of this package
is very lightweight.

%prep
%autosetup -p1 -C
sed -i 's/\r//' *.txt

%pom_remove_plugin :maven-assembly-plugin

%mvn_alias :{*} :@1-core :@1-bean-collections
%mvn_alias :{*} org.apache.commons:@1 org.apache.commons:@1-core org.apache.commons:@1-bean-collections
%mvn_file : %{name} %{name}-core %{name}-bean-collections
%mvn_file : commons-beanutils commons-beanutils-core commons-beanutils-bean-collections

%build
# Some tests fail in Koji
%mvn_build -j -f -- -Dcommons.packageId=beanutils

%install
%mvn_install

%files -f .mfiles
%doc RELEASE-NOTES.txt
%license LICENSE.txt NOTICE.txt

%changelog
%autochangelog
