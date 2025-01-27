%bcond_with bootstrap
%global pkg_version 11b

Name:           java_cup
Epoch:          1
Version:        0.11b
Release:        %autorelease
Summary:        LALR parser generator for Java
License:        SMLNJ
URL:            https://www2.cs.tum.edu/projects/cup/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

# svn export -r 65 https://www2.in.tum.de/repos/cup/develop/ java_cup-0.11b
# tar cjf java_cup-0.11b.tar.bz2 java_cup-0.11b/
Source0:        java_cup-%{version}.tar.bz2
# Add OSGi manifests
Source2:        %{name}-MANIFEST.MF
Source4:        %{name}-runtime-MANIFEST.MF

Patch:          %{name}-build.patch
Patch:          0002-Set-Java-source-target-to-1.8.patch

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  javapackages-local
BuildRequires:  ant
BuildRequires:  java_cup
BuildRequires:  jflex
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 1:0.11b-57

%description
java_cup is a LALR Parser Generator for Java

%package manual
Summary:        Documentation for java_cup

%description manual
Documentation for java_cup.

%prep
%autosetup -p1 -C

# remove all binary files
find -name "*.class" -delete

%mvn_file ':{*}' @1

# remove prebuilt JFlex
rm -rf java_cup-%{version}/bin/JFlex.jar

# remove prebuilt java_cup, if not bootstrapping
rm -rf java_cup-%{version}/bin/java-cup-11.jar

%build
export CLASSPATH=$(build-classpath java_cup java_cup-runtime jflex)

%ant -Dcupversion=20150326 -Dsvnversion=65

# inject OSGi manifests
%jar ufm dist/java-cup-%{pkg_version}.jar %{SOURCE2}
%jar ufm dist/java-cup-%{pkg_version}-runtime.jar %{SOURCE4}

%install
%mvn_artifact %{name}:%{name}:%{version} dist/java-cup-%{pkg_version}.jar
%mvn_artifact %{name}:%{name}-runtime:%{version} dist/java-cup-%{pkg_version}-runtime.jar

%mvn_install

# wrapper script for direct execution
%jpackage_script java_cup.Main "" "" java_cup cup true

%files -f .mfiles
%{_bindir}/cup
%doc changelog.txt
%license licence.txt

%files manual
%doc manual.html
%license licence.txt

%changelog
%autochangelog
