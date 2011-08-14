#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	userspace	# don't build userspace programs
%bcond_with	verbose		# verbose build (V=1)

%if "%{_alt_kernel}" != "%{nil}"
%undefine	with_userspace
%endif
%if %{without userspace}
# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0
%endif

%define		rel	0.1
%define		pname	hsfmodem
Summary:	Conexant HSF controllerless modem driver userspace utils
Summary(pl.UTF-8):	Narzędzia do sterownika winmodemów HSF firmy Conexant
Name:		%{pname}%{_alt_kernel}
Version:	7.80.02.06full
Release:	%{rel}
License:	Custom Licence by (c) 2003-2010 Linuxant inc. All rights reserved.
Group:		Base/Kernel
Source0:	http://www.linuxant.com/drivers/hsf/full/archive/%{pname}-%{version}/%{pname}-%{version}.tar.gz
# Source0-md5:	8eb0935e86b898190bf20c08894af17e
Source1:	https://linux.dell.com/files/ubuntu/hardy/modem-drivers/hsf/hsfmodem-7.68.00.09x86_64oem.tar.gz
# Source1-md5:	9cfa801c88f9c61cb26db786d64872c7
Source2:	http://www.linuxant.com/drivers/hsf/full/archive/%{pname}-%{version}/100498D_RM_HxF_Released.pdf
# Source2-md5:	e6d8fea8f5f641d7bb4dfb33c6f478e7
Source3:	http://www.linuxant.com/drivers/files/listmodem_app_linux.tar.gz
# Source3-md5:	516f3825014eb460a0c16cbd927a80d1
Patch0:		kernel.patch
URL:		http://www.linuxant.com/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
Requires:	pciutils
ExclusiveArch:	%{ix86} %{x8664}
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
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif

%description -n kernel%{_alt_kernel}-char-hsf
This is a Linux driver for Conexant HSF controllerless modem driver.

%description -n kernel%{_alt_kernel}-char-hsf -l pl.UTF-8
Sterownik dla Linuksa do winmodemów HSF firmy Conexant.

%prep
%setup -q
%patch0 -p1

%build
%if %{with dist_kernel}
# see @CNXTMODS@ for module list
# TODO: snd_hda_codec_hsfmodem missing
%build_kernel_modules -C modules -m hsfpcibasic2,hsfpcibasic3,hsfmc97ich,hsfmc97via,hsfmc97ali,hsfmc97ati,hsfmc97sis,hsfusbcd2,hsfhda,hsfsoar,hsfserial,hsfengine,hsfosspec
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
# see @CNXTMODS@ for module list
%install_kernel_modules -d misc -m modules/hsfpcibasic2,modules/hsfpcibasic3,modules/hsfmc97ich,modules/hsfmc97via,modules/hsfmc97ali,modules/hsfmc97ati,modules/hsfmc97sis,modules/hsfusbcd2,modules/hsfhda,modules/hsfsoar,modules/hsfserial,modules/hsfengine,modules/hsfosspec
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
