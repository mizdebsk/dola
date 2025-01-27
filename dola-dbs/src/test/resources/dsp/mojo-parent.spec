%bcond_with bootstrap

Name:           mojo-parent
Version:        85
Release:        %autorelease
Summary:        Codehaus MOJO parent project pom file
License:        Apache-2.0
URL:            https://www.mojohaus.org/mojo-parent/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://repo1.maven.org/maven2/org/codehaus/mojo/mojo-parent/%{version}/mojo-parent-%{version}-source-release.zip
Source1:        https://www.apache.org/licenses/LICENSE-2.0.txt

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.maven.plugins:maven-assembly-plugin)
%endif

%description
Codehaus MOJO parent project pom file

%prep
%autosetup -p1 -C
# Not needed in Fedora.
%pom_remove_plugin :maven-enforcer-plugin
%pom_remove_plugin :maven-site-plugin
%pom_remove_plugin :maven-checkstyle-plugin
%pom_remove_plugin :spotless-maven-plugin
%pom_remove_dep :junit-bom

cp %SOURCE1 .

%build
%mvn_alias : org.codehaus.mojo:mojo
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%doc LICENSE-2.0.txt

%changelog
%autochangelog
