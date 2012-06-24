#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
#
Summary:	Conexant HSF controllerless modem driver userspace utils
Summary(pl):	Narz�dzia do sterownika winmodem�w HSF firmy Conexant
Name:		hsfmodem
Version:	7.18.00.06full
%define	_rel	1
Release:	%{_rel}@%{_kernel_ver_str}
License:	Custom Licence by (c) 2003-2004 Linuxant inc. All rights reserved.
Group:		Base/Kernel
Source0:	http://www.linuxant.com/drivers/hsf/full/archive/%{name}-%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	2d725bd8e484a4037daefec6208ba28b
Source1:	http://www.linuxant.com/drivers/hsf/full/archive/hsfmodem-7.18.00.06full/100498D_RM_HxF_Released.pdf
# Source1-md5:	e6d8fea8f5f641d7bb4dfb33c6f478e7
Source2:	http://www.linuxant.com/drivers/files/listmodem_app_linux.tar.gz
# Source2-md5:	516f3825014eb460a0c16cbd927a80d1
URL:		http://www.linuxant.com/
%{?with_dist_kernel:BuildRequires:	kernel-module-build}
BuildRequires:	%{kgcc_package}
Requires:	pciutils
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Conexant HSF controllerless modem driver for Linux.
This package contains only free version of the drivers (limited to
14kbps and no fax). Full version is available at linuxant.com.

%description -l pl
Sterownik do winmodem�w HSF firmy Conexant dla Linuksa.  Ten pakiet 
zawiera tylko darmow� wersj� sterownik�w, kt�ra ogranicza transfer 
do 14kbps i nie pozwala na u�ycie faksu. Pe�na wersja dost�pna jest na
linuxant.com.

%package -n kernel-char-hsf
Summary:	Conexant HSF controllerless modem driver 
Summary(pl):	Sterownik do winmodem�w HSF firmy Conexant
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:Requires(postun):	kernel-up}

%description -n kernel-char-hsf
This is a Linux driver for Conexant HSF controllerless modem driver.

%description -n kernel-char-hsf -l pl
Sterownik dla Linuksa do winmodem�w HSF firmy Conexant.

%prep
%setup -q

%build
%{__make} all \
	KERNELSRC=%{_kernelsrcdir}

%{__make} --quiet --no-print-directory clean all modules \
	CNXT_KERNELSRC=%{_kernelsrcdir} \
	DISTRO_CFLAGS="-D__MODULE_KERNEL_%{_target_cpu}=1" \
	CNXT_MODS_DIR=binaries/linux-genetic

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,-smp}/misc

%{__make} install \
	ROOT=$RPM_BUILD_ROOT \
	KERNELSRC=%{_kernelsrcdir}

install modules/*.ko  $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
#{,-smp}

%clean
rm -rf $RPM_BUILD_ROOT

#%post
#%{_sbindir}/hsfconfig --auto

#%preun
#%{_sbindir}/hsfconfig --remove

%post -n kernel-char-hsf
%depmod %{_kernel_ver}

%postun -n kernel-char-hsf
%depmod %{_kernel_ver}

%files
%defattr(644,root,root,755)
%doc BUGS CHANGES CREDITS FAQ INSTALL LICENSE README
%attr(755,root,root) %{_sbindir}/*
%dir /etc/hsfmodem
%dir /etc/hsfmodem/nvm
/etc/hsfmodem/package
%config /etc/hsfmodem/nvm/*
%dir %{_libdir}/hsfmodem
%{_libdir}/hsfmodem/LICENSE
%config %{_libdir}/hsfmodem/config.mak
%{_libdir}/hsfmodem/rchsf
%dir %{_libdir}/hsfmodem/modules
%{_libdir}/hsfmodem/modules/[!k]*
%attr(755,root,root) %{_libdir}/hsfmodem/modules/*.sh

%files -n kernel-char-hsf
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*.ko*
