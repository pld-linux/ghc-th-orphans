#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	th-orphans
Summary:	Orphan instances for TH datatypes
Summary(pl.UTF-8):	Osierocone instancje typów danych TH
Name:		ghc-%{pkgname}
Version:	0.13.3
Release:	0.1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/th-orphans
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	d56c8222885e82e47076a27224fd4ced
URL:		http://hackage.haskell.org/package/th-orphans
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 4.3
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-generic-deriving >= 1.9
BuildRequires:	ghc-template-haskell
BuildRequires:	ghc-th-lift >= 0.7.1
BuildRequires:	ghc-th-lift-instances
BuildRequires:	ghc-th-reify-many >= 0.1
BuildRequires:	ghc-th-reify-many < 0.2
%if %{with prof}
BuildRequires:	ghc-base-prof >= 4.3
BuildRequires:	ghc-base-prof < 5
BuildRequires:	ghc-generic-deriving-prof >= 1.9
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-template-haskell-prof
BuildRequires:	ghc-th-lift-instances-prof
BuildRequires:	ghc-th-lift-prof >= 0.7.1
BuildRequires:	ghc-th-reify-many-prof >= 0.1
BuildRequires:	ghc-th-reify-many-prof < 0.2
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_releq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
Requires:	ghc-base >= 4.3
Requires:	ghc-base < 5
Requires:	ghc-generic-deriving >= 1.9
Requires:	ghc-template-haskell
Requires:	ghc-th-lift >= 0.7.1
Requires:	ghc-th-lift-instances
Requires:	ghc-th-reify-many >= 0.1
Requires:	ghc-th-reify-many < 0.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
Orphan instances for TH datatypes. In particular, instances for Ord
and Lift, as well as a few missing Show / Eq. These instances used to
live in haskell-src-meta, and that's where the version number started.

%description -l pl.UTF-8
Osierocone instancje typów danych TH - w szczególności instancje Ord i
Lift, a także kilka brakujących Show / Eq. Instancje te były wcześniej
w haskell-src-meta, i w tym pakiecie zaczęła się numeracja wersji.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC.
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 4.3
Requires:	ghc-base-prof < 5
Requires:	ghc-generic-deriving-prof >= 1.9
Requires:	ghc-template-haskell-prof
Requires:	ghc-th-lift-instances-prof
Requires:	ghc-th-lift-prof >= 0.7.1
Requires:	ghc-th-reify-many-prof >= 0.1
Requires:	ghc-th-reify-many-prof < 0.2

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/HSth-orphans-%{version}.o
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSth-orphans-%{version}.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/TH
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/TH/*.hi

%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSth-orphans-%{version}_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/TH/*.p_hi
