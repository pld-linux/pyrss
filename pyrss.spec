Summary:	PyRSS - headline delivery for Jabber
Summary(pl):	PyRSS - dostarczanie skr�t�w wiadomo�ci do Jabbera
Name:		pyrss
Version:	0.9.6
Release:	0.20050203.1
License:	GPL
Group:		Applications/Communications
#Source0:	http://jabberstudio.org/projects/pyrss/releases/%{name}-%{version}.tar.bz2
Source0:	http://ep09.pld-linux.org/~mmazur/misc/%{name}-%{version}-20050203.tar.bz2
# Source0-md5:	b50f6b4535f9f0a932a7e7e852ed0904
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://pyrss.jabberstudio.org/
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	daemon
Requires:	jabber-common
Requires:	python-pyxmpp
Requires:	python-feedparser
Requires:	python-MySQLdb
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PyRSS polls a series of sources (RSS or Atom file on the web), and,
according to user's interests (individual source subscriptions),
forwards those new items as Jabber messages.

%description -l pl
PyRSS odczytuje szereg �r�de� (plik�w RSS lub Atom w sieci) i,
zgodnie z zainteresowaniami u�ytkownika (indywidualn� prenumerat�),
przekierowuje te nowe wiadomo�ci jako wiadomo�ci Jabbera.

%prep
%setup -qn pyrss

%build

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
if [ -f /etc/jabber/secret ] ; then
	SECRET=`cat /etc/jabber/secret`
	if [ -n "$SECRET" ] ; then
        	echo "Updating component authentication secret in pyrss.xml..."
		perl -pi -e "s/'>password<'/'>$SECRET<'/" /etc/jabber/pyrss.xml
	fi
fi

/sbin/chkconfig --add pyrss
if [ -r /var/lock/subsys/pyrss ]; then
	/etc/rc.d/init.d/pyrss restart >&2
else
	echo "Run \"/etc/rc.d/init.d/pyrss start\" to start PyRSS."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -r /var/lock/subsys/pyrss ]; then
		/etc/rc.d/init.d/pyrss stop >&2
	fi
	/sbin/chkconfig --del pyrss
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO pyrss.sql
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,jabber) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/jabber/pyrss.xml
%attr(754,root,root) /etc/rc.d/init.d/pyrss
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/pyrss