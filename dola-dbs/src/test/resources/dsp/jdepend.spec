Name:           jdepend
Version:        2.10
Release:        %autorelease
Summary:        Java Design Quality Metrics
License:        MIT
URL:            https://github.com/clarkware/jdepend
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/clarkware/jdepend/archive/refs/tags/2.10.tar.gz#/jdepend-2.10.tar.gz

BuildRequires:  javapackages-local
BuildRequires:  ant
BuildRequires:  java-devel
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 2.10-27

%description
JDepend traverses a set of Java class and source file directories and
generates design quality metrics for each Java package. JDepend allows
you to automatically measure the quality of a design in terms of its
extensibility, reusability, and maintainability to effectively manage
and control package dependencies.

%prep
%autosetup -p1 -C
# remove all binary libs
find . -name "*.jar" -delete
# fix strange permissions
find . -type d -exec chmod 755 {} \;
find . -type f -exec chmod 644 {} \;

%mvn_file %{name}:%{name} %{name}

%build
%ant -Dant.build.javac.source=1.8 -Dant.build.javac.target=1.8 jar

%install
%mvn_artifact jdepend:jdepend:%{version} dist/%{name}-%{version}.jar
%mvn_install

%files -f .mfiles
%doc README.md CHANGELOG.md docs
%license LICENSE.md

%changelog
%autochangelog
