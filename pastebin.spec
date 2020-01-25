%define		php_min_version 5.0.0
Summary:	A collaborative debugging tool
Name:		pastebin
Version:	0.60
Release:	0.8
License:	Affero GPL licence
Group:		Applications/WWW
Source0:	http://%{name}.dixo.net/pastebin.tar.gz
# Source0-md5:	c73c4b40e8eeddba9b515586f017a777
Patch0:		postdir.patch
Patch1:		system-geshi.patch
Patch2:		layout.patch
Patch3:		fixes.patch
Patch4:		config.patch
Source1:	apache.conf
Source2:	lighttpd.conf
URL:		http://blog.dixo.net/downloads/
BuildRequires:	rpmbuild(macros) >= 1.553
Requires:	php(core) >= %{php_min_version}
Requires:	php(date)
Requires:	php(pcre)
Requires:	php-geshi >= 1.0.7
Requires:	webapps
Requires:	webserver(access)
Requires:	webserver(alias)
Suggests:	php-mysql
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

# bad depsolver
%define		_noautopear	pear

# exclude optional php dependencies
%define		_noautophp	php-mysql

# put it together for rpmbuild
%define		_noautoreq	%{?_noautophp} %{?_noautopear}

%description
This tool was orignally designed to enable collaborative code review
via the #php IRC channel. Inspired by www.parseerror.com/paste, but
more streamlined and capable of allowing collabation via IRC by
allowing easy modification of posted code. Another benefit is short
urls - e.g. <http://pastebin.com/333>

Since then it has found uses in many developer communities and has
been constantly improved.

%prep
%setup -q
%undos -f php
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

rm -rf lib/geshi

# legacy
rm public_html/legacy.php

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir},/var/lib/%{name}}

cp -a lib public_html $RPM_BUILD_ROOT%{_appdir}

# for file based posts storage
install -d $RPM_BUILD_ROOT/var/lib/%{name}

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf
cp -p $RPM_BUILD_ROOT%{_sysconfdir}/{apache,httpd}.conf

mv $RPM_BUILD_ROOT%{_appdir}/lib/config/* $RPM_BUILD_ROOT%{_sysconfdir}
rmdir $RPM_BUILD_ROOT%{_appdir}/lib/config
ln -s %{_sysconfdir} $RPM_BUILD_ROOT%{_appdir}/lib/config

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES INSTALL LICENCE README UPGRADE
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.php
%{_appdir}

%dir %attr(770,root,http) /var/lib/%{name}
