%global pypi_name pbr

%if 0%{?fedora}
%global with_python3 1
%endif

%if 0%{?fedora} > 19
# we don't have the necessary br's, yet
%global do_test 0
%endif

Name:           python-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        Python Build Reasonableness

License:        ASL 2.0
URL:            http://pypi.python.org/pypi/pbr
Source0:        http://pypi.python.org/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-d2to1

%if 0%{?do_test} == 1
BuildRequires:  python-coverage
BuildRequires:  python-hacking
BuildRequires:  python-mock
BuildRequires:  python-testrepository
BuildRequires:  python-testresources
BuildRequires:  python-testscenarios
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  gnupg
%endif


%if 0%{?rhel}==6
BuildRequires: python-sphinx10
%else
BuildRequires: python-sphinx >= 1.1.3
%endif

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-d2to1
%endif

%description
PBR is a library that injects some useful and sensible default behaviors into 
your setuptools run. It started off life as the chunks of code that were copied
between all of the OpenStack projects. Around the time that OpenStack hit 18 
different projects each with at least 3 active branches, it seems like a good 
time to make that code into a proper re-usable library.

%if 0%{?with_python3}
%package -n python3-pbr
Summary:        Python Build Reasonableness

%description -n python3-pbr
Manage dynamic plugins for Python applications
%endif

%prep
%setup -q -n %{pypi_name}-%{upstream_version}
rm -rf {test-,}requirements.txt pbr.egg-info/requires.txt

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
export SKIP_PIP_INSTALL=1
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

# generate html docs 
%if 0%{?rhel}==6
sphinx-1.0-build doc/source html
%else
sphinx-build doc/source html
%endif
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}


%install
# Must do the python3 install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root=%{buildroot}
popd
%endif
%{__python} setup.py install --skip-build --root %{buildroot}
rm -rf %{buildroot}%{python_sitelib}/pbr/tests

%if 0%{?do_test} 
%check
%{__python} setup.py test
%endif

%files
%license LICENSE
%doc html README.rst
%{_bindir}/pbr
%{python_sitelib}/*.egg-info
%{python_sitelib}/%{pypi_name}

%if 0%{?with_python3}
%files -n python3-pbr
%license LICENSE
%doc html README.rst
%{python3_sitelib}/*.egg-info
%{python3_sitelib}/%{pypi_name}
%endif

%changelog
