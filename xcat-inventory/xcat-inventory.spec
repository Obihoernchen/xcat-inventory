Summary: xCAT Inventory
Name: xcat-inventory
Version: %{?version:%{version}}%{!?version:%(cat Version)}
Release: %{?release:%{release}}%{!?release:%(cat Release)}
Epoch: 4
License: EPL
Group: Applications/System
Source: xcat-inventory-%{version}.tar.gz
Packager: IBM Corp.
Vendor: IBM Corp.
Distribution: %{?_distribution:%{_distribution}}%{!?_distribution:%{_vendor}}
Prefix: /opt/xcat
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root
Requires: python-psycopg2 python-sqlalchemy MySQL-python PyYAML python-six

%ifos linux
BuildArch: noarch
%endif

%description

%prep
%setup -q -n xcat-inventory

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{prefix}/bin
install -d $RPM_BUILD_ROOT/%{prefix}/lib/python/xcclient
install -d $RPM_BUILD_ROOT/%{prefix}/lib/python/xcclient/inventory
install -d $RPM_BUILD_ROOT/%{prefix}/lib/python/xcclient/inventory/schema

install -m755 cli/* $RPM_BUILD_ROOT/%{prefix}/bin
install -m644 xcclient/*.py $RPM_BUILD_ROOT/%{prefix}/lib/python/xcclient
install -m644 xcclient/inventory/*.py $RPM_BUILD_ROOT/%{prefix}/lib/python/xcclient/inventory
install -m644 xcclient/inventory/schema/*.yaml $RPM_BUILD_ROOT/%{prefix}/lib/python/xcclient/inventory/schema

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)

%{prefix}

%changelog

%post

%preun

