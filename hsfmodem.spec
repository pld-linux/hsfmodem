#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	userspace	#
%bcond_with	verbose		# verbose build (V=1)
#
%define	_rel	0.1
Summary:	Conexant HSF controllerless modem driver userspace utils
Summary(pl.UTF-8):	Narzędzia do sterownika winmodemów HSF firmy Conexant
Name:		hsfmodem
Version:	7.60.00.09full
Release:	%{_rel}@%{_kernel_ver_str}
License:	Custom Licence by (c) 2003-2004 Linuxant inc. All rights reserved.
Group:		Base/Kernel
Source0:	http://www.linuxant.com/drivers/hsf/full/archive/%{name}-%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	91e42c01c8d69ad79e0793770e2059d4
Source1:	http://www.linuxant.com/drivers/hsf/full/archive/%{name}-%{version}/100498D_RM_HxF_Released.pdf
# Source1-md5:	e6d8fea8f5f641d7bb4dfb33c6f478e7
Source2:	http://www.linuxant.com/drivers/files/listmodem_app_linux.tar.gz
# Source2-md5:	516f3825014eb460a0c16cbd927a80d1
URL:		http://www.linuxant.com/
BuildRequires:	%{kgcc_package}
%{?with_dist_kernel:BuildRequires:      kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
Requires:	pciutils
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Conexant HSF controllerless modem driver for Linux. This package
contains only free version of the drivers (limited to 14kbps and no
fax). Full version is available at linuxant.com.

%description -l pl.UTF-8
Sterownik do winmodemów HSF firmy Conexant dla Linuksa. Ten pakiet
zawiera tylko darmową wersję sterowników, która ogranicza transfer do
14kbps i nie pozwala na użycie faksu. Pełna wersja dostępna jest na
linuxant.com.

%package -n kernel%{_alt_kernel}-char-hsf
Summary:	Conexant HSF controllerless modem driver
Summary(pl.UTF-8):	Sterownik do winmodemów HSF firmy Conexant
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel}
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:Requires(postun):	kernel%{_alt_kernel}}

%description -n kernel%{_alt_kernel}-char-hsf
This is a Linux driver for Conexant HSF controllerless modem driver.

%description -n kernel%{_alt_kernel}-char-hsf -l pl.UTF-8
Sterownik dla Linuksa do winmodemów HSF firmy Conexant.

%prep
%setup -q

%build
%if %{with dist_kernel}
%build_kernel_modules -m hsfpcibasic2,hsfmc97ich,hsfmc97via,hsfmc97ali,hsfmc97ati,hsfmc97sis,hsfusbcd2,hsfhda,hsfsoar,hsfserial,hsfengine,hsfosspec -C modules
%endif

%if %{with userspace}
%{__make} all \
	KERNELSRC=%{_kernelsrcdir}
#TODO
#%{__make} --quiet --no-print-directory clean all modules
#	CNXT_KERNELSRC=%{_kernelsrcdir} \
#	DISTRO_CFLAGS="-D__MODULE_KERNEL_%{_target_cpu}=1" \
#	CNXT_MODS_DIR=binaries/linux-genetic
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with dist_kernel}
%install_kernel_modules -d misc -m modules/hsfpcibasic2,modules/hsfmc97ich,modules/hsfmc97via,modules/hsfmc97ali,modules/hsfmc97ati,modules/hsfmc97sis,modules/hsfusbcd2,modules/hsfhda,modules/hsfsoar,modules/hsfserial,modules/hsfengine,modules/hsfosspec
%endif

%if %{with userspace}
%{__make} install \
	ROOT=$RPM_BUILD_ROOT \
	KERNELSRC=%{_kernelsrcdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

#%post
#%{_sbindir}/hsfconfig --auto

#%preun
#%{_sbindir}/hsfconfig --remove

%post -n kernel%{_alt_kernel}-char-hsf
%depmod %{_kernel_ver}

%postun -n kernel%{_alt_kernel}-char-hsf
%depmod %{_kernel_ver}

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc BUGS CHANGES CREDITS FAQ INSTALL LICENSE README
%attr(755,root,root) %{_sbindir}/*
%dir %{_sysconfdir}/hsfmodem
%dir %{_sysconfdir}/hsfmodem/nvm
%{_sysconfdir}/hsfmodem/package
%config %{_sysconfdir}/hsfmodem/nvm/*
%dir %{_libdir}/hsfmodem
%{_libdir}/hsfmodem/LICENSE
%config %{_libdir}/hsfmodem/config.mak
%{_libdir}/hsfmodem/rchsf
%dir %{_libdir}/hsfmodem/modules
%{_libdir}/hsfmodem/modules/[!k]*
%attr(755,root,root) %{_libdir}/hsfmodem/modules/*.sh
%endif

%if %{with dist_kernel}
%files -n kernel%{_alt_kernel}-char-hsf
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*.ko*
%endif
