Summary:        Kubernetes Dashboard UI
Name:           kubernetes-dashboard
Version:        1.6.3
Release:        2%{?dist}
License:        Apache-2.0
URL:            https://github.com/kubernetes/dashboard
Source0:        %{name}-v%{version}.tar.gz
%define sha1    kubernetes-dashboard=8e06cb5cd145ffa5c691c3af5fc6e49caececfb2
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  glibc-devel
BuildRequires:  go
BuildRequires:  linux-api-headers
BuildRequires:  nodejs
BuildRequires:  nodejs
BuildRequires:  openjre8
BuildRequires:  which
Requires:       nodejs
Requires:       openjre8

%description
Kubernetes Dashboard UI.

%prep
%setup -q -n dashboard-%{version}

%build
export PATH=${PATH}:/usr/bin
sed -i 's/"google-closure-library": "\*"/"google-closure-library": "v20170521"/' ./bower.json
npm install
npm install babel-loader@7.1.1
./build/postinstall.sh
./node_modules/.bin/gulp build

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}/opt/k8dashboard
cp -p -r ./dist/amd64/dashboard %{buildroot}%{_bindir}/
cp -p -r ./dist/amd64/locale_conf.json %{buildroot}/opt/k8dashboard/
cp -p -r ./dist/amd64/public %{buildroot}/opt/k8dashboard/
cp -p -r ./src/deploy/Dockerfile %{buildroot}/opt/k8dashboard/

%check
# dashboard unit tests require chrome browser binary not present in PhotonOS

%files
%defattr(-,root,root)
%{_bindir}/dashboard
/opt/k8dashboard/Dockerfile
/opt/k8dashboard/locale_conf.json
/opt/k8dashboard/public/*

%changelog
*    Tue Apr 03 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.6.3-2
-    Fix build break in google-closure-library.
*    Mon Sep 11 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.6.3-1
-    kubernetes-dashboard 1.6.3.
*    Fri Jul 14 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.6.1-1
-    Initial version of kubernetes-dashboard package for Photon.
