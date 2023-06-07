#
# Conditional build:
%bcond_with	verbose		# verbose build (V=1)

# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0

%define		rel	2
%define		basever	20210629
%define		snap	20230521
%define		pname	rtl8812au
Summary:	Driver for AC1200 (802.11ac) Wireless Dual-Band USB Adapter
Name:		%{pname}%{_alt_kernel}
Version:	5.13.6.%{snap}
Epoch:		2
Release:	%{rel}%{?_pld_builder:@%{_kernel_ver_str}}
License:	GPL
Group:		Base/Kernel
Source0:	https://github.com/morrownr/8812au-%{basever}/archive/main/%{pname}-%{version}.tar.gz
# Source0-md5:	8ae562b54e89a05894fa4daa0de388ec
Patch0:		no-arch-override.patch
# good luck finding this chip on Realtek website :/
#URL:		http://www.realtek.com.tw/
URL:		https://github.com/morrownr/8812au
BuildRequires:	rpmbuild(macros) >= 1.701
%{expand:%buildrequires_kernel kernel%%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRoot:	%{tmpdir}/%{pname}-%{version}-root-%(id -u -n)

%description
Driver for AC1200 (802.11ac) Wireless Dual-Band USB Adapter.

%define	kernel_pkg()\
%package -n kernel%{_alt_kernel}-net-rtl8812au\
Summary:	Driver for AC1200 (802.11ac) Wireless Dual-Band USB Adapter\
Release:	%{rel}@%{_kernel_ver_str}\
Group:		Base/Kernel\
Requires(post,postun):	/sbin/depmod\
%requires_releq_kernel\
Requires(postun):	%releq_kernel\
\
%description -n kernel%{_alt_kernel}-net-rtl8812au\
Driver for AC1200 (802.11ac) Wireless Dual-Band USB Adapter\
\
%files -n kernel%{_alt_kernel}-net-rtl8812au\
%defattr(644,root,root,755)\
%doc README.md\
/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless/*.ko*\
\
%post	-n kernel%{_alt_kernel}-net-rtl8812au\
%depmod %{_kernel_ver}\
\
%postun	-n kernel%{_alt_kernel}-net-rtl8812au\
%depmod %{_kernel_ver}\
%{nil}

%define build_kernel_pkg()\
%{__make} clean KVER=%{_kernel_ver} KSRC=%{_kernelsrcdir}\
%{__make} modules KVER=%{_kernel_ver} KSRC=%{_kernelsrcdir}\
%install_kernel_modules -D installed -m 8812au -d kernel/drivers/net/wireless\
%{nil}

%{expand:%create_kernel_packages}

%prep
%setup -q -n 8812au-%{basever}-main
%patch0 -p1

%build
%{expand:%build_kernel_packages}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

cp -a installed/* $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT
