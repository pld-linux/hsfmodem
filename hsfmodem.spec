Summary:	Conexant HSF controllerless modem driver
Summary(pl):	Sterownik do winmodemów HSF firmy Conexant
Name:		hsfmodem
Version:	6.03.00lnxt03091800free
%define	_rel	0.1
Release:	%{_rel}@%{_kernel_ver_str}
License:	Custom Licence by LinuxAnt.com
Group:		Base/Kernel
Source0:	http://www.linuxant.com/drivers/hsf/free/archive/%{name}-%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	aa85060185dba1bd090c2d02ef1c9c8a
URL:		http://www.linuxant.com/
%{!?_without_dist_kernel:BuildRequires:	kernel-source }
BuildRequires:	%{kgcc_package}
%{!?_without_dist_kernel:%requires_releq_kernel_up}
Requires:	pciutils
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Conexant HSF controllerless modem driver for Linux.
This package contains only free version of the drivers (limited to
14kbps). Full version is available at linuxant.com.

%description -l pl
Sterownik do winmodemów HSF firmy Conexant dla Linuxa.
Ten pakiet zawiera tylko darmow± wersjê sterowników, która ogranicza
transfer do 14kbps. Pe³na wersja dostêpna jest na linuxant.com.

%prep
%setup -q

%build
%{__make} all KERNELSRC=%{_kernelsrcdir}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	ROOT=$RPM_BUILD_ROOT \
	KERNELSRC=%{_kernelsrcdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/hsfconfig --auto

%preun
%{_sbindir}/hsfconfig --remove

%files
%defattr(644,root,root,755)
%doc BUGS CHANGES CREDITS FAQ INSTALL LICENSE README
%attr(755,root,root) %{_sbindir}/*
%dir /etc/hsfmodem
%dir /etc/hsfmodem/nvm
%config /etc/hsfmodem/nvm/*
%dir %{_libdir}/hsfmodem
%config %{_libdir}/hsfmodem/config.mak
%dir %{_libdir}/hsfmodem/modules
%attr(644,root,root) %{_libdir}/hsfmodem/LICENSE
%{_libdir}/hsfmodem/modules/[!k]*
%attr(755,root,root) %{_libdir}/hsfmodem/modules/*.sh
