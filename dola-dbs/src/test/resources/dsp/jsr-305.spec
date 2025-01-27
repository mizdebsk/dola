%bcond_with bootstrap

Name:           jsr-305
Version:        3.0.2
Release:        %autorelease
Summary:        Correctness annotations for Java code
# The majority of code is BSD-licensed.
# JCIP annotations are Apache-licensed.
License:        BSD-3-Clause AND Apache-2.0
URL:            https://code.google.com/p/jsr-305
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

# ./generate-tarball.sh
Source0:        %{name}-%{version}.tar.gz
Source1:        https://github.com/stephenc/jcip-annotations/archive/refs/tags/jcip-annotations-1.0-1.tar.gz

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 3.0.2-39

%description
This package contains reference implementations, test cases, and other
documents for Java Specification Request 305: Annotations for Software Defect
Detection.

%prep
%autosetup -p1 -C

# Replace javax.annotation.concurrent annotations (that are based on
# code from https://jcip.net/ and are licensed under CC-BY-2.5, which
# is not Fedora-approved for code) with a clean-room implementation
# under Apache-2.0 from https://github.com/stephenc/jcip-annotations
tar xf %{SOURCE1}
rm -rf ri/src/main/java/javax/annotation/concurrent
mv jcip-annotations-jcip-annotations-1.0-1/src/main/java/net/jcip/annotations ri/src/main/java/javax/annotation/concurrent
sed -i /^package/s/net.jcip.annotations/javax.annotation.concurrent/ ri/src/main/java/javax/annotation/concurrent/*

%pom_xpath_set "pom:plugin[pom:artifactId='maven-compiler-plugin']/pom:configuration/*" 1.8
%pom_remove_plugin :maven-compiler-plugin ri

%pom_xpath_set '/pom:project/pom:groupId' 'org.jsr-305' ri/pom.xml
%pom_xpath_set '/pom:project/pom:artifactId' 'ri' ri/pom.xml

%mvn_file :ri %{name}
%mvn_alias :ri com.google.code.findbugs:jsr305
%mvn_package ":{proposedAnnotations,tcl}" __noinstall

# do not build sampleUses module - it causes Javadoc generation to fail
%pom_disable_module sampleUses

%pom_remove_parent ri
%pom_add_parent org.jsr-305:jsr-305:0.1-SNAPSHOT ri

%pom_remove_plugin org.sonatype.plugins:nexus-staging-maven-plugin ri
%pom_remove_plugin org.apache.maven.plugins:maven-source-plugin ri
%pom_remove_plugin org.apache.maven.plugins:maven-javadoc-plugin ri
%pom_remove_plugin org.apache.maven.plugins:maven-gpg-plugin ri

%build
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%license ri/LICENSE jcip-annotations-jcip-annotations-1.0-1/LICENSE.txt
%doc sampleUses

%changelog
%autochangelog
