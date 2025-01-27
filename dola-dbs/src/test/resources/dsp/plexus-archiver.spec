%bcond_with bootstrap

Name:           plexus-archiver
Version:        4.10.0
Release:        %autorelease
Summary:        Plexus Archiver Component
License:        Apache-2.0
URL:            https://codehaus-plexus.github.io/plexus-archiver
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/codehaus-plexus/plexus-archiver/archive/plexus-archiver-%{version}.tar.gz

Patch:          0001-Remove-support-for-snappy.patch
Patch:          0002-Remove-support-for-zstd.patch

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(com.google.code.findbugs:jsr305)
BuildRequires:  mvn(com.google.inject:guice)
BuildRequires:  mvn(commons-io:commons-io)
BuildRequires:  mvn(javax.inject:javax.inject)
BuildRequires:  mvn(org.apache.commons:commons-compress)
BuildRequires:  mvn(org.assertj:assertj-core)
BuildRequires:  mvn(org.codehaus.plexus:plexus-io)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.codehaus.plexus:plexus:pom:)
BuildRequires:  mvn(org.eclipse.sisu:org.eclipse.sisu.inject)
BuildRequires:  mvn(org.eclipse.sisu:sisu-maven-plugin)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter-api)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter-params)
BuildRequires:  mvn(org.slf4j:slf4j-api)
BuildRequires:  mvn(org.slf4j:slf4j-simple)
BuildRequires:  mvn(org.tukaani:xz)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 4.10.0-6

%description
The Plexus project seeks to create end-to-end developer tools for
writing applications. At the core is the container, which can be
embedded or for a full scale application server. There are many
reusable components for hibernate, form processing, jndi, i18n,
velocity, etc. Plexus also includes an application server which
is like a J2EE application server, without all the baggage.

%prep
%autosetup -p1 -C

%mvn_file :%{name} plexus/archiver

%pom_remove_dep io.airlift:aircompressor
rm -r src/main/java/org/codehaus/plexus/archiver/snappy
rm -r src/test/java/org/codehaus/plexus/archiver/snappy
rm src/main/java/org/codehaus/plexus/archiver/tar/SnappyTarFile.java
rm src/main/java/org/codehaus/plexus/archiver/tar/PlexusIoTarSnappyFileResourceCollection.java
rm src/test/java/org/codehaus/plexus/archiver/tar/TarSnappyUnArchiverTest.java

%pom_remove_dep com.github.luben:zstd-jni
rm -r src/main/java/org/codehaus/plexus/archiver/zstd
rm -r src/test/java/org/codehaus/plexus/archiver/zstd
rm src/main/java/org/codehaus/plexus/archiver/tar/ZstdTarFile.java
rm src/main/java/org/codehaus/plexus/archiver/tar/PlexusIoTarZstdFileResourceCollection.java
rm src/main/java/org/codehaus/plexus/archiver/tar/PlexusIoTZstdFileResourceCollection.java
rm src/test/java/org/codehaus/plexus/archiver/tar/TarZstdUnArchiverTest.java

# Fails due to previously removed compressors
rm src/test/java/org/codehaus/plexus/archiver/manager/ArchiverManagerTest.java

%build
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%license LICENSE

%changelog
%autochangelog
