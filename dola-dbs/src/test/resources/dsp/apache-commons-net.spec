Name:           apache-commons-net
Version:        3.11.1
Release:        %autorelease
Summary:        Internet protocol suite Java library
License:        Apache-2.0
URL:            https://commons.apache.org/proper/commons-net/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://archive.apache.org/dist/commons/net/source/commons-net-%{version}-src.tar.gz
Source1:        https://downloads.apache.org/commons/net/source/commons-net-%{version}-src.tar.gz.asc
Source2:        https://downloads.apache.org/commons/KEYS

BuildRequires:  maven-local
BuildRequires:  mvn(commons-io:commons-io)
BuildRequires:  mvn(org.apache.commons:commons-lang3)
BuildRequires:  mvn(org.apache.commons:commons-parent:pom:)
BuildRequires:  mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter-api)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter-engine)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter-params)
BuildRequires:  mvn(org.junit.vintage:junit-vintage-engine)
# for signature verification
BuildRequires:  gnupg2
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 3.11.1-11

%description
This is an Internet protocol suite Java library originally developed by
ORO, Inc.  This version supports Finger, Whois, TFTP, Telnet, POP3, FTP,
NNTP, SMTP, and some miscellaneous protocols like Time and Echo as well
as BSD R command support. The purpose of the library is to provide
fundamental protocol access, not higher-level abstractions.

%prep
%autosetup -p1 -C
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'

%pom_remove_plugin :exec-maven-plugin

# Fails with "Coverage checks have not been met."
%pom_remove_plugin org.jacoco:jacoco-maven-plugin

%pom_remove_dep org.apache.ftpserver:ftpserver-core

# Disable tests that rely on networking to be available and working.
# Depending on host configuration, on different systems they fail with
# errors such as "Connection timed out", "Address already in use",
# "Temporary failure in name resolution" etc.
rm \
src/test/java/org/apache/commons/net/chargen/CharGenUDPClientTest.java \
src/test/java/org/apache/commons/net/daytime/DaytimeTCPClientTest.java \
src/test/java/org/apache/commons/net/daytime/DaytimeUDPClientTest.java \
src/test/java/org/apache/commons/net/discard/DiscardUDPClientTest.java \
src/test/java/org/apache/commons/net/echo/EchoUDPClientTest.java \
src/test/java/org/apache/commons/net/ftp/AbstractFtpsTest.java \
src/test/java/org/apache/commons/net/ftp/FTPClientTransferModeTest.java \
src/test/java/org/apache/commons/net/ftp/FTPSClientTest.java \
src/test/java/org/apache/commons/net/ftp/NoProtocolSslConfigurationProxy.java \
src/test/java/org/apache/commons/net/tftp/TFTPAckPacketTest.java \
src/test/java/org/apache/commons/net/tftp/TFTPDataPacketTest.java \
src/test/java/org/apache/commons/net/tftp/TFTPErrorPacketTest.java \
src/test/java/org/apache/commons/net/tftp/TFTPReadRequestPacketTest.java \
src/test/java/org/apache/commons/net/tftp/TFTPServerPathTest.java \
src/test/java/org/apache/commons/net/tftp/TFTPTest.java \
src/test/java/org/apache/commons/net/tftp/TFTPWriteRequestPacketTest.java \
src/test/java/org/apache/commons/net/time/TimeTCPClientTest.java \
src/test/java/org/apache/commons/net/time/TimeUDPClientTest.java \

%mvn_file : commons-net %{name}
%mvn_alias : org.apache.commons:commons-net

%build
%mvn_build -j -- -Dcommons.osgi.symbolicName=org.apache.commons.net

%install
%mvn_install

%files -f .mfiles
%doc README.md RELEASE-NOTES.txt
%license LICENSE.txt NOTICE.txt

%changelog
%autochangelog
