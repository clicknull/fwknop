%define _prefix /usr
%define _bindir /usr/bin
%define _sbindir /usr/sbin
%define _includedir /usr/include
%ifarch x86_64
%define _libdir /usr/lib64
%else
%define _libdir /usr/lib
%endif
%define _sysconfdir /etc
%define _localstatedir /var/run
%define _infodir /usr/share/info
%define _mandir /usr/share/man

Name:		fwknop
Version:	2.6.6
Epoch:		1
Release:	1%{?dist}
Summary:	Firewall Knock Operator client. An implementation of Single Packet Authorization.

Group:		Applications/Internet
License:	GPL
URL:		http://www.cipherdyne.org/fwknop/
Source0:	fwknop-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	gpg, gpgme-devel, libpcap-devel, iptables
Requires:	libfko >= 2.0.3, iptables


%package -n libfko
Version:	2.0.3
Release:	1
Summary:	The fwknop library
Group:		Development/Libraries
Requires:   gpg, gpgme

%package -n libfko-devel
Version:	2.0.3
Release:	1
Summary:	The fwknop library header and API docs
Group:		Development/Libraries
Requires:	libfko >= 2.0.3

%package server
Summary:	The Firewall Knock Operator server. An implementation of Single Packet Authorization.
Group:		System Environment/Daemons
Requires:	libfko => 2.0.3, libpcap, iptables


%description
Fwknop implements an authorization scheme known as Single Packet Authorization
(SPA) for Linux systems running firewalld or iptables. This mechanism requires
only a single encrypted and non-replayed packet to communicate various pieces of
information including desired access through a firewalld or iptables policy. The
main application of this program is to use firewalld or iptables in a default-drop
stance to protect services such as SSH with an additional layer of security in order
to make the exploitation of vulnerabilities (both 0-day and unpatched code)
much more difficult.

%description -n libfko
The Firewall Knock Operator library, libfko, provides the Single Packet
Authorization implementation and API for the other fwknop components.

%description -n libfko-devel
This is the libfko development header and API documentation.

%description server
The Firewall Knock Operator server component for the FireWall Knock Operator,
and is responsible for monitoring Single Packet Authorization (SPA) packets
that are generated by fwknop clients, modifying a firewall or acl policy to
allow the desired access after decrypting a valid SPA packet, and removing
access after a configurable timeout.

%prep
%setup -q


%build
./configure \
    --prefix=%{_prefix} \
    --sysconfdir=%{_sysconfdir} \
    --localstatedir=%{_localstatedir} \
    --libdir=%{_libdir} \
    --with-gpgme

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
install -D ./extras/fwknop.init.redhat ${RPM_BUILD_ROOT}/etc/rc.d/init.d/fwknopd
# Just in case...
[ -d "${RPM_BUILD_ROOT}/usr/share/info" ] \
    || mkdir -p ${RPM_BUILD_ROOT}/usr/share/info
[ -f "${RPM_BUILD_ROOT}/usr/share/info/dir" ] \
    || touch ${RPM_BUILD_ROOT}/usr/share/info/dir

%clean
rm -rf $RPM_BUILD_ROOT

%post -n libfko-devel
/sbin/ldconfig
/sbin/install-info %{_infodir}/libfko.info* %{_infodir}/dir

%post -n fwknop-server
/sbin/chkconfig --add fwknopd
/sbin/chkconfig fwknopd off

%preun -n fwknop-server
/sbin/chkconfig --del fwknopd

%preun -n libfko-devel
if [ "$1" = 0 ]; then
 /sbin/install-info --delete %{_infodir}/libfko.info* %{_infodir}/dir
fi

%postun -n libfko
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/fwknop
%attr(0644,root,root) %{_mandir}/man8/fwknop.8*
%exclude %{_infodir}/dir

%files -n libfko
%defattr(-,root,root,-)
%attr(0644,root,root) %{_libdir}/libfko.*

%files -n libfko-devel
%defattr(-,root,root,-)
%attr(0644,root,root) %{_includedir}/fko.h
%attr(0644,root,root) %{_infodir}/libfko.info*

%files server
%defattr(-,root,root,-)
%attr(0755,root,root) %{_sbindir}/fwknopd
%attr(0755,root,root) /etc/rc.d/init.d/fwknopd
%attr(0644,root,root) %{_mandir}/man8/fwknopd.8*
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/fwknop/fwknopd.conf
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/fwknop/access.conf

%changelog
* Tue Apr 23 2015 <mbr@cipherdyne.org> - 2.6.6
- fwknop-2.6.6 release.

* Tue Dec 16 2014 <mbr@cipherdyne.org> - 2.6.5
- fwknop-2.6.5 release.

* Sun Nov 16 2014 <mbr@cipherdyne.org> - 2.6.4
- fwknop-2.6.4 release.

* Mon Jul 28 2014 <mbr@cipherdyne.org> - 2.6.3
- Removed gdbm and gdbm-devel dependencies since these are only
  needed if a user compiles fwknopd with the --disable-file-cache
  argument to the 'configure' script, and the RPM's are not built
  with this.
- Bumped libfko and libfko-devel version to 2.0.3.
- fwknop-2.6.3 release.

* Mon Apr 28 2014 <mbr@cipherdyne.org> - 2.6.2
- Bumped libfko and libfko-devel version to 2.0.2.
- fwknop-2.6.2 release.

* Sat Apr 12 2014 <mbr@cipherdyne.org> - 2.6.1
- fwknop-2.6.1 release.

* Sun Jan 12 2014 <mbr@cipherdyne.org> - 2.6.0
- Bumped libfko and libfko-devel version to 2.0.1.
- fwknop-2.6.0 release.

* Thu Jul 25 2013 <mbr@cipherdyne.org> - 2.5.1
- fwknop-2.5.1 release.

* Fri Jul 19 2013 <mbr@cipherdyne.org> - 2.0.4-1
- Bumped libfko and libfko-devel version to 2.0.0.
- fwknop-2.5 release (HMAC authenticated encryption support).

* Sun Dec  9 2012 <mbr@cipherdyne.org> - 2.0.4-1
- Bumped libfko and libfko-devel version to 1.0.0.
- fwknop-2.0.4 release.

* Sat Dec  1 2012 <dstuart@dstuart.org> - 2.0.4-1
- Removed uneeded include files (which had been added to address an issue that
  has since been fixed).

* Thu Nov 15 2012 <mbr@cipherdyne.org>
- fwknop-2.0.4 release.

* Sat Nov  3 2012 Tomoyuki Kano <tomo@appletz.jp> - 1:2.0.3-1
- Added missing include files.

* Thu Jul 15 2010 Damien Stuart <dstuart@dstuart.org>
- Fixed some misplaced depenencies (moved gpgpme from server to libfko).

* Wed Jul  7 2010 Damien Stuart <dstuart@dstuart.org>
- Made the post and preun steps specific to libfko-devel.

* Tue Jul  6 2010 Damien Stuart <dstuart@dstuart.org>
- Initial RPMification.

###EOF###
