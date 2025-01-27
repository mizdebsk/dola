%bcond_with bootstrap

Name:           jansi
Version:        2.4.1
Release:        %autorelease
Summary:        Generate and interpret ANSI escape sequences in Java
License:        Apache-2.0
URL:            https://fusesource.github.io/jansi/
ExclusiveArch:  %{java_arches}

# ./generate-tarball.sh
Source0:        %{name}-%{version}.tar.gz
# Remove bundled binaries which cannot be easily verified for licensing
Source1:        generate-tarball.sh

# Change the location of the native artifact to where Fedora wants it
Patch:          %{name}-jni.patch

BuildRequires:  gcc
%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:  mvn(org.fusesource:fusesource-pom:pom:)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter-params)
BuildRequires:  mvn(org.moditect:moditect-maven-plugin)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 2.4.1-16

%description
Jansi is a small java library that allows you to use ANSI escape sequences
in your Java console applications. It implements ANSI support on platforms
which don't support it like Windows and provides graceful degradation for
when output is being sent to output devices which cannot support ANSI sequences.

%prep
%autosetup -p1 -C

# We don't need the Fuse JXR skin
%pom_xpath_remove "pom:build/pom:extensions"

# Plugins not needed for an RPM build
%pom_remove_plugin :maven-gpg-plugin
%pom_remove_plugin :maven-javadoc-plugin
%pom_remove_plugin :nexus-staging-maven-plugin
%pom_remove_plugin :spotless-maven-plugin

# We don't want GraalVM support in Fedora
%pom_remove_plugin :exec-maven-plugin
%pom_remove_dep :picocli-codegen

# Set the JNI path
sed -i 's,@LIBDIR@,%{_prefix}/lib,' \
    src/main/java/org/fusesource/jansi/internal/JansiLoader.java

%build
%set_build_flags
CC="${CC:-gcc}"
# Build the native artifact
CFLAGS="$CFLAGS -I. -I%{java_home}/include -I%{java_home}/include/linux -fPIC -fvisibility=hidden"
cd src/main/native
$CC $CFLAGS -c jansi.c
$CC $CFLAGS -c jansi_isatty.c
$CC $CFLAGS -c jansi_structs.c
$CC $CFLAGS -c jansi_ttyname.c
$CC $CFLAGS $LDFLAGS -shared -o libjansi.so *.o -lutil
cd -

# Build the Java artifacts
%mvn_build -j -- -Dlibrary.jansi.path=$PWD/src/main/native

%install
# Install the native artifact
mkdir -p %{buildroot}%{_prefix}/lib/%{name}
cp -p src/main/native/libjansi.so %{buildroot}%{_prefix}/lib/%{name}

# Install the Java artifacts
%mvn_install

%files -f .mfiles
%license license.txt
%doc readme.md changelog.md
%{_prefix}/lib/%{name}/

%changelog
%autochangelog
