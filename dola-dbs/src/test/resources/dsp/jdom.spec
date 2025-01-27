%bcond_with bootstrap

Name:           jdom
Version:        1.1.3
Release:        %autorelease
Summary:        Java alternative to DOM and SAX
License:        Saxpath
URL:            http://www.jdom.org/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        http://jdom.org/dist/binary/archive/jdom-%{version}.tar.gz
Source1:        https://repo1.maven.org/maven2/org/jdom/jdom/%{version}/jdom-%{version}.pom

Patch:          %{name}-crosslink.patch
Patch:          %{name}-1.1-OSGiManifest.patch
# Security patches
Patch:          CVE-2021-33813.patch

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  javapackages-local
BuildRequires:  ant
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 1.1.3-45

%description
JDOM is, quite simply, a Java representation of an XML document. JDOM
provides a way to represent that document for easy and efficient
reading, manipulation, and writing. It has a straightforward API, is a
lightweight and fast, and is optimized for the Java programmer. It's an
alternative to DOM and SAX, although it integrates well with both DOM
and SAX.

%package demo
Summary:        Demos for %{name}
Requires:       %{name} = %{version}-%{release}

%description demo
Demonstrations and samples for %{name}.

%prep
%autosetup -p1 -C
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;
find . -name "*.class" -exec rm -f {} \;

%build
%ant -Dcompile.source=1.8 -Dcompile.target=1.8 package

%install
%mvn_file : %{name}
%mvn_alias : jdom:jdom
%mvn_artifact %{SOURCE1} build/%{name}-*-snap.jar
%mvn_install

# demo
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -pr samples $RPM_BUILD_ROOT%{_datadir}/%{name}

%files -f .mfiles
%license LICENSE.txt
%doc CHANGES.txt COMMITTERS.txt README.txt TODO.txt

%files demo
%{_datadir}/%{name}
%license LICENSE.txt

%changelog
%autochangelog
