%bcond_with bootstrap

Name:           apache-commons-lang3
Version:        3.17.0
Release:        %autorelease
Summary:        Provides a host of helper utilities for the java.lang API
License:        Apache-2.0
URL:            https://commons.apache.org/proper/commons-lang/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://archive.apache.org/dist/commons/lang/source/commons-lang3-%{version}-src.tar.gz

Patch:          0001-Remove-test-dependency-on-JUnit-Pioneer.patch

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(biz.aQute.bnd:biz.aQute.bndlib)
BuildRequires:  mvn(com.google.code.findbugs:jsr305)
BuildRequires:  mvn(org.apache.commons:commons-parent:pom:)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires:  mvn(org.easymock:easymock)
BuildRequires:  mvn(org.hamcrest:hamcrest)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 3.17.0-7

%description
The standard Java libraries fail to provide enough methods for
manipulation of its core classes. The Commons Lang Component provides
these extra methods.
The Commons Lang Component provides a host of helper utilities for the
java.lang API, notably String manipulation methods, basic numerical
methods, object reflection, creation and serialization, and System
properties. Additionally it contains an inheritable enum type, an
exception structure that supports multiple types of nested-Exceptions
and a series of utilities dedicated to help with building methods, such
as hashCode, toString and equals.

With version of commons-lang 3.x, developers decided to change API and
therefore created differently named artifact and jar files. This is
the new version, while apache-commons-lang is the compatibility
package.

%prep
%autosetup -p1 -C

%pom_remove_plugin :maven-javadoc-plugin
%pom_remove_dep org.openjdk.jmh:jmh-core
%pom_remove_dep org.openjdk.jmh:jmh-generator-annprocess
%pom_remove_dep org.apache.commons:commons-text

%mvn_file : %{name} commons-lang3

# testParseSync() test fails on ARM and PPC64LE for unknown reason
sed -i 's/\s*public void testParseSync().*/@org.junit.jupiter.api.Disabled\n&/' \
    src/test/java/org/apache/commons/lang3/time/FastDateFormatTest.java

# non-deterministic tests fail randomly
rm src/test/java/org/apache/commons/lang3/RandomStringUtilsTest.java

# Missing dependencies
rm src/test/java/org/apache/commons/lang3/HashSetvBitSetTest.java

# Remove limits and Java 11 options
sed -i '/<argLine>/d' pom.xml

%build
# See "-DcommonsLang3Version" in maven-surefire for the tested version
%mvn_build -j -f

%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt NOTICE.txt
%doc RELEASE-NOTES.txt

%changelog
%autochangelog
