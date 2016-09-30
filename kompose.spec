%if 0%{?fedora} || 0%{?rhel} == 6
# Not all devel deps exist in Fedora so you can't
# install the devel rpm so we need to build without
# devel or unit_test for now
%global with_devel 0
%global with_bundled 1
%global with_debug 1
%global with_check 1
%global with_unit_test 0
%else
%global with_devel 0
%global with_bundled 1
%global with_debug 0
%global with_check 0
%global with_unit_test 0
%endif

# https://fedoraproject.org/wiki/PackagingDrafts/Go#Debuginfo
# https://bugzilla.redhat.com/show_bug.cgi?id=995136#c12
%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

# https://fedoraproject.org/wiki/PackagingDrafts/Go#Debuginfo
%if ! 0%{?gobuild:1}
%define gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};
%endif

%global provider        github
%global provider_tld    com
%global project         skippbox
%global repo            kompose
# https://github.com/skippbox/kompose
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          822768446621d71ffd02eafd138db0d8ab4a7d0e
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

# define ldflags, buildflags, testflags here. The ldflags/buildflags
# were taken from script/.build and the testflags were taken from
# script/test-unit. We will need to periodically check these for
# consistency.
%global ldflags "-w -X github.com/skippbox/kompose/version.GITCOMMIT=%{shortcommit}"
%global buildflags -tags experimental
%global testflags -cover -coverprofile=cover.out

Name:           kompose
Version:        0.1.0
Release:        0.1.git%{shortcommit}%{?dist}
Summary:        Tool to move from `docker-compose` to Kubernetes
License:        ASL 2.0
URL:            https://%{provider_prefix}
Source0:        https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

# Main package BuildRequires
%if ! 0%{?with_bundled}
# cli/main/main.go
BuildRequires: golang(github.com/urfave/cli)
# Remaining dependencies not included in main packages
BuildRequires: golang(k8s.io/kubernetes/pkg/apis/extensions/install)
BuildRequires: golang(k8s.io/kubernetes/pkg/kubectl)
BuildRequires: golang(k8s.io/kubernetes/pkg/apis/extensions)
BuildRequires: golang(github.com/docker/libcompose/lookup)
BuildRequires: golang(k8s.io/kubernetes/pkg/client/unversioned)
BuildRequires: golang(github.com/openshift/origin/pkg/deploy/api)
BuildRequires: golang(github.com/ghodss/yaml)
BuildRequires: golang(k8s.io/kubernetes/pkg/kubectl/cmd/util)
BuildRequires: golang(github.com/openshift/origin/pkg/deploy/api/install)
BuildRequires: golang(github.com/docker/libcompose/project)
BuildRequires: golang(github.com/fatih/structs)
BuildRequires: golang(github.com/docker/libcompose/config)
BuildRequires: golang(k8s.io/kubernetes/pkg/util/intstr)
BuildRequires: golang(k8s.io/kubernetes/pkg/runtime)
BuildRequires: golang(k8s.io/kubernetes/pkg/api)
BuildRequires: golang(k8s.io/kubernetes/pkg/api/unversioned)
BuildRequires: golang(k8s.io/kubernetes/pkg/api/install)
BuildRequires: golang(github.com/docker/docker/api/client/bundlefile)
BuildRequires: golang(github.com/Sirupsen/logrus)
%endif

# Main package Provides
%if 0%{?with_bundled}
Provides: bundled(golang(github.com/Azure/go-ansiterm)) = %{version}-388960b655244e76e24c75f48631564eaefade62
Provides: bundled(golang(github.com/Azure/go-ansiterm/winterm)) = %{version}-388960b655244e76e24c75f48631564eaefade62
Provides: bundled(golang(github.com/Microsoft/go-winio)) = %{version}-8f9387ea7efabb228a981b9c381142be7667967f
Provides: bundled(golang(github.com/Sirupsen/logrus)) = %{version}-98a1428efc3d732f9e377b50c8e2113e070896cf
Provides: bundled(golang(github.com/beorn7/perks/quantile)) = %{version}-3ac7bf7a47d159a033b107610db8a1b6575507a4
Provides: bundled(golang(github.com/blang/semver)) = %{version}-31b736133b98f26d5e078ec9eb591666edfd091f
Provides: bundled(golang(github.com/coreos/go-oidc/http)) = %{version}-5cf2aa52da8c574d3aa4458f471ad6ae2240fe6b
Provides: bundled(golang(github.com/coreos/go-oidc/jose)) = %{version}-5cf2aa52da8c574d3aa4458f471ad6ae2240fe6b
Provides: bundled(golang(github.com/coreos/go-oidc/key)) = %{version}-5cf2aa52da8c574d3aa4458f471ad6ae2240fe6b
Provides: bundled(golang(github.com/coreos/go-oidc/oauth2)) = %{version}-5cf2aa52da8c574d3aa4458f471ad6ae2240fe6b
Provides: bundled(golang(github.com/coreos/go-oidc/oidc)) = %{version}-5cf2aa52da8c574d3aa4458f471ad6ae2240fe6b
Provides: bundled(golang(github.com/coreos/go-systemd/journal)) = %{version}-4484981625c1a6a2ecb40a390fcb6a9bcfee76e3
Provides: bundled(golang(github.com/coreos/pkg/capnslog)) = %{version}-7f080b6c11ac2d2347c3cd7521e810207ea1a041
Provides: bundled(golang(github.com/coreos/pkg/health)) = %{version}-7f080b6c11ac2d2347c3cd7521e810207ea1a041
Provides: bundled(golang(github.com/coreos/pkg/httputil)) = %{version}-7f080b6c11ac2d2347c3cd7521e810207ea1a041
Provides: bundled(golang(github.com/coreos/pkg/timeutil)) = %{version}-7f080b6c11ac2d2347c3cd7521e810207ea1a041
Provides: bundled(golang(github.com/davecgh/go-spew/spew)) = %{version}-5215b55f46b2b919f50a1df0eaa5886afe4e3b3d
Provides: bundled(golang(github.com/dgrijalva/jwt-go)) = %{version}-5ca80149b9d3f8b863af0e2bb6742e608603bd99
Provides: bundled(golang(github.com/docker/distribution)) = %{version}-4e17ab5d319ac5b70b2769442947567a83386fbc
Provides: bundled(golang(github.com/docker/distribution/context)) = %{version}-4e17ab5d319ac5b70b2769442947567a83386fbc
Provides: bundled(golang(github.com/docker/distribution/digest)) = %{version}-4e17ab5d319ac5b70b2769442947567a83386fbc
Provides: bundled(golang(github.com/docker/distribution/manifest)) = %{version}-4e17ab5d319ac5b70b2769442947567a83386fbc
Provides: bundled(golang(github.com/docker/distribution/manifest/schema1)) = %{version}-4e17ab5d319ac5b70b2769442947567a83386fbc
Provides: bundled(golang(github.com/docker/distribution/manifest/schema2)) = %{version}-4e17ab5d319ac5b70b2769442947567a83386fbc
Provides: bundled(golang(github.com/docker/distribution/reference)) = %{version}-4e17ab5d319ac5b70b2769442947567a83386fbc
Provides: bundled(golang(github.com/docker/distribution/registry/api/errcode)) = %{version}-4e17ab5d319ac5b70b2769442947567a83386fbc
Provides: bundled(golang(github.com/docker/distribution/registry/api/v2)) = %{version}-4e17ab5d319ac5b70b2769442947567a83386fbc
Provides: bundled(golang(github.com/docker/distribution/registry/client)) = %{version}-4e17ab5d319ac5b70b2769442947567a83386fbc
Provides: bundled(golang(github.com/docker/distribution/registry/client/auth)) = %{version}-4e17ab5d319ac5b70b2769442947567a83386fbc
Provides: bundled(golang(github.com/docker/distribution/registry/client/transport)) = %{version}-4e17ab5d319ac5b70b2769442947567a83386fbc
Provides: bundled(golang(github.com/docker/distribution/registry/storage/cache)) = %{version}-4e17ab5d319ac5b70b2769442947567a83386fbc
Provides: bundled(golang(github.com/docker/distribution/registry/storage/cache/memory)) = %{version}-4e17ab5d319ac5b70b2769442947567a83386fbc
Provides: bundled(golang(github.com/docker/distribution/uuid)) = %{version}-4e17ab5d319ac5b70b2769442947567a83386fbc
Provides: bundled(golang(github.com/docker/docker/api/client/bundlefile)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/api/types/backend)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/builder)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/builder/dockerignore)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/cliconfig)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/cliconfig/configfile)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/daemon/graphdriver)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/image)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/image/v1)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/layer)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/opts)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/pkg/archive)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/pkg/chrootarchive)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/pkg/fileutils)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/pkg/gitutils)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/pkg/homedir)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/pkg/httputils)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/pkg/idtools)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/pkg/ioutils)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/pkg/jsonlog)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/pkg/jsonmessage)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/pkg/longpath)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/pkg/mflag)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/pkg/mount)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/pkg/plugins)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/pkg/plugins/transport)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/pkg/pools)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/pkg/progress)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/pkg/promise)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/pkg/random)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/pkg/reexec)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/pkg/signal)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/pkg/stdcopy)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/pkg/streamformatter)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/pkg/stringid)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/pkg/symlink)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/pkg/system)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/pkg/tarsum)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/pkg/term)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/pkg/term/windows)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/pkg/urlutil)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/reference)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/registry)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/docker/runconfig/opts)) = %{version}-e4a0dbc47232e3a9da4cfe6ce44f250e6e85ed43
Provides: bundled(golang(github.com/docker/engine-api/client)) = %{version}-1d247454d4307fb1ddf10d09fd2996394b085904
Provides: bundled(golang(github.com/docker/engine-api/client/transport)) = %{version}-1d247454d4307fb1ddf10d09fd2996394b085904
Provides: bundled(golang(github.com/docker/engine-api/client/transport/cancellable)) = %{version}-1d247454d4307fb1ddf10d09fd2996394b085904
Provides: bundled(golang(github.com/docker/engine-api/types)) = %{version}-1d247454d4307fb1ddf10d09fd2996394b085904
Provides: bundled(golang(github.com/docker/engine-api/types/blkiodev)) = %{version}-1d247454d4307fb1ddf10d09fd2996394b085904
Provides: bundled(golang(github.com/docker/engine-api/types/container)) = %{version}-1d247454d4307fb1ddf10d09fd2996394b085904
Provides: bundled(golang(github.com/docker/engine-api/types/events)) = %{version}-1d247454d4307fb1ddf10d09fd2996394b085904
Provides: bundled(golang(github.com/docker/engine-api/types/filters)) = %{version}-1d247454d4307fb1ddf10d09fd2996394b085904
Provides: bundled(golang(github.com/docker/engine-api/types/network)) = %{version}-1d247454d4307fb1ddf10d09fd2996394b085904
Provides: bundled(golang(github.com/docker/engine-api/types/reference)) = %{version}-1d247454d4307fb1ddf10d09fd2996394b085904
Provides: bundled(golang(github.com/docker/engine-api/types/registry)) = %{version}-1d247454d4307fb1ddf10d09fd2996394b085904
Provides: bundled(golang(github.com/docker/engine-api/types/strslice)) = %{version}-1d247454d4307fb1ddf10d09fd2996394b085904
Provides: bundled(golang(github.com/docker/engine-api/types/swarm)) = %{version}-1d247454d4307fb1ddf10d09fd2996394b085904
Provides: bundled(golang(github.com/docker/engine-api/types/time)) = %{version}-1d247454d4307fb1ddf10d09fd2996394b085904
Provides: bundled(golang(github.com/docker/engine-api/types/versions)) = %{version}-1d247454d4307fb1ddf10d09fd2996394b085904
Provides: bundled(golang(github.com/docker/go-connections/nat)) = %{version}-f549a9393d05688dff0992ef3efd8bbe6c628aeb
Provides: bundled(golang(github.com/docker/go-connections/sockets)) = %{version}-f549a9393d05688dff0992ef3efd8bbe6c628aeb
Provides: bundled(golang(github.com/docker/go-connections/tlsconfig)) = %{version}-f549a9393d05688dff0992ef3efd8bbe6c628aeb
Provides: bundled(golang(github.com/docker/go-units)) = %{version}-0bbddae09c5a5419a8c6dcdd7ff90da3d450393b
Provides: bundled(golang(github.com/docker/libcompose/config)) = %{version}-c10fa1d7ef4e0fe05b2bc9ca7444ea421b1df236
Provides: bundled(golang(github.com/docker/libcompose/docker)) = %{version}-c10fa1d7ef4e0fe05b2bc9ca7444ea421b1df236
Provides: bundled(golang(github.com/docker/libcompose/docker/builder)) = %{version}-c10fa1d7ef4e0fe05b2bc9ca7444ea421b1df236
Provides: bundled(golang(github.com/docker/libcompose/docker/client)) = %{version}-c10fa1d7ef4e0fe05b2bc9ca7444ea421b1df236
Provides: bundled(golang(github.com/docker/libcompose/docker/network)) = %{version}-c10fa1d7ef4e0fe05b2bc9ca7444ea421b1df236
Provides: bundled(golang(github.com/docker/libcompose/docker/volume)) = %{version}-c10fa1d7ef4e0fe05b2bc9ca7444ea421b1df236
Provides: bundled(golang(github.com/docker/libcompose/labels)) = %{version}-c10fa1d7ef4e0fe05b2bc9ca7444ea421b1df236
Provides: bundled(golang(github.com/docker/libcompose/logger)) = %{version}-c10fa1d7ef4e0fe05b2bc9ca7444ea421b1df236
Provides: bundled(golang(github.com/docker/libcompose/lookup)) = %{version}-c10fa1d7ef4e0fe05b2bc9ca7444ea421b1df236
Provides: bundled(golang(github.com/docker/libcompose/project)) = %{version}-c10fa1d7ef4e0fe05b2bc9ca7444ea421b1df236
Provides: bundled(golang(github.com/docker/libcompose/project/events)) = %{version}-c10fa1d7ef4e0fe05b2bc9ca7444ea421b1df236
Provides: bundled(golang(github.com/docker/libcompose/project/options)) = %{version}-c10fa1d7ef4e0fe05b2bc9ca7444ea421b1df236
Provides: bundled(golang(github.com/docker/libcompose/utils)) = %{version}-c10fa1d7ef4e0fe05b2bc9ca7444ea421b1df236
Provides: bundled(golang(github.com/docker/libcompose/version)) = %{version}-c10fa1d7ef4e0fe05b2bc9ca7444ea421b1df236
Provides: bundled(golang(github.com/docker/libcompose/yaml)) = %{version}-c10fa1d7ef4e0fe05b2bc9ca7444ea421b1df236
Provides: bundled(golang(github.com/docker/libtrust)) = %{version}-9cbd2a1374f46905c68a4eb3694a130610adc62a
Provides: bundled(golang(github.com/emicklei/go-restful)) = %{version}-7c47e2558a0bbbaba9ecab06bc6681e73028a28a
Provides: bundled(golang(github.com/emicklei/go-restful/log)) = %{version}-7c47e2558a0bbbaba9ecab06bc6681e73028a28a
Provides: bundled(golang(github.com/emicklei/go-restful/swagger)) = %{version}-7c47e2558a0bbbaba9ecab06bc6681e73028a28a
Provides: bundled(golang(github.com/evanphx/json-patch)) = %{version}-465937c80b3c07a7c7ad20cc934898646a91c1de
Provides: bundled(golang(github.com/fatih/structs)) = %{version}-be738c8546f55b34e60125afa50ed73a9a9c460e
Provides: bundled(golang(github.com/flynn/go-shlex)) = %{version}-3f9db97f856818214da2e1057f8ad84803971cff
Provides: bundled(golang(github.com/fsouza/go-dockerclient)) = %{version}-bf97c77db7c945cbcdbf09d56c6f87a66f54537b
Provides: bundled(golang(github.com/fsouza/go-dockerclient/external/github.com/Sirupsen/logrus)) = %{version}-bf97c77db7c945cbcdbf09d56c6f87a66f54537b
Provides: bundled(golang(github.com/fsouza/go-dockerclient/external/github.com/docker/docker/opts)) = %{version}-bf97c77db7c945cbcdbf09d56c6f87a66f54537b
Provides: bundled(golang(github.com/fsouza/go-dockerclient/external/github.com/docker/docker/pkg/archive)) = %{version}-bf97c77db7c945cbcdbf09d56c6f87a66f54537b
Provides: bundled(golang(github.com/fsouza/go-dockerclient/external/github.com/docker/docker/pkg/fileutils)) = %{version}-bf97c77db7c945cbcdbf09d56c6f87a66f54537b
Provides: bundled(golang(github.com/fsouza/go-dockerclient/external/github.com/docker/docker/pkg/homedir)) = %{version}-bf97c77db7c945cbcdbf09d56c6f87a66f54537b
Provides: bundled(golang(github.com/fsouza/go-dockerclient/external/github.com/docker/docker/pkg/idtools)) = %{version}-bf97c77db7c945cbcdbf09d56c6f87a66f54537b
Provides: bundled(golang(github.com/fsouza/go-dockerclient/external/github.com/docker/docker/pkg/ioutils)) = %{version}-bf97c77db7c945cbcdbf09d56c6f87a66f54537b
Provides: bundled(golang(github.com/fsouza/go-dockerclient/external/github.com/docker/docker/pkg/longpath)) = %{version}-bf97c77db7c945cbcdbf09d56c6f87a66f54537b
Provides: bundled(golang(github.com/fsouza/go-dockerclient/external/github.com/docker/docker/pkg/pools)) = %{version}-bf97c77db7c945cbcdbf09d56c6f87a66f54537b
Provides: bundled(golang(github.com/fsouza/go-dockerclient/external/github.com/docker/docker/pkg/promise)) = %{version}-bf97c77db7c945cbcdbf09d56c6f87a66f54537b
Provides: bundled(golang(github.com/fsouza/go-dockerclient/external/github.com/docker/docker/pkg/stdcopy)) = %{version}-bf97c77db7c945cbcdbf09d56c6f87a66f54537b
Provides: bundled(golang(github.com/fsouza/go-dockerclient/external/github.com/docker/docker/pkg/system)) = %{version}-bf97c77db7c945cbcdbf09d56c6f87a66f54537b
Provides: bundled(golang(github.com/fsouza/go-dockerclient/external/github.com/docker/go-units)) = %{version}-bf97c77db7c945cbcdbf09d56c6f87a66f54537b
Provides: bundled(golang(github.com/fsouza/go-dockerclient/external/github.com/hashicorp/go-cleanhttp)) = %{version}-bf97c77db7c945cbcdbf09d56c6f87a66f54537b
Provides: bundled(golang(github.com/fsouza/go-dockerclient/external/github.com/opencontainers/runc/libcontainer/user)) = %{version}-bf97c77db7c945cbcdbf09d56c6f87a66f54537b
Provides: bundled(golang(github.com/fsouza/go-dockerclient/external/golang.org/x/net/context)) = %{version}-bf97c77db7c945cbcdbf09d56c6f87a66f54537b
Provides: bundled(golang(github.com/fsouza/go-dockerclient/external/golang.org/x/sys/unix)) = %{version}-bf97c77db7c945cbcdbf09d56c6f87a66f54537b
Provides: bundled(golang(github.com/ghodss/yaml)) = %{version}-73d445a93680fa1a78ae23a5839bad48f32ba1ee
Provides: bundled(golang(github.com/gogo/protobuf/proto)) = %{version}-82d16f734d6d871204a3feb1a73cb220cc92574c
Provides: bundled(golang(github.com/golang/glog)) = %{version}-44145f04b68cf362d9c4df2182967c2275eaefed
Provides: bundled(golang(github.com/golang/groupcache/lru)) = %{version}-604ed5785183e59ae2789449d89e73f3a2a77987
Provides: bundled(golang(github.com/golang/protobuf/proto)) = %{version}-b982704f8bb716bb608144408cff30e15fbde841
Provides: bundled(golang(github.com/google/cadvisor/info/v1)) = %{version}-4dbefc9b671b81257973a33211fb12370c1a526e
Provides: bundled(golang(github.com/google/gofuzz)) = %{version}-bbcb9da2d746f8bdbd6a936686a0a6067ada0ec5
Provides: bundled(golang(github.com/gorilla/context)) = %{version}-215affda49addc4c8ef7e2534915df2c8c35c6cd
Provides: bundled(golang(github.com/gorilla/mux)) = %{version}-8096f47503459bcc74d1f4c487b7e6e42e5746b5
Provides: bundled(golang(github.com/imdario/mergo)) = %{version}-6633656539c1639d9d78127b7d47c622b5d7b6dc
Provides: bundled(golang(github.com/inconshreveable/mousetrap)) = %{version}-76626ae9c91c4f2a10f34cad8ce83ea42c93bb75
Provides: bundled(golang(github.com/jonboulle/clockwork)) = %{version}-3f831b65b61282ba6bece21b91beea2edc4c887a
Provides: bundled(golang(github.com/juju/ratelimit)) = %{version}-77ed1c8a01217656d2080ad51981f6e99adaa177
Provides: bundled(golang(github.com/matttproud/golang_protobuf_extensions/pbutil)) = %{version}-fc2b8d3a73c4867e51861bbdd5ae3c1f0869dd6a
Provides: bundled(golang(github.com/opencontainers/runc/libcontainer/cgroups)) = %{version}-7ca2aa4873aea7cb4265b1726acb24b90d8726c6
Provides: bundled(golang(github.com/opencontainers/runc/libcontainer/cgroups/fs)) = %{version}-7ca2aa4873aea7cb4265b1726acb24b90d8726c6
Provides: bundled(golang(github.com/opencontainers/runc/libcontainer/configs)) = %{version}-7ca2aa4873aea7cb4265b1726acb24b90d8726c6
Provides: bundled(golang(github.com/opencontainers/runc/libcontainer/system)) = %{version}-7ca2aa4873aea7cb4265b1726acb24b90d8726c6
Provides: bundled(golang(github.com/opencontainers/runc/libcontainer/user)) = %{version}-7ca2aa4873aea7cb4265b1726acb24b90d8726c6
Provides: bundled(golang(github.com/openshift/origin/pkg/api)) = %{version}-2e48c47ce0371eab4d23ce32c0fec6de2e964dc1
Provides: bundled(golang(github.com/openshift/origin/pkg/api/extension)) = %{version}-2e48c47ce0371eab4d23ce32c0fec6de2e964dc1
Provides: bundled(golang(github.com/openshift/origin/pkg/authorization/api)) = %{version}-2e48c47ce0371eab4d23ce32c0fec6de2e964dc1
Provides: bundled(golang(github.com/openshift/origin/pkg/build/api)) = %{version}-2e48c47ce0371eab4d23ce32c0fec6de2e964dc1
Provides: bundled(golang(github.com/openshift/origin/pkg/deploy/api)) = %{version}-2e48c47ce0371eab4d23ce32c0fec6de2e964dc1
Provides: bundled(golang(github.com/openshift/origin/pkg/deploy/api/install)) = %{version}-2e48c47ce0371eab4d23ce32c0fec6de2e964dc1
Provides: bundled(golang(github.com/openshift/origin/pkg/deploy/api/v1)) = %{version}-2e48c47ce0371eab4d23ce32c0fec6de2e964dc1
Provides: bundled(golang(github.com/openshift/origin/pkg/image/api)) = %{version}-2e48c47ce0371eab4d23ce32c0fec6de2e964dc1
Provides: bundled(golang(github.com/openshift/origin/pkg/oauth/api)) = %{version}-2e48c47ce0371eab4d23ce32c0fec6de2e964dc1
Provides: bundled(golang(github.com/openshift/origin/pkg/project/api)) = %{version}-2e48c47ce0371eab4d23ce32c0fec6de2e964dc1
Provides: bundled(golang(github.com/openshift/origin/pkg/route/api)) = %{version}-2e48c47ce0371eab4d23ce32c0fec6de2e964dc1
Provides: bundled(golang(github.com/openshift/origin/pkg/sdn/api)) = %{version}-2e48c47ce0371eab4d23ce32c0fec6de2e964dc1
Provides: bundled(golang(github.com/openshift/origin/pkg/security/api)) = %{version}-2e48c47ce0371eab4d23ce32c0fec6de2e964dc1
Provides: bundled(golang(github.com/openshift/origin/pkg/template/api)) = %{version}-2e48c47ce0371eab4d23ce32c0fec6de2e964dc1
Provides: bundled(golang(github.com/openshift/origin/pkg/user/api)) = %{version}-2e48c47ce0371eab4d23ce32c0fec6de2e964dc1
Provides: bundled(golang(github.com/openshift/origin/pkg/util/namer)) = %{version}-2e48c47ce0371eab4d23ce32c0fec6de2e964dc1
Provides: bundled(golang(github.com/pborman/uuid)) = %{version}-ca53cad383cad2479bbba7f7a1a05797ec1386e4
Provides: bundled(golang(github.com/prometheus/client_golang/prometheus)) = %{version}-3b78d7a77f51ccbc364d4bc170920153022cfd08
Provides: bundled(golang(github.com/prometheus/client_model/go)) = %{version}-fa8ad6fec33561be4280a8f0514318c79d7f6cb6
Provides: bundled(golang(github.com/prometheus/common/expfmt)) = %{version}-a6ab08426bb262e2d190097751f5cfd1cfdfd17d
Provides: bundled(golang(github.com/prometheus/common/internal/bitbucket.org/ww/goautoneg)) = %{version}-a6ab08426bb262e2d190097751f5cfd1cfdfd17d
Provides: bundled(golang(github.com/prometheus/common/model)) = %{version}-a6ab08426bb262e2d190097751f5cfd1cfdfd17d
Provides: bundled(golang(github.com/prometheus/procfs)) = %{version}-490cc6eb5fa45bf8a8b7b73c8bc82a8160e8531d
Provides: bundled(golang(github.com/spf13/cobra)) = %{version}-4c05eb1145f16d0e6bb4a3e1b6d769f4713cb41f
Provides: bundled(golang(github.com/spf13/pflag)) = %{version}-08b1a584251b5b62f458943640fc8ebd4d50aaa5
Provides: bundled(golang(github.com/ugorji/go/codec)) = %{version}-f4485b318aadd133842532f841dc205a8e339d74
Provides: bundled(golang(github.com/urfave/cli)) = %{version}-71f57d300dd6a780ac1856c005c4b518cfd498ec
Provides: bundled(golang(github.com/vbatts/tar-split/archive/tar)) = %{version}-28bc4c32f9fa9725118a685c9ddd7ffdbdbfe2c8
Provides: bundled(golang(github.com/vbatts/tar-split/tar/asm)) = %{version}-28bc4c32f9fa9725118a685c9ddd7ffdbdbfe2c8
Provides: bundled(golang(github.com/vbatts/tar-split/tar/storage)) = %{version}-28bc4c32f9fa9725118a685c9ddd7ffdbdbfe2c8
Provides: bundled(golang(github.com/vdemeester/docker-events)) = %{version}-be74d4929ec1ad118df54349fda4b0cba60f849b
Provides: bundled(golang(github.com/xeipuuv/gojsonpointer)) = %{version}-e0fe6f68307607d540ed8eac07a342c33fa1b54a
Provides: bundled(golang(github.com/xeipuuv/gojsonreference)) = %{version}-e02fc20de94c78484cd5ffb007f8af96be030a45
Provides: bundled(golang(github.com/xeipuuv/gojsonschema)) = %{version}-ac452913faa25c08bb78810d3e6f88b8a39f8f25
Provides: bundled(golang(golang.org/x/net/context)) = %{version}-62685c2d7ca23c807425dca88b11a3e2323dab41
Provides: bundled(golang(golang.org/x/net/context/ctxhttp)) = %{version}-62685c2d7ca23c807425dca88b11a3e2323dab41
Provides: bundled(golang(golang.org/x/net/http2)) = %{version}-62685c2d7ca23c807425dca88b11a3e2323dab41
Provides: bundled(golang(golang.org/x/net/http2/hpack)) = %{version}-62685c2d7ca23c807425dca88b11a3e2323dab41
Provides: bundled(golang(golang.org/x/net/proxy)) = %{version}-62685c2d7ca23c807425dca88b11a3e2323dab41
Provides: bundled(golang(golang.org/x/oauth2)) = %{version}-b5adcc2dcdf009d0391547edc6ecbaff889f5bb9
Provides: bundled(golang(golang.org/x/oauth2/google)) = %{version}-b5adcc2dcdf009d0391547edc6ecbaff889f5bb9
Provides: bundled(golang(golang.org/x/oauth2/internal)) = %{version}-b5adcc2dcdf009d0391547edc6ecbaff889f5bb9
Provides: bundled(golang(golang.org/x/oauth2/jws)) = %{version}-b5adcc2dcdf009d0391547edc6ecbaff889f5bb9
Provides: bundled(golang(golang.org/x/oauth2/jwt)) = %{version}-b5adcc2dcdf009d0391547edc6ecbaff889f5bb9
Provides: bundled(golang(golang.org/x/sys/unix)) = %{version}-833a04a10549a95dc34458c195cbad61bbb6cb4d
Provides: bundled(golang(google.golang.org/cloud/compute/metadata)) = %{version}-eb47ba841d53d93506cfbfbc03927daf9cc48f88
Provides: bundled(golang(google.golang.org/cloud/internal)) = %{version}-eb47ba841d53d93506cfbfbc03927daf9cc48f88
Provides: bundled(golang(gopkg.in/inf.v0)) = %{version}-3887ee99ecf07df5b447e9b00d9c0b2adaa9f3e4
Provides: bundled(golang(gopkg.in/yaml.v2)) = %{version}-a83829b6f1293c91addabc89d0571c246397bbf4
Provides: bundled(golang(k8s.io/kubernetes/federation/apis/federation)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/federation/apis/federation/install)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/federation/apis/federation/v1beta1)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/federation/client/clientset_generated/federation_internalclientset)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/federation/client/clientset_generated/federation_internalclientset/typed/core/unversioned)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/federation/client/clientset_generated/federation_internalclientset/typed/federation/unversioned)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/api)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/annotations)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/endpoints)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/errors)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/install)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/meta)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/meta/metatypes)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/pod)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/resource)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/rest)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/service)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/unversioned)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/unversioned/validation)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/util)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/v1)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/validation)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/apimachinery)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/apimachinery/registered)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/apps)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/apps/install)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/apps/v1alpha1)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/authentication.k8s.io)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/authentication.k8s.io/install)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/authentication.k8s.io/v1beta1)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/authorization)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/authorization/install)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/authorization/v1beta1)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/autoscaling)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/autoscaling/install)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/autoscaling/v1)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/batch)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/batch/install)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/batch/v1)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/batch/v2alpha1)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/componentconfig)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/componentconfig/install)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/componentconfig/v1alpha1)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/extensions)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/extensions/install)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/extensions/v1beta1)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/extensions/validation)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/policy)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/policy/install)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/policy/v1alpha1)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/rbac)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/rbac/install)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/rbac/v1alpha1)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/auth/authenticator)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/auth/user)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/capabilities)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/cache)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/clientset_generated/internalclientset)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/clientset_generated/internalclientset/typed/autoscaling/unversioned)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/clientset_generated/internalclientset/typed/batch/unversioned)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/clientset_generated/internalclientset/typed/core/unversioned)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/clientset_generated/internalclientset/typed/extensions/unversioned)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/clientset_generated/internalclientset/typed/rbac/unversioned)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/metrics)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/record)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/restclient)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/transport)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/typed/discovery)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/unversioned)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/unversioned/adapters/internalclientset)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/unversioned/auth)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/unversioned/clientcmd)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/unversioned/clientcmd/api)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/unversioned/clientcmd/api/latest)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/unversioned/clientcmd/api/v1)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/controller)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/controller/framework)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/conversion)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/conversion/queryparams)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/credentialprovider)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/fieldpath)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/fields)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/kubectl)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/kubectl/cmd/util)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/kubectl/resource)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/kubelet/qos)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/kubelet/qos/util)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/labels)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/master/ports)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/registry/generic)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/registry/thirdpartyresourcedata)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/runtime)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/runtime/serializer)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/runtime/serializer/json)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/runtime/serializer/protobuf)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/runtime/serializer/recognizer)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/runtime/serializer/streaming)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/runtime/serializer/versioning)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/security/podsecuritypolicy/util)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/securitycontextconstraints/util)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/serviceaccount)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/storage)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/types)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/util)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/crypto)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/deployment)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/diff)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/errors)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/flag)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/flowcontrol)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/framer)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/hash)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/homedir)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/integer)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/intstr)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/json)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/jsonpath)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/labels)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/net)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/net/sets)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/parsers)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/pod)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/rand)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/replicaset)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/runtime)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/sets)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/slice)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/strategicpatch)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/validation)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/validation/field)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/wait)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/yaml)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/version)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/watch)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/pkg/watch/versioned)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/plugin/pkg/client/auth)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/plugin/pkg/client/auth/gcp)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/plugin/pkg/client/auth/oidc)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/third_party/forked/json)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/third_party/forked/reflect)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
Provides: bundled(golang(k8s.io/kubernetes/third_party/golang/template)) = %{version}-57fb9acc109285378ecd0af925c8160eb8ca19e6
%endif

%description
%{summary}

%if 0%{?with_devel}
%package devel
Summary:       %{summary}
BuildArch:     noarch

# devel subpackage BuildRequires
%if 0%{?with_check} && ! 0%{?with_bundled}
# These buildrequires are only for our tests (check)
BuildRequires: golang(github.com/Sirupsen/logrus)
BuildRequires: golang(github.com/docker/docker/api/client/bundlefile)
BuildRequires: golang(github.com/docker/libcompose/config)
BuildRequires: golang(github.com/docker/libcompose/lookup)
BuildRequires: golang(github.com/docker/libcompose/project)
BuildRequires: golang(github.com/fatih/structs)
BuildRequires: golang(github.com/ghodss/yaml)
BuildRequires: golang(github.com/openshift/origin/pkg/deploy/api)
BuildRequires: golang(github.com/openshift/origin/pkg/deploy/api/install)
BuildRequires: golang(github.com/urfave/cli)
BuildRequires: golang(k8s.io/kubernetes/pkg/api)
BuildRequires: golang(k8s.io/kubernetes/pkg/api/install)
BuildRequires: golang(k8s.io/kubernetes/pkg/api/unversioned)
BuildRequires: golang(k8s.io/kubernetes/pkg/apis/extensions)
BuildRequires: golang(k8s.io/kubernetes/pkg/apis/extensions/install)
BuildRequires: golang(k8s.io/kubernetes/pkg/client/unversioned)
BuildRequires: golang(k8s.io/kubernetes/pkg/kubectl)
BuildRequires: golang(k8s.io/kubernetes/pkg/kubectl/cmd/util)
BuildRequires: golang(k8s.io/kubernetes/pkg/runtime)
BuildRequires: golang(k8s.io/kubernetes/pkg/util/intstr)
%endif

# devel subpackage Requires. This is basically the source code from 
# all of the libraries that kompose imports during build.
Requires:      golang(github.com/Sirupsen/logrus)
Requires:      golang(github.com/docker/docker/api/client/bundlefile)
Requires:      golang(github.com/docker/libcompose/config)
Requires:      golang(github.com/docker/libcompose/lookup)
Requires:      golang(github.com/docker/libcompose/project)
Requires:      golang(github.com/fatih/structs)
Requires:      golang(github.com/ghodss/yaml)
Requires:      golang(github.com/openshift/origin/pkg/deploy/api)
Requires:      golang(github.com/openshift/origin/pkg/deploy/api/install)
Requires:      golang(github.com/urfave/cli)
Requires:      golang(k8s.io/kubernetes/pkg/api)
Requires:      golang(k8s.io/kubernetes/pkg/api/install)
Requires:      golang(k8s.io/kubernetes/pkg/api/unversioned)
Requires:      golang(k8s.io/kubernetes/pkg/apis/extensions)
Requires:      golang(k8s.io/kubernetes/pkg/apis/extensions/install)
Requires:      golang(k8s.io/kubernetes/pkg/client/unversioned)
Requires:      golang(k8s.io/kubernetes/pkg/kubectl)
Requires:      golang(k8s.io/kubernetes/pkg/kubectl/cmd/util)
Requires:      golang(k8s.io/kubernetes/pkg/runtime)
Requires:      golang(k8s.io/kubernetes/pkg/util/intstr)

# devel subpackage Provides
Provides:      golang(%{import_path}/cli/app) = %{version}-%{release}
Provides:      golang(%{import_path}/cli/command) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/kobject) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/loader) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/loader/bundle) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/loader/compose) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/transformer) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/transformer/kubernetes) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/transformer/openshift) = %{version}-%{release}
Provides:      golang(%{import_path}/version) = %{version}-%{release}

%description devel
%{summary}

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%package unit-test-devel
Summary:         Unit tests for %{name} package
%if 0%{?with_check}
#Here comes all BuildRequires: PACKAGE the unit tests
#in %%check section need for running
%endif

# test subpackage tests code from devel subpackage
Requires:        %{name}-devel = %{version}-%{release}

%if 0%{?with_check} && ! 0%{?with_bundled}
%endif


%description unit-test-devel
%{summary}

This package contains unit tests for project
providing packages with %{import_path} prefix.
%endif

%prep
%setup -q -n %{repo}-%{commit}
# Hack for now to get our docs to not be executable. This was fixed
# upstream in https://github.com/skippbox/kompose/pull/171 but this
# was after the 0.1.0 release
chmod 644 LICENSE CONTRIBUTING.md CHANGELOG.md RELEASE.md README.md code-of-conduct.md

%build
# set up temporary build gopath in pwd
mkdir -p src/%{provider}.%{provider_tld}/%{project}
ln -s ../../../ src/%{import_path}
export GOPATH=$(pwd):%{gopath}

export LDFLAGS=%{ldflags}
%gobuild %{buildflags} -o bin/kompose %{import_path}/cli/main


%install
install -d -p %{buildroot}%{_bindir}
install -p -m 0755 bin/kompose %{buildroot}%{_bindir}

# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . \( -iname "*.go" -or -iname "*.s" \) \! -iname "*_test.go" | grep -v "vendor") ; do
    dirprefix=$(dirname $file)
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$dirprefix
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list

    while [ "$dirprefix" != "." ]; do
        echo "%%dir %%{gopath}/src/%%{import_path}/$dirprefix" >> devel.file-list
        dirprefix=$(dirname $dirprefix)
    done
done
%endif

# testing files for this project
%if 0%{?with_unit_test} && 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test-devel.file-list
for file in $(find . -iname "*_test.go" | grep -v "vendor") ; do
    dirprefix=$(dirname $file)
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$dirprefix
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> unit-test-devel.file-list

    while [ "$dirprefix" != "." ]; do
        echo "%%dir %%{gopath}/src/%%{import_path}/$dirprefix" >> devel.file-list
        dirprefix=$(dirname $dirprefix)
    done
done
%endif

%if 0%{?with_devel}
sort -u -o devel.file-list devel.file-list
%endif

# check uses buildroot macro so that unit-tests can be run over the 
# files that are about to be installed with the rpm. 
%check
%if 0%{?with_check} && 0%{?with_unit_test} && 0%{?with_devel}
%if ! 0%{?with_bundled}
export GOPATH=%{buildroot}/%{gopath}:%{gopath}
%else
# Since we aren't packaging up the vendor directory we need to link 
# back to it somehow. Hack it up so that we can add the vendor
# directory from BUILD dir as a gopath to be searched when executing
# tests from the BUILDROOT dir.
ln -s ./ ./vendor/src # ./vendor/src -> ./vendor
export GOPATH=%{buildroot}/%{gopath}:$(pwd)/vendor:%{gopath}
%endif

%if ! 0%{?gotest:1}
%global gotest go test -ldflags "${LDFLAGS:-}"
%endif

export LDFLAGS=%{ldflags}
%gotest %{buildflags} %{testflags} %{import_path}/cli/app
%gotest %{buildflags} %{testflags} %{import_path}/pkg/transformer/kubernetes
%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license LICENSE
%doc CONTRIBUTING.md CHANGELOG.md RELEASE.md README.md code-of-conduct.md
%{_bindir}/kompose

%if 0%{?with_devel}
%files devel -f devel.file-list
%license LICENSE
%doc CONTRIBUTING.md CHANGELOG.md RELEASE.md README.md code-of-conduct.md
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%files unit-test-devel -f unit-test-devel.file-list
%license LICENSE
%doc CONTRIBUTING.md CHANGELOG.md RELEASE.md README.md code-of-conduct.md
%endif

%changelog
* Thu Sep 22 2016 dustymabe - 0.1.0-0.1.git8227684
- First package for Fedora
