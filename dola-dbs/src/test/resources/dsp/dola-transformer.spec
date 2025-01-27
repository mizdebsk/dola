Name:           dola-transformer
Version:        0^20250515.102327.git.e03f39a
Release:        %autorelease
Summary:        Maven 4 extension for dynamic POM transformation
License:        Apache-2.0
URL:            https://github.com/mizdebsk/dola-transformer
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source:         dola-transformer-snapshot-20250515.102327-e03f39a.tar.zst

BuildRequires:  maven-local
BuildRequires:  mvn(io.kojan:kojan-parent:pom:)
BuildRequires:  mvn(javax.inject:javax.inject)
BuildRequires:  mvn(org.apache.maven:maven-api-model:4.0.0-rc-3)
BuildRequires:  mvn(org.apache.maven:maven-api-spi:4.0.0-rc-3)
BuildRequires:  mvn(org.eclipse.sisu:sisu-maven-plugin)

%description
Dola Transformer is an extension for Apache Maven 4 that enables
dynamic, in-memory transformation of project models (POMs) without
modifying them on disk.  It supports a range of transformations,
including adding or removing plugins, dependencies, and parent POMs.

Unlike traditional POM modification tools from the Javapackages
project, Dola Transformer works with a variety of model formats and is
not limited to XML.  This makes it especially useful in environments
where custom Maven builds are needed without manually editing POM
files.

%prep
%autosetup -p1 -C

%build
# TODO enable tests once EasyMock is updated to version >= 5.
# Tests require EasyMock 5, but we only have EasyMock 4 packaged.
%mvn_build -j -f

%install
%mvn_install

%files -f .mfiles
%license LICENSE NOTICE
%doc README.md

%changelog
%autochangelog
