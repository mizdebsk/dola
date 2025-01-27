%bcond_with bootstrap

Name:           qdox
Version:        2.1.0
Release:        %autorelease
Summary:        Extract class/interface/method definitions from sources
License:        Apache-2.0
URL:            https://github.com/paul-hammant/qdox
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

# ./generate-tarball.sh
Source0:        %{name}-%{version}.tar.gz
Source1:        qdox-MANIFEST.MF
# Remove bundled binaries which are possibly proprietary
Source2:        generate-tarball.sh

Patch:          qdox-port-tests-to-java-21.patch

BuildRequires:  byaccj
%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  jflex
BuildRequires:  mvn(org.assertj:assertj-core)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter)
BuildRequires:  mvn(org.mockito:mockito-core)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 2.1.0-15

%description
QDox is a high speed, small footprint parser
for extracting class/interface/method definitions
from source files complete with JavaDoc @tags.
It is designed to be used by active code
generators or documentation tools.

%prep
%autosetup -p1 -C

# remove unnecessary dependency on parent POM
%pom_remove_parent

# We don't need these plugins
%pom_remove_plugin :animal-sniffer-maven-plugin
%pom_remove_plugin :maven-assembly-plugin
%pom_remove_plugin :maven-failsafe-plugin
%pom_remove_plugin :maven-invoker-plugin
%pom_remove_plugin :jflex-maven-plugin
%pom_remove_plugin :maven-enforcer-plugin
%pom_remove_plugin :exec-maven-plugin

%mvn_file : %{name}
%mvn_alias : qdox:qdox

%build
%{?jpb_env}

# Generate scanners (upstream does this with maven-jflex-plugin)
jflex -d src/main/java/com/thoughtworks/qdox/parser/impl src/grammar/lexer.flex
jflex -d src/main/java/com/thoughtworks/qdox/parser/impl src/grammar/commentlexer.flex

# Generate parsers (upstream does this with exec-maven-plugin)
(cd ./src/main/java/com/thoughtworks/qdox/parser/impl
 byaccj -v -Jnorun -Jnoconstruct -Jclass=DefaultJavaCommentParser -Jpackage=com.thoughtworks.qdox.parser.impl ../../../../../../../grammar/commentparser.y
 byaccj -v -Jnorun -Jnoconstruct -Jclass=Parser -Jimplements=CommentHandler -Jsemantic=Value -Jpackage=com.thoughtworks.qdox.parser.impl -Jstack=500 ../../../../../../../grammar/parser.y
)

# Build artifact
%mvn_build -j -- -Dmaven.compiler.source=1.8 -Dmaven.compiler.target=1.8

# Inject OSGi manifests
%jar ufm target/%{name}-%{version}.jar %{SOURCE1}

%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt
%doc README.md

%changelog
%autochangelog
