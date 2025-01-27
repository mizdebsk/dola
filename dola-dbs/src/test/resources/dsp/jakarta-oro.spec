%global base_name oro

Name:           jakarta-oro
Version:        2.0.8
Release:        %autorelease
Summary:        Full regular expressions API
License:        Apache-1.1
URL:            https://jakarta.apache.org/oro/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        http://archive.apache.org/dist/jakarta/oro/%{name}-%{version}.tar.gz
Source1:        MANIFEST.MF
Source2:        http://repo1.maven.org/maven2/%{base_name}/%{base_name}/%{version}/%{base_name}-%{version}.pom

Patch:          %{name}-build-xml.patch

BuildRequires:  javapackages-local
BuildRequires:  ant
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 2.0.8-53
Provides:       deprecated()

%description
The Jakarta-ORO Java classes are a set of text-processing Java classes
that provide Perl5 compatible regular expressions, AWK-like regular
expressions, glob expressions, and utility classes for performing
substitutions, splits, filtering filenames, etc. This library is the
successor to the OROMatcher, AwkTools, PerlTools, and TextTools
libraries from ORO, Inc. (www.oroinc.com). 

%prep
%autosetup -p1 -C
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;
# remove all CVS files
for dir in `find . -type d -name CVS`; do rm -rf $dir; done
for file in `find . -type f -name .cvsignore`; do rm -rf $file; done

cp %{SOURCE1} .

%build
ant -Dfinal.name=%{base_name} jar -Dant.build.javac.source=1.8 -Dant.build.javac.target=1.8

%install
%mvn_file : %{name} %{base_name}
%mvn_artifact %{SOURCE2} %{base_name}.jar

%mvn_install

%files -f .mfiles
%doc COMPILE ISSUES README TODO CHANGES CONTRIBUTORS STYLE
%license LICENSE

%changelog
%autochangelog
