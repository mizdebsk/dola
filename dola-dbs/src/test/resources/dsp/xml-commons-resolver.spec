Name:           xml-commons-resolver
Version:        1.2
Release:        %autorelease
Summary:        Resolver subproject of xml-commons
License:        Apache-2.0
URL:            https://xerces.apache.org/xml-commons/components/resolver/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        http://www.apache.org/dist/xerces/xml-commons/%{name}-%{version}.tar.gz
Source5:        %{name}-pom.xml
Source6:        %{name}-resolver.1
Source7:        %{name}-xparse.1
Source8:        %{name}-xread.1

Patch:          %{name}-1.2-crosslink.patch
Patch:          %{name}-1.2-osgi.patch

BuildRequires:  javapackages-local
BuildRequires:  ant
BuildRequires:  apache-parent
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 1.2-53

%description
Resolver subproject of xml-commons.

%prep
%autosetup -p1 -C

# remove all binary libs and prebuilt javadocs
find . -name "*.jar" -exec rm -f {} \;
rm -rf docs
sed -i 's/\r//' KEYS LICENSE.resolver.txt NOTICE-resolver.txt

%mvn_file : xml-commons-resolver xml-resolver

%build
%ant -f resolver.xml jar -Dant.build.javac.source=1.8 -Dant.build.javac.target=1.8
%mvn_artifact %{SOURCE5} build/resolver.jar

%install
%mvn_install

# Scripts
mkdir -p %{buildroot}%{_bindir}
%jpackage_script org.apache.xml.resolver.apps.resolver "" "" %{name} xml-resolver true
%jpackage_script org.apache.xml.resolver.apps.xread "" "" %{name} xml-xread true
%jpackage_script org.apache.xml.resolver.apps.xparse "" "" %{name} xml-xparse true

# Man pages
install -d -m 755 %{buildroot}%{_mandir}/man1
install -p -m 644 %{SOURCE6} %{buildroot}%{_mandir}/man1/xml-resolver.1
install -p -m 644 %{SOURCE7} %{buildroot}%{_mandir}/man1/xml-xparse.1
install -p -m 644 %{SOURCE8} %{buildroot}%{_mandir}/man1/xml-xread.1

%files -f .mfiles
%doc KEYS
%license LICENSE.resolver.txt NOTICE-resolver.txt
%{_mandir}/man1/*
%{_bindir}/xml-*

%changelog
%autochangelog
