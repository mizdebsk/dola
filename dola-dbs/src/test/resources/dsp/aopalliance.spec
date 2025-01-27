%bcond_with bootstrap

Name:           aopalliance
Version:        1.0
Release:        %autorelease
Summary:        Java/J2EE AOP standards
License:        LicenseRef-Fedora-Public-Domain
URL:            https://aopalliance.sourceforge.net
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

# cvs -d:pserver:anonymous@aopalliance.cvs.sourceforge.net:/cvsroot/aopalliance login
# password empty
# cvs -z3 -d:pserver:anonymous@aopalliance.cvs.sourceforge.net:/cvsroot/aopalliance export -r HEAD aopalliance
Source0:        aopalliance-src.tar.gz
Source1:        http://repo1.maven.org/maven2/aopalliance/aopalliance/1.0/aopalliance-1.0.pom
Source2:        %{name}-MANIFEST.MF

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  javapackages-local
BuildRequires:  ant
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 1.0-56

%description
Aspect-Oriented Programming (AOP) offers a better solution to many
problems than do existing technologies, such as EJB.  AOP Alliance
intends to facilitate and standardize the use of AOP to enhance
existing middleware environments (such as J2EE), or development
environements (e.g. Eclipse).  The AOP Alliance also aims to ensure
interoperability between Java/J2EE AOP implementations to build a
larger AOP community.

%prep
%autosetup -p1 -C

%build
export CLASSPATH=
export OPT_JAR_LIST=:
%ant -Dbuild.sysclasspath=only jar -Dant.build.javac.source=1.8 -Dant.build.javac.target=1.8

# Inject OSGi manifest required by Eclipse.
%jar umf %{SOURCE2} build/%{name}.jar

%install
%mvn_file : %{name}
%mvn_artifact %{SOURCE1} build/%{name}.jar

%mvn_install -J build/javadoc

%files -f .mfiles

%changelog
%autochangelog
