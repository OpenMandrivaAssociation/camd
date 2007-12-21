%define name	camd
%define NAME	CAMD
%define version	2.2.0
%define release	%mkrel 1
%define major	%{version}
%define libname	%mklibname %{name} %{major}
%define develname	%mklibname %{name} -d

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Constrained approximate minimum degree ordering
Group:		System/Libraries
License:	LGPL
URL:		http://www.cise.ufl.edu/research/sparse/amd/
Source0:	http://www.cise.ufl.edu/research/sparse/amd/%{NAME}-%{version}.tar.gz
Source1:	http://www.cise.ufl.edu/research/sparse/UFconfig/UFconfig-3.0.0.tar.gz

%description
CAMD is a set of routines for ordering a sparse matrix prior to Cholesky
factorization (or for LU factorization with diagonal pivoting). There are
versions in both C and Fortran.

%package -n %{libname}
Summary:	Main library for %{name}
Group:		System/Libraries

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n %{develname}
Summary:	Headers for developing programs that will use %{name}
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%prep
%setup -q -c 
%setup -q -c -a 0 -a 1
%setup -q -D -T -n %{name}-%{version}/%{NAME}

%build
cd Lib
    %{__make} -f GNUmakefile CFLAGS="$RPM_OPT_FLAGS -fPIC" 
    gcc -shared -Wl,-soname,libcamd.so.%{major} -o ../Lib/libcamd.so.%{version} `ls *.o`
cd ..
cd Doc
    %{__make}
cd ..


%install
rm -rf %{buildroot}

install -d -m 755 %{buildroot}%{_libdir}
install -m 755 Lib/libcamd.so.%{version} %{buildroot}%{_libdir}
install -m 644 Lib/libcamd.a %{buildroot}%{_libdir}
(cd %{buildroot}%{_libdir} && ln -s libcamd.so.%{version} libcamd.so)

install -d -m 755 %{buildroot}%{_includedir}
install -m 644 Include/*.h %{buildroot}%{_includedir}

install -d -m 755 %{buildroot}%{_docdir}/%{name}
install -m 644 README.txt Doc/CAMD_UserGuide.pdf %{buildroot}%{_docdir}/%{name}

%clean
rm -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-,root,root)
%{_docdir}/%{name}
%{_libdir}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a


