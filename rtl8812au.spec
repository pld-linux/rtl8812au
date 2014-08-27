# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_with	verbose		# verbose build (V=1)

%define _alt_kernel %{nil}
%if "%{_alt_kernel}" != "%{nil}"
%if 0%{?build_kernels:1}
%{error:alt_kernel and build_kernels are mutually exclusive}
exit 1
%endif
%global		_build_kernels		%{alt_kernel}
%else
%global		_build_kernels		%{?build_kernels:,%{?build_kernels}}
%endif

# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0

%define		kbrs	%(echo %{_build_kernels} | tr , '\\n' | while read n ; do echo %%undefine alt_kernel ; [ -z "$n" ] || echo %%define alt_kernel $n ; echo "BuildRequires:kernel%%{_alt_kernel}-module-build >= 3:2.6.20.2" ; done)
%define		kpkg	%(echo %{_build_kernels} | tr , '\\n' | while read n ; do echo %%undefine alt_kernel ; [ -z "$n" ] || echo %%define alt_kernel $n ; echo %%kernel_pkg ; done)
%define		bkpkg	%(echo %{_build_kernels} | tr , '\\n' | while read n ; do echo %%undefine alt_kernel ; [ -z "$n" ] || echo %%define alt_kernel $n ; echo %%build_kernel_pkg ; done)

%define		rel	1
%define		snap	20140817
%define		pname	rtl8812au
Summary:	Driver for AC1200 (802.11ac) Wireless Dual-Band USB Adapter
Name:		%{pname}%{_alt_kernel}
Version:	4.2.2_7502.20130517
Release:	0.%{snap}.%{rel}%{?_pld_builder:@%{_kernel_ver_str}}
License:	GPL
Group:		Base/Kernel
URL:		http://www.realtek.com.tw/
#Source0:	https://github.com/abperiasamy/rtl8812AU_8821AU_linux/archive/v%{version}/%{name}-%{version}.tar.gz
Source0:	https://github.com/abperiasamy/rtl8812AU_8821AU_linux/archive/master/%{name}-%{version}-%{snap}.tar.gz
# Source0-md5:	988810755bc6e687d358475861a2a6ca
Patch0:		disable-CONFIG_IOCTL_CFG80211.patch
Patch1:		usb-ids.patch
BuildRequires:	rpmbuild(macros) >= 1.678
%{?with_dist_kernel:%{expand:%kbrs}}
BuildRoot:	%{tmpdir}/%{pname}-%{version}-root-%(id -u -n)

%description
Driver for AC1200 (802.11ac) Wireless Dual-Band USB Adapter.

%define	kernel_pkg()\
%package -n kernel%{_alt_kernel}-net-rtl8812au\
Summary:	Driver for AC1200 (802.11ac) Wireless Dual-Band USB Adapter\
Release:	%{rel}@%{_kernel_ver_str}\
Group:		Base/Kernel\
Requires(post,postun):	/sbin/depmod\
%if %{with dist_kernel}\
%requires_releq_kernel\
Requires(postun):	%releq_kernel\
%endif\
\
%description -n kernel%{_alt_kernel}-net-rtl8812au\
Driver for AC1200 (802.11ac) Wireless Dual-Band USB Adapter\
\
%files -n kernel%{_alt_kernel}-net-rtl8812au\
%defattr(644,root,root,755)\
/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless/*.ko*\
\
%post	-n kernel%{_alt_kernel}-net-rtl8812au\
%depmod %{_kernel_ver}\
\
%postun	-n kernel%{_alt_kernel}-net-rtl8812au\
%depmod %{_kernel_ver}\
%{nil}

%define build_kernel_pkg()\
%{__make} clean KVER=%{_kernel_ver}\
%{__make} modules KVER=%{_kernel_ver}\
%install_kernel_modules -D installed -m 8812au -d kernel/drivers/net/wireless\
%{nil}

%{expand:%kpkg}

%prep
#%setup -q -n %{pname}-%{version}
%setup -q -n rtl8812AU_8821AU_linux-master
%patch0 -p1
%patch1 -p1

%build
%{expand:%bkpkg}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

cp -a installed/* $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT
