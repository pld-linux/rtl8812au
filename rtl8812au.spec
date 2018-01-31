#
# Conditional build:
%bcond_with	verbose		# verbose build (V=1)

# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0

%define		rel	1
%define		snap	20180131
%define		pname	rtl8812au
Summary:	Driver for AC1200 (802.11ac) Wireless Dual-Band USB Adapter
Name:		%{pname}%{_alt_kernel}
Version:	5.2.20_25672.20171213
Release:	0.%{snap}.%{rel}%{?_pld_builder:@%{_kernel_ver_str}}
License:	GPL
Group:		Base/Kernel
Source0:	https://github.com/gordboy/rtl8812au/archive/master/%{pname}-%{version}-%{snap}.tar.gz
# Source0-md5:	5fc6e00f86ce93feabf3fd3655207e12
# good luck finding this chip on Realtek website :/
#URL:		http://www.realtek.com.tw/
URL:		https://github.com/gordboy/rtl8812au
Patch0:		gcc-4.9.patch
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
%doc Realtek_Changelog.txt README.md\
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
%setup -q -n %{pname}-master
%patch0 -p1

%build
%{expand:%build_kernel_packages}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

cp -a installed/* $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT
