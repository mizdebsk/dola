Name:           xml-commons-apis
Version:        1.4.01
Release:        %autorelease
Summary:        APIs for DOM, SAX, and JAXP
License:        Apache-2.0 AND W3C AND SAX-PD-2.0
URL:            https://xerces.apache.org/xml-commons/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

# From source control because the published tarball doesn't include some docs:
#   svn export http://svn.apache.org/repos/asf/xml/commons/tags/xml-commons-external-1_4_01/java/external/
#   tar czf xml-commons-external-1.4.01-src.tar.gz external
Source0:        xml-commons-external-%{version}-src.tar.gz
Source1:        %{name}-MANIFEST.MF
Source2:        %{name}-ext-MANIFEST.MF
Source3:        http://repo1.maven.org/maven2/xml-apis/xml-apis/2.0.2/xml-apis-2.0.2.pom
Source4:        http://repo1.maven.org/maven2/xml-apis/xml-apis-ext/1.3.04/xml-apis-ext-1.3.04.pom

BuildRequires:  javapackages-local
BuildRequires:  ant
BuildRequires:  apache-parent
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 1.4.01-59
Provides:       xml-commons = %{version}-%{release}

%description
xml-commons-apis is designed to organize and have common packaging for
the various externally-defined standard interfaces for XML. This
includes the DOM, SAX, and JAXP.

%prep
%autosetup -p1 -C
# Make sure upstream hasn't sneaked in any jars we don't know about
find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

# Fix file encodings
iconv -f iso8859-1 -t utf-8 LICENSE.dom-documentation.txt > \
  LICENSE.dom-doc.temp && mv -f LICENSE.dom-doc.temp LICENSE.dom-documentation.txt
iconv -f iso8859-1 -t utf-8 LICENSE.dom-software.txt > \
  LICENSE.dom-sof.temp && mv -f LICENSE.dom-sof.temp LICENSE.dom-software.txt

# remove bogus section from poms
cp %{SOURCE3} %{SOURCE4} .
sed -i '/distributionManagement/,/\/distributionManagement/ {d}' *.pom

%mvn_file :xml-apis xml-commons-apis jaxp13 jaxp xml-commons-jaxp-1.3-apis
%mvn_file :xml-apis-ext xml-commons-apis-ext
%mvn_alias :xml-apis-ext xerces:dom3-xml-apis

%build
%ant -Dant.build.javac.source=1.8 -Dant.build.javac.target=1.8 jar

# inject OSGi manifests
jar ufm build/xml-apis.jar %{SOURCE1}
jar ufm build/xml-apis-ext.jar %{SOURCE2}

%mvn_artifact xml-apis-[0-9]*.pom build/xml-apis.jar
%mvn_artifact xml-apis-ext*.pom build/xml-apis-ext.jar

%install
%mvn_install

# prevent apis javadoc from being included in doc
rm -rf build/docs/javadoc

%files -f .mfiles
%doc LICENSE NOTICE
%doc LICENSE.dom-documentation.txt README.dom.txt
%doc LICENSE.dom-software.txt LICENSE.sac.html
%doc LICENSE.sax.txt README-sax  README.sax.txt

%changelog
%autochangelog
