%{!?docs:%define docs 1}
%{?buildrhel3:%define kerbdir /usr/kerberos}
%{!?kerbdir:%define kerbdir "/usr"}

Summary:	A "master to multiple slaves" replication system with cascading and failover
Name:		postgresql-slony1
Version:	1.2.12
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
URL:		http://main.slony.info/
Source0:	http://main.slony.info/downloads/1.2/source/postgresql-slony1-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	postgresql-devel, postgresql-server, initscripts
Requires:	postgresql-server 

%if %docs
BuildRequires:	docbook-style-dsssl
%endif

%description
Slony-I is a "master to multiple slaves" replication 
system for PostgreSQL with cascading and failover.

The big picture for the development of Slony-I is to build
a master-slave system that includes all features and
capabilities needed to replicate large databases to a
reasonably limited number of slave systems.

Slony-I is a system for data centers and backup
sites, where the normal mode of operation is that all nodes
are available

%if %docs
%package docs
Summary:	Documentation for Slony-I
Group:		Applications/Databases
Requires:	postgresql-slony1-1.2.12-%{release}
BuildRequires:	libjpeg, netpbm-progs, groff, docbook-style-dsssl, ghostscript

%description docs
The postgresql-slony1-docs package includes some 
documentation for Slony-I.
%endif

%prep
%setup -q -n postgresql-slony1-%{version}

%build

# Temporary measure for 1.2.10
%if %docs
find doc/ -type f -exec chmod 600 {} \;
%endif

CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS
CPPFLAGS="${CPPFLAGS} -I%{_includedir}/et -I%{kerbdir}/include" ; export CPPFLAGS
CFLAGS="${CFLAGS} -I%{_includedir}/et -I%{kerbdir}/include" ; export CFLAGS

export LIBNAME=%{_lib}
%configure --includedir %{_includedir}/pgsql --with-pgconfigdir=%{_bindir} --libdir=%{_libdir} \
	--with-perltools=%{_bindir} --with-toolsbin=%{_bindir} \
%if %docs
	--with-docs --with-docdir=%{_docdir}/%{name}-%{version} \
%endif
	--datadir %{_datadir}/pgsql --with-pglibdir=%{_libdir}/pgsql 

make %{?_smp_mflags}
make %{?_smp_mflags} -C tools

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}%{_datadir}/pgsql/
install -d %{buildroot}%{_libdir}/pgsql/
make %{?_smp_mflags} DESTDIR=%{buildroot} install
install -m 0755 src/backend/slony1_funcs.so %{buildroot}%{_libdir}/pgsql/slony1_funcs.so
install -m 0755 src/xxid/xxid.so %{buildroot}%{_libdir}/pgsql/xxid.so
install -m 0644 src/backend/*.sql %{buildroot}%{_datadir}/pgsql/
install -m 0644 src/xxid/*.sql %{buildroot}%{_datadir}/pgsql/
install -m 0755 tools/*.sh  %{buildroot}%{_bindir}/
install -m 0644 share/slon.conf-sample %{buildroot}%{_sysconfdir}/slon.conf
/bin/chmod 644 COPYRIGHT UPGRADING SAMPLE HISTORY-1.1 RELEASE

install -d %{buildroot}%{_initrddir}
install -m 755 redhat/postgresql-slony1.init %{buildroot}%{_initrddir}/postgresql-slony1

# Temporary measure for 1.2.10
%if %docs
	rm -f doc/implementation/.cvsignore
	rm -f doc/concept/.cvsignore
%endif

cd tools
make %{?_smp_mflags} DESTDIR=%{buildroot} install
/bin/rm -rf altperl/*.pl altperl/ToDo altperl/README altperl/Makefile altperl/CVS
install -m 0644 altperl/slon_tools.conf-sample  %{buildroot}%{_sysconfdir}/slon_tools.conf
install -m 0755 altperl/* %{buildroot}%{_bindir}/
install -m 0644 altperl/slon-tools  %{buildroot}%{_libdir}/pgsql/slon-tools.pm
/bin/rm -f %{buildroot}%{_sysconfdir}/slon_tools.conf-sample
/bin/rm -f %{buildroot}%{_bindir}/slon_tools.conf-sample
/bin/rm -f %{buildroot}%{_bindir}/slon-tools.pm
/bin/rm -f %{buildroot}%{_bindir}/slon-tools
/bin/rm -f %{buildroot}%{_bindir}/pgsql/slon-tools
/bin/rm -f %{buildroot}%{_bindir}/old-apache-rotatelogs.patch

%clean
rm -rf %{buildroot}

%post
chkconfig --add postgresql-slony1

%preun
if [ $1 = 0 ] ; then
	/sbin/service postgresql-slony1 condstop >/dev/null 2>&1
	chkconfig --del postgresql-slony1
fi

%postun
if [ $1 -ge 1 ]; then
	/sbin/service postgresql-slony1 condrestart >/dev/null 2>&1
fi

%files
%defattr(-,root,root,-)
%attr(644,root,root) %doc COPYRIGHT UPGRADING HISTORY-1.1 INSTALL SAMPLE RELEASE
%{_bindir}/*
%{_libdir}/pgsql/slony1_funcs.so
%{_libdir}/pgsql/xxid.so
%{_datadir}/pgsql/*.sql
%config(noreplace) %{_sysconfdir}/slon.conf
%{_libdir}/pgsql/slon-tools.pm
%config(noreplace) %{_sysconfdir}/slon_tools.conf
%attr(755,root,root) %{_sysconfdir}/rc.d/init.d/postgresql-slony1

%if %docs
%files docs
%attr(644,root,root) %doc doc/adminguide  doc/concept  doc/howto  doc/implementation  doc/support
%endif

%changelog
* Wed Aug 29 2007 Devrim Gunduz <devrim@CommandPrompt.com> 1.2.11-1
- Update to 1.2.11
- Remove the word "engine" from init script name.

* Mon Aug 6 2007 Devrim Gunduz <devrim@CommandPrompt.com> 1.2.10-2
- Fix Source0
- Spec file cleanup (removed macro for perltools)
- Added initscripts as BR.
- Fix doc package installation path (and ownership issue)

* Wed Jun 13 2007 Devrim Gunduz <devrim@CommandPrompt.com> 1.2.10-1
- Update to 1.2.10

* Mon Jun 11 2007 Devrim Gunduz <devrim@CommandPrompt.com> 1.2.9-3
- Add BuildRequires for docs subpackage, per #199154 (Thanks Ruben).

* Sun Jun 3 2007 Devrim Gunduz <devrim@CommandPrompt.com> 1.2.9-2
- Some more fixes for Fedora review.
- Remove executable bits from docs.

* Thu May 17 2007 Devrim Gunduz <devrim@CommandPrompt.com>
- Install init script with rpm.
- Fix --with-pgconfigdir parameter.
- Fix rpm build problem when the system has pg_config in both under
  /usr/local/pgsql/bin and /usr/bin

* Wed Mar 22 2007 Christopher Browne <cbbrowne@ca.afilias.info>
- Added more recent release notes

* Wed Mar 7 2007 Christopher Browne <cbbrowne@ca.afilias.info>
- Added more recent release notes

* Thu Jan 4 2007 Devrim Gunduz <devrim@CommandPrompt.com>
- Add docs package (It should be added before but...)

* Wed Nov 8 2006 Devrim Gunduz <devrim@CommandPrompt.com>
- On 64-bit boxes, both 32 and 64 bit -devel packages may be installed. 
  Fix version check script
- Revert tar name patch
- Macros cannot be used in various parts of the spec file. Revert that commit
- Spec file cleanup

* Tue Oct 31 2006 Trevor Astrope <astrope@sitesell.com>
- Fixup tar name and install slon-tools as slon-tools.pm

* Mon Jul 17 2006 Devrim Gunduz <devrim@CommandPrompt.com> postgresql-slony1-engine
- Updated spec and cleaned up rpmlint errors and warnings

* Wed Dec 21 2005 Devrim Gunduz <devrim@commandprompt.com> postgresql-slony1-engine
- Added a buildrhel3 macro to fix RHEL 3 RPM builds
- Added a kerbdir macro

* Wed Dec 14 2005 Devrim Gunduz <devrim@commandprompt.com> postgresql-slony1-engine
- Fixed the spec file so that during upgrade, conf files will not be replaced, and a .rpmnew will be created.

* Thu Nov 24 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- Created bindir

* Wed Oct 26 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- Modify CPPFLAGS and CFLAGS to fix builds on RHEL -- Per Philip Yarra

* Tue Oct 18 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- Created a new package : -docs and moved all the docs there.

* Tue Oct 18 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- Fixed the problem in http://gborg.postgresql.org/pipermail/slony1-general/2005-October/003105.html

* Sat Oct 01 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- Upgrade to 1.1.1

* Tue Jul 12 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- Added a line to check postgresql RPM version and tag SlonyI RPM with it.
- Updated Requires files so that it checks correct PostgreSQL version
- Moved autoconf line into correct place.

* Thu Jun 08 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- Added UPGRADING, HISTORY-1.1, INSTALL, SAMPLE among installed files, reflecting the change in GNUMakefile.in

* Thu Jun 02 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- Apply a new %docs macro and disable building of docs by default.
- Remove slon-tools.conf-sample from bindir.
- Removed --bindir and --libdir, since they are not needed.

* Mon Apr 10 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- More fixes on RPM builds

* Thu Apr 07 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- More fixes on RPM builds

* Tue Apr 04 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- Fix RPM build errors, regarding to tools/ .

* Thu Apr 02 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- Added docs to installed files list.
- Added perltools, so that tools/altperl may be compiled.
- Updated the spec file

* Thu Mar 17 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- Update to 1.1.0beta1
- Remove PostgreSQL source dependency

* Thu Mar 17 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- Fix RPM builds

* Thu Mar 18 2004 Daniel Berrange <berrange@redhat.com> postgresql-slony1-engine
- Initial RPM packaging

