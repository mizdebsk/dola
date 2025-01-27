%bcond_with bootstrap

Name:           byte-buddy
Version:        1.14.2
Release:        %autorelease
Summary:        Runtime code generation for the Java virtual machine
License:        Apache-2.0
URL:            https://bytebuddy.net
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/raphw/byte-buddy/archive/refs/tags/byte-buddy-%{version}.tar.gz

# Patch the build to avoid bundling inside shaded jars
Patch:          0001-Avoid-bundling-asm.patch
Patch:          0002-Remove-dependencies.patch
Patch:          0003-Fix-broken-modular-jars.patch

BuildRequires:  jurand
%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(codes.rafael.modulemaker:modulemaker-maven-plugin)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(net.bytebuddy:byte-buddy)
BuildRequires:  mvn(net.bytebuddy:byte-buddy-dep)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugin-testing:maven-plugin-testing-harness)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  mvn(org.apache.maven:maven-compat)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(org.eclipse.aether:aether-api)
BuildRequires:  mvn(org.eclipse.aether:aether-util)
BuildRequires:  mvn(org.mockito:mockito-core)
BuildRequires:  mvn(org.ow2.asm:asm)
BuildRequires:  mvn(org.ow2.asm:asm-analysis)
BuildRequires:  mvn(org.ow2.asm:asm-commons)
BuildRequires:  mvn(org.ow2.asm:asm-util)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 1.14.2-25

%description
Byte Buddy is a code generation library for creating Java classes during the
runtime of a Java application and without the help of a compiler. Other than
the code generation utilities that ship with the Java Class Library, Byte Buddy
allows the creation of arbitrary classes and is not limited to implementing
interfaces for the creation of runtime proxies. 

%package agent
Summary:        Byte Buddy Java agent

%description agent
The Byte Buddy Java agent allows to access the JVM's HotSwap feature.

%package maven-plugin
Summary:        Byte Buddy Maven plugin

%description maven-plugin
A plugin for post-processing class files via Byte Buddy in a Maven build.

%prep
%autosetup -p1 -C


find -name '*.class' -delete

rm byte-buddy-agent/src/test/java/net/bytebuddy/agent/VirtualMachineAttachmentTest.java\
   byte-buddy-agent/src/test/java/net/bytebuddy/agent/VirtualMachineForOpenJ9Test.java\
   byte-buddy-agent/src/test/java/net/bytebuddy/test/utility/JnaRule.java\
;

# Don't ship android or benchmark modules
%pom_disable_module byte-buddy-android
%pom_disable_module byte-buddy-android-test
%pom_disable_module byte-buddy-benchmark

# Don't ship gradle plugin
%pom_disable_module byte-buddy-gradle-plugin

# Remove check plugins unneeded by RPM builds
%pom_remove_plugin :jacoco-maven-plugin
%pom_remove_plugin :license-maven-plugin
%pom_remove_plugin :pitest-maven
%pom_remove_plugin :coveralls-maven-plugin
%pom_remove_plugin :spotbugs-maven-plugin
%pom_remove_plugin :jitwatch-jarscan-maven-plugin
%pom_remove_plugin :maven-release-plugin
%pom_remove_plugin :nexus-staging-maven-plugin

# Avoid circural dependency
%pom_remove_plugin :byte-buddy-maven-plugin byte-buddy-dep

# Not interested in shading sources (causes NPE on old versions of shade plugin)
%pom_xpath_set "pom:createSourcesJar" "false" byte-buddy

# Drop build dep on findbugs annotations, used only by the above check plugins
%pom_remove_dep -r :findbugs-annotations
%java_remove_annotations byte-buddy-agent byte-buddy-dep byte-buddy-maven-plugin -n SuppressFBWarnings

%pom_remove_dep org.ow2.asm:asm-deprecated

%pom_remove_plugin -r :maven-shade-plugin
%pom_remove_dep -r net.java.dev.jna:jna
%pom_remove_dep -r net.java.dev.jna:jna-platform

%mvn_package :byte-buddy-parent __noinstall

%build
# Ignore test failures, there seems to be something different about the
# bytecode of our recompiled test resources, expect 6 test failures in
# the byte-buddy-dep module

# NOTE you can obtain valid profiles for precompilation by:
# xmllint --xpath '//*[local-name()="profile"]/*[local-name()="id"]/text()' byte-buddy-dep/pom.xml | grep 'precompile$' | grep -v 'no-precompile$' | sed 's/\(.*\)/-P\1/'
profiles='-Pjava-8-precompile -Pjava-8-parameters-precompile -Pjava-11-precompile -Pjava-16-precompile -Pjava-17-precompile'
%mvn_build -j -s -- -P'java8,!checks' "${profiles}" -Dsourcecode.main.version=8 -Dsourcecode.test.version=8 -Dmaven.test.failure.ignore=true

%install
%mvn_install

%files -f .mfiles-%{name} -f .mfiles-%{name}-dep
%doc README.md release-notes.md
%license LICENSE NOTICE

%files agent -f .mfiles-%{name}-agent
%license LICENSE NOTICE

%files maven-plugin -f .mfiles-%{name}-maven-plugin

%changelog
%autochangelog
