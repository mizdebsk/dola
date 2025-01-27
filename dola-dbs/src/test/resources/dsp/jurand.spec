Name:           jurand
Version:        1.3.5
Release:        %autorelease
Summary:        A tool for manipulating Java symbols
License:        Apache-2.0
URL:            https://github.com/fedora-java/jurand

Source0:        https://github.com/fedora-java/jurand/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  diffutils
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  rubygem-asciidoctor

%description
The tool can be used for patching .java sources in cases where using sed is
insufficient due to Java language syntax. The tool follows Java language rules
rather than applying simple regular expressions on the source code.

%prep
%autosetup -p1 -C

%build
%{make_build} test-compile manpages

%install
export buildroot=%{buildroot}
export bindir=%{_bindir}
export rpmmacrodir=%{_rpmmacrodir}
export mandir=%{_mandir}

./install.sh

%check
make test

%files -f target/installed_files
%dir %{_rpmconfigdir}
%dir %{_rpmmacrodir}
%license LICENSE NOTICE
%doc README.adoc

%changelog
%autochangelog
