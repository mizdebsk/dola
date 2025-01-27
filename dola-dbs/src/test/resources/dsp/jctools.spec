%bcond_with bootstrap
%global srcname JCTools

Name:           jctools
Version:        4.0.2
Release:        %autorelease
Summary:        Java Concurrency Tools for the JVM
License:        Apache-2.0
URL:            https://github.com/JCTools/JCTools
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        %{url}/archive/v%{version}/%{srcname}-%{version}.tar.gz

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(com.google.guava:guava-testlib)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.hamcrest:hamcrest-all)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 4.0.2-15

%description
This project aims to offer some concurrent data structures
currently missing from the JDK:

° SPSC/MPSC/SPMC/MPMC Bounded lock free queues
° SPSC/MPSC Unbounded lock free queues
° Alternative interfaces for queues
° Offheap concurrent ring buffer for ITC/IPC purposes
° Single Writer Map/Set implementations
° Low contention stats counters
° Executor

%prep
%autosetup -p1 -C

# drop some failure-prone tests (race conditions?)
rm jctools-core/src/test/java/org/jctools/queues/MpqSanityTestMpscCompound.java

# set correct version in all pom.xml files
%pom_xpath_set pom:project/pom:version %{version}
%pom_xpath_set pom:parent/pom:version %{version} jctools-{build,core,channels,experimental}

# remove plugins unnecessary for RPM builds
%pom_remove_plugin :coveralls-maven-plugin jctools-core
%pom_remove_plugin :jacoco-maven-plugin jctools-core
%pom_remove_plugin :maven-enforcer-plugin
%pom_remove_plugin :maven-source-plugin jctools-core
%pom_remove_plugin :maven-javadoc-plugin jctools-core

# remove tests with additional kotlin dependencies
rm -r jctools-core/src/test/java/org/jctools/maps/linearizability_test/

# disable unused modules with unavailable dependencies
%pom_disable_module jctools-benchmarks
%pom_disable_module jctools-concurrency-test

# incompatible with Java 11 and unused in fedora:
# https://github.com/JCTools/JCTools/issues/254
%pom_disable_module jctools-channels
%pom_disable_module jctools-experimental

%pom_disable_module jctools-build
%pom_remove_plugin :exec-maven-plugin jctools-core

# do not install internal build tools
%mvn_package :jctools-build __noinstall

# do not install unused parent POM
%mvn_package :jctools-parent __noinstall

%build
# Tests time out in Koji
%mvn_build -j -s -f

%install
%mvn_install

%files -f .mfiles-jctools-core
%doc README.md
%license LICENSE

%changelog
%autochangelog
