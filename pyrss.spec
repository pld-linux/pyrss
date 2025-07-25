Summary:	PyRSS - headline delivery for Jabber
Summary(pl.UTF-8):	PyRSS - dostarczanie skrótów wiadomości do Jabbera
Name:		pyrss
Version:	0.9.9.1
Release:	2
License:	GPL
Group:		Applications/Communications
Source0:	http://files.jabberstudio.org/pyrss/%{name}-%{version}.tar.bz2
# Source0-md5:	3f48f3b7f36c2c588b8d55a5841482ab
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-psyco_fix.patch
URL:		http://pyrss.jabberstudio.org/
Requires(post):	sed >= 4.0
Requires(post,preun):	/sbin/chkconfig
Requires:	daemon
Requires:	jabber-common
Requires:	python-MySQLdb
Requires:	python-feedparser
Requires:	python-pyxmpp
Requires:	rc-scripts
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PyRSS polls a series of sources (RSS or Atom file on the web), and,
according to user's interests (individual source subscriptions),
forwards those new items as Jabber messages.

%description -l pl.UTF-8
PyRSS odczytuje szereg źródeł (plików RSS lub Atom w sieci) i, zgodnie
z zainteresowaniami użytkownika (indywidualną prenumeratą),
przekierowuje te nowe wiadomości jako wiadomości Jabbera.

%prep
%setup -q
%patch -P0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/jabber,%{_sbindir}} \
	$RPM_BUILD_ROOT{/etc/sysconfig,/etc/rc.d/init.d}

install pyrss.py $RPM_BUILD_ROOT%{_sbindir}/pyrss
install pyrss.xml $RPM_BUILD_ROOT%{_sysconfdir}/jabber
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/pyrss
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/pyrss

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f %{_sysconfdir}/jabber/secret ] ; then
	SECRET=`cat %{_sysconfdir}/jabber/secret`
	if [ -n "$SECRET" ] ; then
		echo "Updating component authentication secret in pyrss.xml..."
		%{__sed} -i -e "s/'>password<'/'>$SECRET<'/" /etc/jabber/pyrss.xml
	fi
fi

/sbin/chkconfig --add pyrss
%service pyrss restart "PyRSS"

%preun
if [ "$1" = "0" ]; then
	%service pyrss stop
	/sbin/chkconfig --del pyrss
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO pyrss.sql contrib
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,jabber) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/jabber/pyrss.xml
%attr(754,root,root) /etc/rc.d/init.d/pyrss
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/pyrss
