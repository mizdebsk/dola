%bcond_with bootstrap

Name:           plexus-compiler
Version:        2.15.0
Release:        %autorelease
Summary:        Compiler call initiators for Plexus
# extras subpackage has a bit different licensing
# parts of compiler-api are Apache-2.0/MIT
License:        MIT AND Apache-2.0
URL:            https://github.com/codehaus-plexus/plexus-compiler
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/codehaus-plexus/%{name}/archive/%{name}-%{version}.tar.gz
Source1:        https://www.apache.org/licenses/LICENSE-2.0.txt
Source2:        LICENSE.MIT

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(javax.inject:javax.inject)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.codehaus.plexus:plexus:pom:)
BuildRequires:  mvn(org.eclipse.sisu:org.eclipse.sisu.plexus)
BuildRequires:  mvn(org.eclipse.sisu:sisu-maven-plugin)
BuildRequires:  mvn(org.slf4j:slf4j-api)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 2.15.0-11

%description
Plexus Compiler adds support for using various compilers from a
unified api. Support for javac is available in main package. For
additional compilers see %{name}-extras package.

%package extras
Summary:        Extra compiler support for %{name}
# Apache-2.0: src/main/java/org/codehaus/plexus/compiler/util/scan/
#          ...codehaus/plexus/compiler/csharp/CSharpCompiler.java
# Apache-1.1/MIT: ...codehaus/plexus/compiler/jikes/JikesCompiler.java
License:        MIT AND Apache-2.0 AND Apache-1.1

%description extras
Additional support for csharp, eclipse and jikes compilers

%package pom
Summary:        Maven POM files for %{name}

%description pom
This package provides %{summary}.

%prep
%autosetup -p1 -C

find -name '.class' -delete

cp %{SOURCE1} LICENSE
cp %{SOURCE2} LICENSE.MIT

%pom_remove_dep :junit-bom

%pom_disable_module plexus-compiler-aspectj plexus-compilers
# missing com.google.errorprone:error_prone_core
%pom_disable_module plexus-compiler-javac-errorprone plexus-compilers

%pom_disable_module plexus-compiler-eclipse plexus-compilers

# don't build/install compiler-test module, it needs maven2 test harness
%pom_disable_module plexus-compiler-test
%pom_disable_module plexus-compiler-its

# don't install sources jars
%mvn_package ":*::sources:" __noinstall

%mvn_package ":plexus-compiler{,s}" pom
%mvn_package ":*{csharp,eclipse,jikes}*" extras

# don't generate requires on test dependency (see #1007498)
%pom_xpath_remove "pom:dependency[pom:artifactId[text()='plexus-compiler-test']]" plexus-compilers

%pom_remove_plugin :maven-site-plugin
%pom_remove_plugin :maven-enforcer-plugin

%pom_remove_dep -r org.codehaus.plexus:plexus-compiler-javac-errorprone
%pom_remove_dep org.codehaus.plexus:plexus-xml plexus-compiler-manager

%build
# Tests are skipped because of unavailable plexus-compiler-test artifact
%mvn_build -j -f

%install
%mvn_install

%files -f .mfiles
%license LICENSE LICENSE.MIT

%files extras -f .mfiles-extras

%files pom -f .mfiles-pom

%changelog
%autochangelog
