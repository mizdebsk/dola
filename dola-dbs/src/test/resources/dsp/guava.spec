%bcond_with bootstrap

Name:           guava
Version:        33.3.0
Release:        %autorelease
Summary:        Google Core Libraries for Java
# Most of the code is under Apache-2.0
# Few classes are under CC0-1.0 grep for creativecommons
License:        Apache-2.0 AND CC0-1.0
URL:            https://github.com/google/guava
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/google/guava/archive/v%{version}/guava-%{version}.tar.gz

BuildRequires:  jurand
%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(com.google.code.findbugs:jsr305)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-enforcer-plugin)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 33.3.0-8

%description
Guava is a suite of core and expanded libraries that include
utility classes, Google’s collections, io classes, and much
much more.
This project is a complete packaging of all the Guava libraries
into a single jar.  Individual portions of Guava can be used
by downloading the appropriate module and its dependencies.

%package testlib
Summary:        The guava-testlib artifact

%description testlib
guava-testlib provides additional functionality for conveninent unit testing

%prep
%autosetup -p1 -C

find . -name '*.jar' -delete

%pom_remove_parent guava-bom

%pom_disable_module guava-gwt
%pom_disable_module guava-tests

%pom_xpath_inject pom:modules "<module>futures/failureaccess</module>"
%pom_xpath_inject pom:parent "<relativePath>../..</relativePath>" futures/failureaccess
%pom_xpath_set pom:parent/pom:version %{version}-jre futures/failureaccess

%pom_remove_plugin -r :animal-sniffer-maven-plugin
%pom_remove_plugin -r :maven-source-plugin

%pom_remove_plugin -r :toolchains-maven-plugin
%pom_remove_plugin -r :maven-toolchains-plugin
%pom_xpath_remove pom:jdkToolchain

%pom_remove_dep :caliper guava-tests

%mvn_package :guava-parent guava

# javadoc generation fails due to strict doclint in JDK 1.8.0_45
%pom_remove_plugin -r :maven-javadoc-plugin

%pom_remove_plugin -r :build-helper-maven-plugin

%pom_xpath_inject /pom:project/pom:build/pom:plugins/pom:plugin/pom:configuration/pom:instructions "<_nouses>true</_nouses>" guava/pom.xml

# missing error_prone_core artifact
%pom_xpath_remove pom:annotationProcessorPaths
sed -i /Xplugin:ErrorProne/d pom.xml

%pom_remove_dep -r :error_prone_annotations
%pom_remove_dep -r :j2objc-annotations
%pom_remove_dep -r org.checkerframework:
%pom_remove_dep -r :listenablefuture

%java_remove_annotations guava guava-testlib -s \
  -p org[.]checkerframework[.] \
  -p com[.]google[.]common[.]annotations[.] \
  -p com[.]google[.]errorprone[.]annotations[.] \
  -p com[.]google[.]j2objc[.]annotations[.] \

%mvn_package "com.google.guava:failureaccess" guava

%mvn_package "com.google.guava:guava-bom" __noinstall

%build
# Tests fail on Koji due to insufficient memory,
# see https://bugzilla.redhat.com/show_bug.cgi?id=1332971
%mvn_build -j -s -f

%install
%mvn_install

%files -f .mfiles-guava
%doc CONTRIBUTORS README*
%license LICENSE

%files testlib -f .mfiles-guava-testlib

%changelog
%autochangelog
