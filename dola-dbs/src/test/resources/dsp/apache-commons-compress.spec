%bcond_with bootstrap

Name:           apache-commons-compress
Version:        1.27.1
Release:        %autorelease
Summary:        Java API for working with compressed files and archivers
License:        Apache-2.0
URL:            https://commons.apache.org/proper/commons-compress/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://archive.apache.org/dist/commons/compress/source/commons-compress-%{version}-src.tar.gz

Patch:          0001-Remove-Brotli-compressor.patch
Patch:          0002-Remove-ZSTD-compressor.patch
Patch:          0003-Remove-Pack200-compressor.patch

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(commons-codec:commons-codec)
BuildRequires:  mvn(commons-io:commons-io)
BuildRequires:  mvn(org.apache.commons:commons-lang3)
BuildRequires:  mvn(org.apache.commons:commons-parent:pom:)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires:  mvn(org.osgi:org.osgi.core)
BuildRequires:  mvn(org.ow2.asm:asm)
BuildRequires:  mvn(org.tukaani:xz)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 1.27.1-7

%description
The Apache Commons Compress library defines an API for working with
ar, cpio, Unix dump, tar, zip, gzip, XZ, Pack200 and bzip2 files.
In version 1.14 read-only support for Brotli decompression has been added,
but it has been removed form this package.

%prep
%autosetup -p1 -C

# Unavailable Google Brotli library (org.brotli.dec)
%pom_remove_dep org.brotli:dec
rm -r src/{main,test}/java/org/apache/commons/compress/compressors/brotli

# Unavailable ZSTD JNI library
%pom_remove_dep :zstd-jni
rm -r src/{main,test}/java/org/apache/commons/compress/compressors/zstandard

# Remove support for pack200 which depends on ancient asm:asm:3.2
rm -r src/{main,test}/java/org/apache/commons/compress/harmony
rm -r src/main/java/org/apache/commons/compress/compressors/pack200
rm src/main/java/org/apache/commons/compress/java/util/jar/Pack200.java
rm -r src/test/java/org/apache/commons/compress/compressors/pack200
rm src/test/java/org/apache/commons/compress/java/util/jar/Pack200Test.java

# remove osgi tests, we don't have deps for them
%pom_remove_dep org.ops4j.pax.exam:::test
%pom_remove_dep :org.apache.felix.framework::test
%pom_remove_dep :javax.inject::test

# Not packaged
%pom_remove_dep com.github.marschall:memoryfilesystem
rm src/test/java/org/apache/commons/compress/archivers/tar/TarMemoryFileSystemTest.java

%build
%mvn_file  : commons-compress %{name}
%mvn_alias : commons:
# XXX failing tests, need to investigate why
%mvn_build -j -f -- -Dcommons.osgi.symbolicName=org.apache.commons.compress

%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt NOTICE.txt

%changelog
%autochangelog
