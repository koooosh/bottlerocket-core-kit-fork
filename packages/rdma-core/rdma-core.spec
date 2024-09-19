Name: %{_cross_os}rdma-core
Version: 53.0
Release: 1%{?dist}
Summary: RDMA core userspace libraries and daemons
License: MIT OR GPL-2.0-only
Source0: https://github.com/linux-rdma/rdma-core/releases/download/v%{version}/rdma-core-%{version}.tar.gz
Source100: rdma-core-tmpfiles.conf

BuildRequires: cmake >= 2.8.11
BuildRequires: %{_cross_os}libnl-devel
BuildRequires: %{_cross_os}glibc-devel

%description
%{summary}.

%package devel
Summary: RDMA core development libraries and headers
Provides: %{_cross_os}rdma-core-devel

%description devel
%{summary}.

%prep
%autosetup -n rdma-core-%{version} -p1

%build
%{cross_cmake} . \
  -DNO_PYVERBS=1 \
  -DNO_MAN_PAGES=1 \
  -DENABLE_STATIC=1 \
  -DCMAKE_INSTALL_LIBDIR:PATH=%{_cross_libdir} \
  -DCMAKE_INSTALL_BINDIR:PATH=%{_cross_bindir} \
  -DCMAKE_INSTALL_SBINDIR:PATH=%{_cross_sbindir} \
  -DCMAKE_INSTALL_INCLUDEDIR:PATH=%{_cross_includedir} \
  -DCMAKE_INSTALL_SYSCONFDIR:PATH=%{_cross_sysconfdir} \
  -DCMAKE_INSTALL_FULL_SYSCONFDIR:PATH=%{_cross_sysconfdir} \

%make_build

%install
%make_install

install -d %{buildroot}%{_cross_tmpfilesdir}
install -p -m 0644 %{S:100} %{buildroot}%{_cross_tmpfilesdir}/rdma-core.conf

install -d %{buildroot}%{_cross_factorydir}%{_cross_sysconfdir}/rdma-core/libibverbs.d
install -p %{buildroot}%{_cross_sysconfdir}/libibverbs.d/efa.driver %{buildroot}%{_cross_factorydir}%{_cross_sysconfdir}/rdma-core/libibverbs.d

%files
%license COPYING.*
%{_cross_attribution_file}
%{_cross_tmpfilesdir}/rdma-core.conf
%{_cross_factorydir}%{_cross_sysconfdir}/rdma-core/libibverbs.d/efa.driver
%{_cross_libdir}/libefa.so.*
# Below binary is used to verify devices
# TODO : put this in a separate "extras" subpkg
%{_cross_bindir}/ibv_devices
%exclude %{_cross_prefix}/*
# TODO : list specific excludes for all other devices besides EFA in libdir instead of below wildcard
%exclude %{_cross_libdir}/*
%exclude %{_cross_bindir}/*
%exclude %{_cross_sbindir}/*
%exclude %{_cross_includedir}/*
%exclude %{_cross_sysconfdir}/*

%files devel
%{_cross_libdir}/libefa.a
%{_cross_libdir}/libefa.so
%{_cross_libdir}/libibverbs/libefa-rdmav34.so
%{_cross_pkgconfigdir}/libefa.pc

%changelog
