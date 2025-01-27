%bcond_with bootstrap

Name:           apache-commons-io
Epoch:          1
Version:        2.16.1
Release:        %autorelease
Summary:        Utilities to assist with developing IO functionality
License:        Apache-2.0
URL:            https://commons.apache.org/proper/commons-io/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://archive.apache.org/dist/commons/io/source/commons-io-%{version}-src.tar.gz

BuildRequires:  jurand
%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.commons:commons-lang3)
BuildRequires:  mvn(org.apache.commons:commons-parent:pom:)
BuildRequires:  mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter)
BuildRequires:  mvn(org.mockito:mockito-core)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 1:2.16.1-13

%description
Commons-IO contains utility classes, stream implementations,
file filters, and endian classes. It is a library of utilities
to assist with developing IO functionality.

%prep
%autosetup -p1 -C

sed -i 's/\r//' *.txt

# Run tests in multiple reusable forks to improve test performance
sed -i -e /reuseForks/d -e /forkCount/d pom.xml
sed -i '/<argLine>/d' pom.xml

%mvn_file : commons-io %{name}
%mvn_alias : org.apache.commons:

%pom_remove_dep org.junit-pioneer:junit-pioneer
%java_remove_annotations src -s -n DefaultLocale

%pom_remove_dep com.google.jimfs:jimfs
rm src/test/java/org/apache/commons/io/input/ReversedLinesFileReaderTestParamFile.java

%build
# See "-DcommonsIoVersion" in maven-surefire for the tested version

# The following tests fail on tmpfs/nfs:
#  * PathUtilsDeleteDirectoryTest.testDeleteDirectory1FileSize0OverrideReadOnly:80->testDeleteDirectory1FileSize0:68 » FileSystem
#  * PathUtilsDeleteFileTest.testDeleteReadOnlyFileDirectory1FileSize1:114 » FileSystem
#  * PathUtilsDeleteFileTest.testSetReadOnlyFileDirectory1FileSize1:134 » FileSystem
#  * PathUtilsDeleteTest.testDeleteDirectory1FileSize0OverrideReadonly:97->testDeleteDirectory1FileSize0:69 » FileSystem
#  * PathUtilsDeleteTest.testDeleteDirectory1FileSize1OverrideReadOnly:145->testDeleteDirectory1FileSize1:117 » FileSystem

# moditect profile generates module-info.class
%mvn_build -j -f -- -Dcommons.osgi.symbolicName=org.apache.commons.io

%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt NOTICE.txt
%doc RELEASE-NOTES.txt

%changelog
%autochangelog
