
Name:    gpom
Version: 3.0.1
Release: alt2

Summary: Group Policy Object Manager
License: Apache-2.0
Group:   Other
URL:     https://github.com/altlinuxteam/gpom

Packager: Sergey Bubnov <omg@altlinux.org>

BuildRequires: rpm-build-python
BuildRequires: python-devel
BuildRequires: python-module-distribute

BuildArch: noarch

Source:  %name-%version.tar

#Requires: python-module-xmltodict
#Requires: python-module-configparser
#Requires: python-module-ldap
#Requires: python-module-samba
Requires: libsasl2-plugin-gssapi

%description
Group Policy Object Manager

%prep
%setup -n %name-%version

%build
%python_build

%install
%python_install

%files
%_bindir/*
%python_sitelibdir/%name/
%python_sitelibdir/*.egg-info

%changelog
* Tue Sep 18 2018 Evgeny Sinelnikov <sin@altlinux.org> 3.0.1-alt2
- Fix running gpom as console_script

* Fri Sep 14 2018 Sergey Bubnov <omg@altlinux.org> 3.0.1-alt1
- Initial build for Sisyphus
