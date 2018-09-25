
Name:    gpom
Version: 3.0.2
Release: alt1%ubt

Summary: Group Policy Object Manager
License: Apache-2.0
Group:   Other
URL:     https://github.com/altlinuxteam/gpom

Packager: Sergey Bubnov <omg@altlinux.org>

BuildRequires(pre): rpm-build-ubt

BuildRequires: rpm-build-python
BuildRequires: python-devel
BuildRequires: python-module-distribute

BuildArch: noarch

Source:  %name-%version.tar

# Dueconfigparser from python-module-future not contains SafeConfigParser
Requires: python-module-configparser

#Requires: python-module-xmltodict
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
mkdir -p %buildroot%_sysconfdir
install -m644 gpom.conf %buildroot%_sysconfdir/
mkdir -p %buildroot%_localstatedir/%name/{cache,state,cache/policies}

%files
%config(noreplace) %_sysconfdir/%name.conf
%_bindir/*
%python_sitelibdir/%name/
%python_sitelibdir/*.egg-info
%_localstatedir/%name/state
%dir %_localstatedir/%name/cache
%dir %_localstatedir/%name/cache/policies

%changelog
* Wed Sep 25 2018 Sergey Bubnov <omg@altlinux.org> 3.0.2-alt1%ubt
- Fix bug with account name in CLI parser

* Wed Sep 25 2018 Sergey Bubnov <omg@altlinux.org> 3.0.1-alt5%ubt
- Fix state behaviour
- Fix broken imports
- Remove stupid hardcode

* Mon Sep 24 2018 Evgeny Sinelnikov <sin@altlinux.org> 3.0.1-alt4%ubt
- Fix wrong distribution requires for configparser

* Mon Sep 24 2018 Evgeny Sinelnikov <sin@altlinux.org> 3.0.1-alt3%ubt
- Add default config to sysconfig directory
- Build with ubt macros for backporting to stable branches

* Tue Sep 18 2018 Evgeny Sinelnikov <sin@altlinux.org> 3.0.1-alt2
- Fix running gpom as console_script

* Fri Sep 14 2018 Sergey Bubnov <omg@altlinux.org> 3.0.1-alt1
- Initial build for Sisyphus
