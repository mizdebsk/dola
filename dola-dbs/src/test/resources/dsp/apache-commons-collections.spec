%bcond_with bootstrap

Name:           apache-commons-collections
Version:        3.2.2
Release:        %autorelease
Summary:        Provides new interfaces, implementations and utilities for Java Collections
License:        Apache-2.0
URL:            https://commons.apache.org/proper/commons-collections/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        http://www.apache.org/dist/commons/collections/source/commons-collections-%{version}-src.tar.gz

Patch:          0001-Port-to-Java-8.patch
Patch:          0002-Port-to-OpenJDK-11.patch
Patch:          0003-Port-to-OpenJDK-21.patch

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.commons:commons-parent:pom:)
BuildRequires:  mvn(org.apache.maven.plugins:maven-antrun-plugin)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 3.2.2-57

%description
The introduction of the Collections API by Sun in JDK 1.2 has been a
boon to quick and effective Java programming. Ready access to powerful
data structures has accelerated development by reducing the need for
custom container classes around each core object. Most Java2 APIs are
significantly easier to use because of the Collections API.
However, there are certain holes left unfilled by Sun's
implementations, and the Jakarta-Commons Collections Component strives
to fulfill them. Among the features of this package are:
- special-purpose implementations of Lists and Maps for fast access
- adapter classes from Java1-style containers (arrays, enumerations) to
Java2-style collections.
- methods to test or create typical set-theory properties of collections
such as union, intersection, and closure.

%package testframework
Summary:        Testframework for %{name}
Requires:       %{name} = %{version}-%{release}

%description testframework
%{summary}.

%prep
%autosetup -p1 -C

# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;
find . -name "*.class" -exec rm -f {} \;


# Port to maven-antrun-plugin 3.0.0
sed -i s/tasks/target/ pom.xml

# Fix file eof
sed -i 's/\r//' LICENSE.txt PROPOSAL.html README.txt NOTICE.txt

%mvn_package :commons-collections-testframework testframework
%mvn_file ':commons-collections{,-testframework}' %{name}@1 commons-collections@1

%build
%mvn_build -j -- -Dcommons.packageId=collections

%install
%mvn_artifact commons-collections:commons-collections-testframework:%{version} target/commons-collections-testframework-%{version}.jar
%mvn_install

%files -f .mfiles
%doc PROPOSAL.html README.txt
%license LICENSE.txt NOTICE.txt

%files testframework -f .mfiles-testframework

%changelog
%autochangelog
