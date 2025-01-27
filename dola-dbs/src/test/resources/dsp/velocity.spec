%bcond_with bootstrap

Name:           velocity
Version:        2.3
Release:        %autorelease
Summary:        Java-based template engine
License:        Apache-2.0
URL:            https://velocity.apache.org
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/apache/velocity-engine/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz

Patch:          0001-Template-is-a-reserved-keyword-in-javacc.patch

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(commons-io:commons-io)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.commons:commons-lang3)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-enforcer-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:  mvn(org.codehaus.mojo:extra-enforcer-rules)
BuildRequires:  mvn(org.codehaus.mojo:javacc-maven-plugin)
BuildRequires:  mvn(org.slf4j:slf4j-api)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 2.3-21

%description
Velocity is a Java-based template engine. It permits anyone to use the
simple yet powerful template language to reference objects defined in
Java code.
When Velocity is used for web development, Web designers can work in
parallel with Java programmers to develop web sites according to the
Model-View-Controller (MVC) model, meaning that web page designers can
focus solely on creating a site that looks good, and programmers can
focus solely on writing top-notch code. Velocity separates Java code
from the web pages, making the web site more maintainable over the long
run and providing a viable alternative to Java Server Pages (JSPs) or
PHP.
Velocity's capabilities reach well beyond the realm of web sites; for
example, it can generate SQL and PostScript and XML (see Anakia for more
information on XML transformations) from templates. It can be used
either as a standalone utility for generating source code and reports,
or as an integrated component of other systems. Velocity also provides
template services for the Turbine web application framework.
Velocity+Turbine provides a template service that will allow web
applications to be developed according to a true MVC model.

%prep
%autosetup -p1 -C

%mvn_alias : velocity:velocity
%mvn_alias : org.apache.velocity:velocity

%pom_remove_parent
%pom_xpath_inject pom:project "<groupId>org.apache.velocity</groupId>"

%pom_disable_module spring-velocity-support
%pom_disable_module velocity-custom-parser-example
%pom_disable_module velocity-engine-examples
%pom_disable_module velocity-engine-scripting

%pom_remove_plugin :maven-javadoc-plugin

%pom_remove_plugin :templating-maven-plugin velocity-engine-core
sed 's/${project.version}/%{version}/' \
    velocity-engine-core/src/main/java-templates/org/apache/velocity/runtime/VelocityEngineVersion.java \
   >velocity-engine-core/src/main/java/org/apache/velocity/runtime/VelocityEngineVersion.java

%pom_remove_plugin com.google.code.maven-replacer-plugin:replacer velocity-engine-core
%pom_remove_plugin :maven-shade-plugin velocity-engine-core

%pom_xpath_remove "pom:dependency[pom:scope='test']" velocity-engine-core

%build
%mvn_build -j -f -- -Djavacc.visitor=false

%install
%mvn_install

%files -f .mfiles
%doc README.md
%license LICENSE NOTICE

%changelog
%autochangelog
