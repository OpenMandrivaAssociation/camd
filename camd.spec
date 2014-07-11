%define NAME	CAMD
%define major	2
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname %{name} -d

Name:		camd
Version:	2.3.1
Release:	4
Epoch:		1
Summary:	Routines for permuting sparse matricies prior to factorization
Group:		System/Libraries
License:	LGPLv2+
URL:		http://www.cise.ufl.edu/research/sparse/camd/
Source0:	http://www.cise.ufl.edu/research/sparse/camd/%{NAME}-%{version}.tar.gz
BuildRequires:	suitesparse-common-devel >= 4.0.0

%description
CAMD provides a set of routines for permuting sparse matricies prior
to factorization.

%package -n %{libname}
Summary:	Library of routines for permuting sparse matricies prior to factorization
Group:		System/Libraries

%description -n %{libname}
CAMD provides a set of routines for permuting sparse matricies prior
to factorization.

This package contains the library needed to run programs dynamically
linked against %{NAME}.

%package -n %{devname}
Summary:	C routines for permuting sparse matricies prior to factorization
Group:		Development/C
Requires:	suitesparse-common-devel >= 4.0.0
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
CAMD provides a set of routines for permuting sparse matricies prior
to factorization.

This package contains the files needed to develop applications which
use %{name}.

%prep
%setup -q -c -n %{name}-%{version}
cd %{NAME}
find . -perm 0640 | xargs chmod 0644
mkdir ../SuiteSparse_config
ln -sf %{_includedir}/suitesparse/SuiteSparse_config.* ../SuiteSparse_config

%build
cd %{NAME}
pushd Lib
    %global optflags %{optflags} -fforce-addr -frename-registers -funroll-loops -Ofast
    %make -f GNUmakefile CC=gcc CFLAGS="%{optflags} -fPIC -I%{_includedir}/suitesparse" INC=
    gcc %{ldflags} -shared -Wl,-soname,lib%{name}.so.%{major} -o lib%{name}.so.%{version} -lm *.o
popd

%install
cd %{NAME}

install -d -m 755 %{buildroot}%{_libdir} 
install -d -m 755 %{buildroot}%{_includedir}/suitesparse 

for f in Lib/*.so*; do
    install -m 755 $f %{buildroot}%{_libdir}/`basename $f`
done
for f in Lib/*.a; do
    install -m 644 $f %{buildroot}%{_libdir}/`basename $f`
done
for f in Include/*.h; do
    install -m 644 $f %{buildroot}%{_includedir}/suitesparse/`basename $f`
done

ln -s lib%{name}.so.%{version} %{buildroot}%{_libdir}/lib%{name}.so

install -d -m 755 %{buildroot}%{_docdir}/%{name}
install -m 644 README.txt Doc/*.txt Doc/*.pdf Doc/ChangeLog Doc/License %{buildroot}%{_docdir}/%{name}

%files -n %{libname}
%{_libdir}/lib%{name}.so.*

%files -n %{devname}
%{_docdir}/%{name}
%{_includedir}/*
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}.a

