%bcond_with bootstrap

Name:           jline
Version:        3.29.0
Release:        %autorelease
Summary:        Java library for handling console input
License:        BSD-3-Clause AND Apache-2.0
URL:            https://github.com/jline/jline3
ExclusiveArch:  %{java_arches}

Source0:        %{url}/archive/jline-%{version}.tar.gz

# Fedora/RHEL specific: JNI shared objects MUST be placed in %{_prefix}/lib/%{name}
Patch:          0001-Load-native-library-form-usr-lib-jline.patch
# Patch out unwanted optional dependency on universalchardet
Patch:          0002-Remove-optional-dependency-on-universalchardet.patch

BuildRequires:  gcc
%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(com.google.code.findbugs:jsr305)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-dependency-plugin)
BuildRequires:  mvn(org.easymock:easymock)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter-api)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter-params)
%endif
# TODO remove in Fedora 46
Obsoletes:      %{name}-builtins < 3.29.0
Obsoletes:      %{name}-console < 3.29.0
Obsoletes:      %{name}-javadoc < 3.29.0
Obsoletes:      %{name}-native < 3.29.0
Obsoletes:      %{name}-parent < 3.29.0
Obsoletes:      %{name}-reader < 3.29.0
Obsoletes:      %{name}-remote-ssh < 3.29.0
Obsoletes:      %{name}-remote-telnet < 3.29.0
Obsoletes:      %{name}-style < 3.29.0
Obsoletes:      %{name}-terminal < 3.29.0
Obsoletes:      %{name}-terminal-jansi < 3.29.0
Obsoletes:      %{name}-terminal-jna < 3.29.0

%description
JLine is a Java library for handling console input.  It is similar in
functionality to BSD editline and GNU readline but with additional
features that bring it in par with the ZSH line editor.  Those familiar
with the readline/editline capabilities for modern shells (such as bash
and tcsh) will find most of the command editing features of JLine to be
familiar.

%prep
%autosetup -p1 -C
cp -p console-ui/LICENSE.txt LICENSE-APACHE.txt

# Remove prebuilt native objects
rm -r native/src/main/resources/org/jline/nativ/*/

# -Werror is considered harmful for downstream packaging
sed -i /-Werror/d $(find -name pom.xml)

# Optional dependency on juniversalchardet was removed via a patch
%pom_remove_dep -r :juniversalchardet

# Disable FFM module for now
# TODO enable FFM when switching to Java 25
%pom_disable_module terminal-ffm

# Disable unwanted modules
%pom_disable_module terminal-jna
%pom_disable_module terminal-jansi
%pom_disable_module groovy
%pom_disable_module remote-ssh
%pom_disable_module remote-telnet
%pom_disable_module curses
%pom_disable_module demo
%pom_disable_module graal

# Unnecessary plugins for an rpm build
%pom_remove_plugin :maven-enforcer-plugin
%pom_remove_plugin :spotless-maven-plugin

# There is no need to re-generate jni-config.json for GraalVM
# as is already present under native/src/main/resources/
%pom_remove_plugin :exec-maven-plugin native
%pom_remove_dep :picocli-codegen native

%build
# Build a native object
gcc -Wall %{build_cflags} -fPIC -fvisibility=hidden -shared -I native/src/main/native \
  -I %{_jvmdir}/java/include -I %{_jvmdir}/java/include/linux %{build_ldflags} \
  -o libjlinenative.so native/src/main/native/{jlinenative,clibrary}.c

# Build the Java artifacts
%mvn_build -j -- -P\!bundle -Dlibrary.jline.path=$PWD

%install
%mvn_install
install -d -m 755 %{buildroot}%{_prefix}/lib/%{name}/
install -p -m 755 libjlinenative.so %{buildroot}%{_prefix}/lib/%{name}/

%files -f .mfiles
%{_prefix}/lib/%{name}
%doc changelog.md README.md
%license LICENSE.txt LICENSE-APACHE.txt

%changelog
%autochangelog
