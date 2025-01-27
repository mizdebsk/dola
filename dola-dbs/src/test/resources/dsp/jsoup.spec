%bcond_with bootstrap

Name:           jsoup
Version:        1.18.1
Release:        %autorelease
Summary:        Java library for working with real-world HTML
License:        MIT
URL:            https://jsoup.org/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

# ./generate-tarball.sh
Source0:        %{name}-%{version}.tar.gz
# The sources contain non-free scraped web pages as test data
Source1:        generate-tarball.sh

BuildRequires:  jurand
%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 1.18.1-11

%description
jsoup is a Java library for working with real-world HTML. It provides a very
convenient API for fetching URLs and extracting and manipulating data, using the
best of HTML5 DOM methods and CSS selectors.

jsoup implements the WHATWG HTML5 specification, and parses HTML to the same DOM
as modern browsers do.
* scrape and parse HTML from a URL, file, or string
* find and extract data, using DOM traversal or CSS selectors
* manipulate the HTML elements, attributes, and text
* clean user-submitted content against a safelist, to prevent XSS attacks
* output tidy HTML

jsoup is designed to deal with all varieties of HTML found in the wild; from
pristine and validating, to invalid tag-soup; jsoup will create a sensible parse
tree.

%prep
%autosetup -p1 -C

%pom_remove_plugin :animal-sniffer-maven-plugin
%pom_remove_plugin :maven-failsafe-plugin
%pom_remove_plugin :maven-javadoc-plugin
%pom_remove_plugin com.github.siom79.japicmp:japicmp-maven-plugin

# Expose internal packages in the OSGi metadata, clearly marking them as such
# using the x-internal attribute
%pom_xpath_inject "pom:plugin[pom:artifactId='maven-bundle-plugin']/pom:configuration/pom:instructions" \
  "<_exportcontents>*.internal;x-internal:=true,*</_exportcontents>"

# Remove jspecify annotations which are used for static analysis only
%pom_remove_dep :jspecify
sed -i /org.jspecify/d src/main/java9/module-info.java
%java_remove_annotations src/main/java -s \
  -p org[.]jspecify[.]annotations[.] \

%build
%mvn_build -j -f

%install
%mvn_install

%files -f .mfiles
%doc README.md CHANGES.md
%license LICENSE

%changelog
%autochangelog
