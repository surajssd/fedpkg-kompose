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
%global project         kubernetes-incubator
%global repo            kompose
# https://github.com/kubernetes-incubator/kompose
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          92ea0477f10facebfeb499d1ae7af6288763c4ec
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

# define ldflags, buildflags, testflags here. The ldflags/buildflags
# were taken from script/.build and the testflags were taken from
# script/test-unit. We will need to periodically check these for
# consistency.
%global ldflags "-w -X github.com/kubernetes-incubator/kompose/version.GITCOMMIT=%{shortcommit}"
%global buildflags %nil
%global testflags -cover -coverprofile=cover.out

Name:           kompose
Version:        0.1.2
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
# main.go
BuildRequires: golang(github.com/urfave/cli)

# Remaining dependencies not included in main packages
BuildRequires: golang(k8s.io/kubernetes/pkg/runtime)
BuildRequires: golang(github.com/ghodss/yaml)
BuildRequires: golang(github.com/Sirupsen/logrus)
BuildRequires: golang(github.com/openshift/origin/pkg/deploy/api)
BuildRequires: golang(github.com/openshift/origin/pkg/image/api)
BuildRequires: golang(k8s.io/kubernetes/pkg/api/resource)
BuildRequires: golang(github.com/openshift/origin/pkg/client)
BuildRequires: golang(k8s.io/kubernetes/pkg/client/unversioned/clientcmd)
BuildRequires: golang(k8s.io/kubernetes/pkg/api/install)
BuildRequires: golang(github.com/docker/libcompose/lookup)
BuildRequires: golang(k8s.io/kubernetes/pkg/kubectl/cmd/util)
BuildRequires: golang(github.com/docker/libcompose/project)
BuildRequires: golang(k8s.io/kubernetes/pkg/kubectl)
BuildRequires: golang(k8s.io/kubernetes/pkg/apis/extensions/install)
BuildRequires: golang(github.com/openshift/origin/pkg/deploy/api/install)
BuildRequires: golang(github.com/fatih/structs)
BuildRequires: golang(k8s.io/kubernetes/pkg/apis/extensions)
BuildRequires: golang(k8s.io/kubernetes/pkg/client/unversioned)
BuildRequires: golang(github.com/openshift/origin/pkg/image/api/install)
BuildRequires: golang(k8s.io/kubernetes/pkg/util/intstr)
BuildRequires: golang(k8s.io/kubernetes/pkg/api)
BuildRequires: golang(k8s.io/kubernetes/pkg/api/unversioned)
BuildRequires: golang(github.com/docker/libcompose/config)
BuildRequires: golang(github.com/openshift/origin/pkg/cmd/cli/config)
%endif

# Main package Provides
%if 0%{?with_bundled}
Provides: bundled(golang(bitbucket.org/ww/goautoneg)) = %{version}-75cd24fc2f2c2a2088577d12123ddee5f54e0675
Provides: bundled(golang(github.com/Azure/go-ansiterm)) = %{version}-fa152c58bc15761d0200cb75fe958b89a9d4888e
Provides: bundled(golang(github.com/Azure/go-ansiterm/winterm)) = %{version}-fa152c58bc15761d0200cb75fe958b89a9d4888e
Provides: bundled(golang(github.com/MakeNowJust/heredoc)) = %{version}-1d91351acdc1cb2f2c995864674b754134b86ca7
Provides: bundled(golang(github.com/Sirupsen/logrus)) = %{version}-4b6ea7319e214d98c938f12692336f7ca9348d6b
Provides: bundled(golang(github.com/beorn7/perks/quantile)) = %{version}-3ac7bf7a47d159a033b107610db8a1b6575507a4
Provides: bundled(golang(github.com/blang/semver)) = %{version}-31b736133b98f26d5e078ec9eb591666edfd091f
Provides: bundled(golang(github.com/coreos/etcd/auth/authpb)) = %{version}-9efa00d1030d4bf62eb8e5ec130023aeb1b8e2d0
Provides: bundled(golang(github.com/coreos/etcd/client)) = %{version}-9efa00d1030d4bf62eb8e5ec130023aeb1b8e2d0
Provides: bundled(golang(github.com/coreos/etcd/clientv3)) = %{version}-9efa00d1030d4bf62eb8e5ec130023aeb1b8e2d0
Provides: bundled(golang(github.com/coreos/etcd/etcdserver/api/v3rpc/rpctypes)) = %{version}-9efa00d1030d4bf62eb8e5ec130023aeb1b8e2d0
Provides: bundled(golang(github.com/coreos/etcd/etcdserver/etcdserverpb)) = %{version}-9efa00d1030d4bf62eb8e5ec130023aeb1b8e2d0
Provides: bundled(golang(github.com/coreos/etcd/mvcc/mvccpb)) = %{version}-9efa00d1030d4bf62eb8e5ec130023aeb1b8e2d0
Provides: bundled(golang(github.com/coreos/etcd/pkg/fileutil)) = %{version}-9efa00d1030d4bf62eb8e5ec130023aeb1b8e2d0
Provides: bundled(golang(github.com/coreos/etcd/pkg/pathutil)) = %{version}-9efa00d1030d4bf62eb8e5ec130023aeb1b8e2d0
Provides: bundled(golang(github.com/coreos/etcd/pkg/tlsutil)) = %{version}-9efa00d1030d4bf62eb8e5ec130023aeb1b8e2d0
Provides: bundled(golang(github.com/coreos/etcd/pkg/transport)) = %{version}-9efa00d1030d4bf62eb8e5ec130023aeb1b8e2d0
Provides: bundled(golang(github.com/coreos/etcd/pkg/types)) = %{version}-9efa00d1030d4bf62eb8e5ec130023aeb1b8e2d0
Provides: bundled(golang(github.com/coreos/go-oidc/http)) = %{version}-5cf2aa52da8c574d3aa4458f471ad6ae2240fe6b
Provides: bundled(golang(github.com/coreos/go-oidc/jose)) = %{version}-5cf2aa52da8c574d3aa4458f471ad6ae2240fe6b
Provides: bundled(golang(github.com/coreos/go-oidc/key)) = %{version}-5cf2aa52da8c574d3aa4458f471ad6ae2240fe6b
Provides: bundled(golang(github.com/coreos/go-oidc/oauth2)) = %{version}-5cf2aa52da8c574d3aa4458f471ad6ae2240fe6b
Provides: bundled(golang(github.com/coreos/go-oidc/oidc)) = %{version}-5cf2aa52da8c574d3aa4458f471ad6ae2240fe6b
Provides: bundled(golang(github.com/coreos/go-systemd/journal)) = %{version}-4484981625c1a6a2ecb40a390fcb6a9bcfee76e3
Provides: bundled(golang(github.com/coreos/pkg/capnslog)) = %{version}-fa29b1d70f0beaddd4c7021607cc3c3be8ce94b8
Provides: bundled(golang(github.com/coreos/pkg/health)) = %{version}-fa29b1d70f0beaddd4c7021607cc3c3be8ce94b8
Provides: bundled(golang(github.com/coreos/pkg/httputil)) = %{version}-fa29b1d70f0beaddd4c7021607cc3c3be8ce94b8
Provides: bundled(golang(github.com/coreos/pkg/timeutil)) = %{version}-fa29b1d70f0beaddd4c7021607cc3c3be8ce94b8
Provides: bundled(golang(github.com/davecgh/go-spew/spew)) = %{version}-5215b55f46b2b919f50a1df0eaa5886afe4e3b3d
Provides: bundled(golang(github.com/dgrijalva/jwt-go)) = %{version}-01aeca54ebda6e0fbfafd0a524d234159c05ec20
Provides: bundled(golang(github.com/docker/distribution)) = %{version}-1921dde3f1e52bf7dac07a0a2fcd55b770e134c5
Provides: bundled(golang(github.com/docker/distribution/context)) = %{version}-1921dde3f1e52bf7dac07a0a2fcd55b770e134c5
Provides: bundled(golang(github.com/docker/distribution/digest)) = %{version}-1921dde3f1e52bf7dac07a0a2fcd55b770e134c5
Provides: bundled(golang(github.com/docker/distribution/manifest)) = %{version}-1921dde3f1e52bf7dac07a0a2fcd55b770e134c5
Provides: bundled(golang(github.com/docker/distribution/manifest/schema1)) = %{version}-1921dde3f1e52bf7dac07a0a2fcd55b770e134c5
Provides: bundled(golang(github.com/docker/distribution/manifest/schema2)) = %{version}-1921dde3f1e52bf7dac07a0a2fcd55b770e134c5
Provides: bundled(golang(github.com/docker/distribution/reference)) = %{version}-1921dde3f1e52bf7dac07a0a2fcd55b770e134c5
Provides: bundled(golang(github.com/docker/distribution/uuid)) = %{version}-1921dde3f1e52bf7dac07a0a2fcd55b770e134c5
Provides: bundled(golang(github.com/docker/docker/api/types)) = %{version}-601004e1a714d77d3a43e957b8ae8adbc867b280
Provides: bundled(golang(github.com/docker/docker/api/types/blkiodev)) = %{version}-601004e1a714d77d3a43e957b8ae8adbc867b280
Provides: bundled(golang(github.com/docker/docker/api/types/container)) = %{version}-601004e1a714d77d3a43e957b8ae8adbc867b280
Provides: bundled(golang(github.com/docker/docker/api/types/filters)) = %{version}-601004e1a714d77d3a43e957b8ae8adbc867b280
Provides: bundled(golang(github.com/docker/docker/api/types/mount)) = %{version}-601004e1a714d77d3a43e957b8ae8adbc867b280
Provides: bundled(golang(github.com/docker/docker/api/types/network)) = %{version}-601004e1a714d77d3a43e957b8ae8adbc867b280
Provides: bundled(golang(github.com/docker/docker/api/types/registry)) = %{version}-601004e1a714d77d3a43e957b8ae8adbc867b280
Provides: bundled(golang(github.com/docker/docker/api/types/strslice)) = %{version}-601004e1a714d77d3a43e957b8ae8adbc867b280
Provides: bundled(golang(github.com/docker/docker/api/types/swarm)) = %{version}-601004e1a714d77d3a43e957b8ae8adbc867b280
Provides: bundled(golang(github.com/docker/docker/api/types/versions)) = %{version}-601004e1a714d77d3a43e957b8ae8adbc867b280
Provides: bundled(golang(github.com/docker/docker/cli/command/bundlefile)) = %{version}-601004e1a714d77d3a43e957b8ae8adbc867b280
Provides: bundled(golang(github.com/docker/docker/opts)) = %{version}-601004e1a714d77d3a43e957b8ae8adbc867b280
Provides: bundled(golang(github.com/docker/docker/pkg/mount)) = %{version}-601004e1a714d77d3a43e957b8ae8adbc867b280
Provides: bundled(golang(github.com/docker/docker/pkg/signal)) = %{version}-601004e1a714d77d3a43e957b8ae8adbc867b280
Provides: bundled(golang(github.com/docker/docker/pkg/system)) = %{version}-601004e1a714d77d3a43e957b8ae8adbc867b280
Provides: bundled(golang(github.com/docker/docker/pkg/term)) = %{version}-601004e1a714d77d3a43e957b8ae8adbc867b280
Provides: bundled(golang(github.com/docker/docker/pkg/term/windows)) = %{version}-601004e1a714d77d3a43e957b8ae8adbc867b280
Provides: bundled(golang(github.com/docker/docker/pkg/urlutil)) = %{version}-601004e1a714d77d3a43e957b8ae8adbc867b280
Provides: bundled(golang(github.com/docker/docker/runconfig/opts)) = %{version}-601004e1a714d77d3a43e957b8ae8adbc867b280
Provides: bundled(golang(github.com/docker/engine-api/types)) = %{version}-1d247454d4307fb1ddf10d09fd2996394b085904
Provides: bundled(golang(github.com/docker/engine-api/types/blkiodev)) = %{version}-1d247454d4307fb1ddf10d09fd2996394b085904
Provides: bundled(golang(github.com/docker/engine-api/types/container)) = %{version}-1d247454d4307fb1ddf10d09fd2996394b085904
Provides: bundled(golang(github.com/docker/engine-api/types/filters)) = %{version}-1d247454d4307fb1ddf10d09fd2996394b085904
Provides: bundled(golang(github.com/docker/engine-api/types/network)) = %{version}-1d247454d4307fb1ddf10d09fd2996394b085904
Provides: bundled(golang(github.com/docker/engine-api/types/registry)) = %{version}-1d247454d4307fb1ddf10d09fd2996394b085904
Provides: bundled(golang(github.com/docker/engine-api/types/strslice)) = %{version}-1d247454d4307fb1ddf10d09fd2996394b085904
Provides: bundled(golang(github.com/docker/engine-api/types/swarm)) = %{version}-1d247454d4307fb1ddf10d09fd2996394b085904
Provides: bundled(golang(github.com/docker/engine-api/types/versions)) = %{version}-1d247454d4307fb1ddf10d09fd2996394b085904
Provides: bundled(golang(github.com/docker/go-connections/nat)) = %{version}-f549a9393d05688dff0992ef3efd8bbe6c628aeb
Provides: bundled(golang(github.com/docker/go-units)) = %{version}-0bbddae09c5a5419a8c6dcdd7ff90da3d450393b
Provides: bundled(golang(github.com/docker/libcompose/config)) = %{version}-fbdac0a6a80837c63eb6c8f43514f7bb3f32df6c
Provides: bundled(golang(github.com/docker/libcompose/logger)) = %{version}-fbdac0a6a80837c63eb6c8f43514f7bb3f32df6c
Provides: bundled(golang(github.com/docker/libcompose/lookup)) = %{version}-fbdac0a6a80837c63eb6c8f43514f7bb3f32df6c
Provides: bundled(golang(github.com/docker/libcompose/project)) = %{version}-fbdac0a6a80837c63eb6c8f43514f7bb3f32df6c
Provides: bundled(golang(github.com/docker/libcompose/project/events)) = %{version}-fbdac0a6a80837c63eb6c8f43514f7bb3f32df6c
Provides: bundled(golang(github.com/docker/libcompose/project/options)) = %{version}-fbdac0a6a80837c63eb6c8f43514f7bb3f32df6c
Provides: bundled(golang(github.com/docker/libcompose/utils)) = %{version}-fbdac0a6a80837c63eb6c8f43514f7bb3f32df6c
Provides: bundled(golang(github.com/docker/libcompose/yaml)) = %{version}-fbdac0a6a80837c63eb6c8f43514f7bb3f32df6c
Provides: bundled(golang(github.com/docker/libtrust)) = %{version}-c54fbb67c1f1e68d7d6f8d2ad7c9360404616a41
Provides: bundled(golang(github.com/emicklei/go-restful)) = %{version}-89ef8af493ab468a45a42bb0d89a06fccdd2fb22
Provides: bundled(golang(github.com/emicklei/go-restful/log)) = %{version}-89ef8af493ab468a45a42bb0d89a06fccdd2fb22
Provides: bundled(golang(github.com/emicklei/go-restful/swagger)) = %{version}-89ef8af493ab468a45a42bb0d89a06fccdd2fb22
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
Provides: bundled(golang(github.com/gogo/protobuf/proto)) = %{version}-e18d7aa8f8c624c915db340349aad4c49b10d173
Provides: bundled(golang(github.com/gogo/protobuf/sortkeys)) = %{version}-e18d7aa8f8c624c915db340349aad4c49b10d173
Provides: bundled(golang(github.com/golang/glog)) = %{version}-335da9dda11408a34b64344f82e9c03779b71673
Provides: bundled(golang(github.com/golang/groupcache/lru)) = %{version}-604ed5785183e59ae2789449d89e73f3a2a77987
Provides: bundled(golang(github.com/golang/protobuf/jsonpb)) = %{version}-8616e8ee5e20a1704615e6c8d7afcdac06087a67
Provides: bundled(golang(github.com/golang/protobuf/proto)) = %{version}-8616e8ee5e20a1704615e6c8d7afcdac06087a67
Provides: bundled(golang(github.com/gonum/blas)) = %{version}-80dca99229cccca259b550ae3f755cf79c65a224
Provides: bundled(golang(github.com/gonum/blas/blas64)) = %{version}-80dca99229cccca259b550ae3f755cf79c65a224
Provides: bundled(golang(github.com/gonum/blas/native)) = %{version}-80dca99229cccca259b550ae3f755cf79c65a224
Provides: bundled(golang(github.com/gonum/blas/native/internal/math32)) = %{version}-80dca99229cccca259b550ae3f755cf79c65a224
Provides: bundled(golang(github.com/gonum/graph)) = %{version}-bde6d0fbd9dec5a997e906611fe0364001364c41
Provides: bundled(golang(github.com/gonum/graph/concrete)) = %{version}-bde6d0fbd9dec5a997e906611fe0364001364c41
Provides: bundled(golang(github.com/gonum/graph/encoding/dot)) = %{version}-bde6d0fbd9dec5a997e906611fe0364001364c41
Provides: bundled(golang(github.com/gonum/graph/internal)) = %{version}-bde6d0fbd9dec5a997e906611fe0364001364c41
Provides: bundled(golang(github.com/gonum/graph/path)) = %{version}-bde6d0fbd9dec5a997e906611fe0364001364c41
Provides: bundled(golang(github.com/gonum/graph/topo)) = %{version}-bde6d0fbd9dec5a997e906611fe0364001364c41
Provides: bundled(golang(github.com/gonum/graph/traverse)) = %{version}-bde6d0fbd9dec5a997e906611fe0364001364c41
Provides: bundled(golang(github.com/gonum/internal/asm)) = %{version}-5b84ddfb9d3e72d73b8de858c97650be140935c0
Provides: bundled(golang(github.com/gonum/lapack)) = %{version}-88ec467285859a6cd23900147d250a8af1f38b10
Provides: bundled(golang(github.com/gonum/lapack/lapack64)) = %{version}-88ec467285859a6cd23900147d250a8af1f38b10
Provides: bundled(golang(github.com/gonum/lapack/native)) = %{version}-88ec467285859a6cd23900147d250a8af1f38b10
Provides: bundled(golang(github.com/gonum/matrix/mat64)) = %{version}-fb1396264e2e259ff714a408a7b0142d238b198d
Provides: bundled(golang(github.com/google/cadvisor/info/v1)) = %{version}-d84e0758ab16ee68598702793119c9a7370c1522
Provides: bundled(golang(github.com/google/gofuzz)) = %{version}-bbcb9da2d746f8bdbd6a936686a0a6067ada0ec5
Provides: bundled(golang(github.com/gorilla/context)) = %{version}-215affda49addc4c8ef7e2534915df2c8c35c6cd
Provides: bundled(golang(github.com/gorilla/mux)) = %{version}-8096f47503459bcc74d1f4c487b7e6e42e5746b5
Provides: bundled(golang(github.com/grpc-ecosystem/grpc-gateway/runtime)) = %{version}-f52d055dc48aec25854ed7d31862f78913cf17d1
Provides: bundled(golang(github.com/grpc-ecosystem/grpc-gateway/runtime/internal)) = %{version}-f52d055dc48aec25854ed7d31862f78913cf17d1
Provides: bundled(golang(github.com/grpc-ecosystem/grpc-gateway/utilities)) = %{version}-f52d055dc48aec25854ed7d31862f78913cf17d1
Provides: bundled(golang(github.com/imdario/mergo)) = %{version}-6633656539c1639d9d78127b7d47c622b5d7b6dc
Provides: bundled(golang(github.com/inconshreveable/mousetrap)) = %{version}-76626ae9c91c4f2a10f34cad8ce83ea42c93bb75
Provides: bundled(golang(github.com/jonboulle/clockwork)) = %{version}-3f831b65b61282ba6bece21b91beea2edc4c887a
Provides: bundled(golang(github.com/juju/ratelimit)) = %{version}-77ed1c8a01217656d2080ad51981f6e99adaa177
Provides: bundled(golang(github.com/matttproud/golang_protobuf_extensions/pbutil)) = %{version}-fc2b8d3a73c4867e51861bbdd5ae3c1f0869dd6a
Provides: bundled(golang(github.com/openshift/origin/pkg/api)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/api/extension)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/api/graph)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/api/graph/graphview)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/api/kubegraph)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/api/kubegraph/analysis)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/api/kubegraph/nodes)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/api/latest)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/api/restmapper)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/auth/api)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/auth/authenticator)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/auth/authenticator/request/x509request)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/authorization/api)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/authorization/reaper)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/build/api)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/build/client)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/build/cmd)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/build/graph)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/build/graph/analysis)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/build/graph/nodes)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/build/util)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/client)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/cmd/cli/config)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/cmd/cli/describe)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/cmd/flagtypes)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/cmd/util)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/cmd/util/clientcmd)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/deploy/api)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/deploy/api/install)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/deploy/api/v1)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/deploy/cmd)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/deploy/graph)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/deploy/graph/analysis)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/deploy/graph/nodes)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/deploy/util)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/image/api)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/image/api/docker10)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/image/api/dockerpre012)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/image/api/install)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/image/api/v1)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/image/graph)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/image/graph/nodes)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/oauth/api)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/project/api)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/quota/api)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/quota/util)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/route/api)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/route/generator)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/route/graph)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/route/graph/analysis)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/route/graph/nodes)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/sdn/api)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/security/api)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/template/api)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/user/api)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/user/reaper)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/util)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/util/dot)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/util/errors)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/util/namer)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/util/parallel)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/openshift/origin/pkg/version)) = %{version}-67479ffd447d68d20e556746d56eb80458b9294c
Provides: bundled(golang(github.com/pborman/uuid)) = %{version}-ca53cad383cad2479bbba7f7a1a05797ec1386e4
Provides: bundled(golang(github.com/prometheus/client_golang/prometheus)) = %{version}-e51041b3fa41cece0dca035740ba6411905be473
Provides: bundled(golang(github.com/prometheus/client_model/go)) = %{version}-fa8ad6fec33561be4280a8f0514318c79d7f6cb6
Provides: bundled(golang(github.com/prometheus/common/expfmt)) = %{version}-a6ab08426bb262e2d190097751f5cfd1cfdfd17d
Provides: bundled(golang(github.com/prometheus/common/internal/bitbucket.org/ww/goautoneg)) = %{version}-a6ab08426bb262e2d190097751f5cfd1cfdfd17d
Provides: bundled(golang(github.com/prometheus/common/model)) = %{version}-a6ab08426bb262e2d190097751f5cfd1cfdfd17d
Provides: bundled(golang(github.com/prometheus/procfs)) = %{version}-454a56f35412459b5e684fd5ec0f9211b94f002a
Provides: bundled(golang(github.com/spf13/cobra)) = %{version}-7c674d9e72017ed25f6d2b5e497a1368086b6a6f
Provides: bundled(golang(github.com/spf13/pflag)) = %{version}-1560c1005499d61b80f865c04d39ca7505bf7f0b
Provides: bundled(golang(github.com/ugorji/go/codec)) = %{version}-f4485b318aadd133842532f841dc205a8e339d74
Provides: bundled(golang(github.com/urfave/cli)) = %{version}-71f57d300dd6a780ac1856c005c4b518cfd498ec
Provides: bundled(golang(github.com/xeipuuv/gojsonpointer)) = %{version}-e0fe6f68307607d540ed8eac07a342c33fa1b54a
Provides: bundled(golang(github.com/xeipuuv/gojsonreference)) = %{version}-e02fc20de94c78484cd5ffb007f8af96be030a45
Provides: bundled(golang(github.com/xeipuuv/gojsonschema)) = %{version}-ac452913faa25c08bb78810d3e6f88b8a39f8f25
Provides: bundled(golang(golang.org/x/net/context)) = %{version}-e90d6d0afc4c315a0d87a568ae68577cc15149a0
Provides: bundled(golang(golang.org/x/net/context/ctxhttp)) = %{version}-e90d6d0afc4c315a0d87a568ae68577cc15149a0
Provides: bundled(golang(golang.org/x/net/http2)) = %{version}-e90d6d0afc4c315a0d87a568ae68577cc15149a0
Provides: bundled(golang(golang.org/x/net/http2/hpack)) = %{version}-e90d6d0afc4c315a0d87a568ae68577cc15149a0
Provides: bundled(golang(golang.org/x/net/internal/timeseries)) = %{version}-e90d6d0afc4c315a0d87a568ae68577cc15149a0
Provides: bundled(golang(golang.org/x/net/lex/httplex)) = %{version}-e90d6d0afc4c315a0d87a568ae68577cc15149a0
Provides: bundled(golang(golang.org/x/net/trace)) = %{version}-e90d6d0afc4c315a0d87a568ae68577cc15149a0
Provides: bundled(golang(golang.org/x/oauth2)) = %{version}-b5adcc2dcdf009d0391547edc6ecbaff889f5bb9
Provides: bundled(golang(golang.org/x/oauth2/google)) = %{version}-b5adcc2dcdf009d0391547edc6ecbaff889f5bb9
Provides: bundled(golang(golang.org/x/oauth2/internal)) = %{version}-b5adcc2dcdf009d0391547edc6ecbaff889f5bb9
Provides: bundled(golang(golang.org/x/oauth2/jws)) = %{version}-b5adcc2dcdf009d0391547edc6ecbaff889f5bb9
Provides: bundled(golang(golang.org/x/oauth2/jwt)) = %{version}-b5adcc2dcdf009d0391547edc6ecbaff889f5bb9
Provides: bundled(golang(golang.org/x/sys/unix)) = %{version}-833a04a10549a95dc34458c195cbad61bbb6cb4d
Provides: bundled(golang(google.golang.org/cloud/compute/metadata)) = %{version}-eb47ba841d53d93506cfbfbc03927daf9cc48f88
Provides: bundled(golang(google.golang.org/cloud/internal)) = %{version}-eb47ba841d53d93506cfbfbc03927daf9cc48f88
Provides: bundled(golang(google.golang.org/grpc)) = %{version}-231b4cfea0e79843053a33f5fe90bd4d84b23cd3
Provides: bundled(golang(google.golang.org/grpc/codes)) = %{version}-231b4cfea0e79843053a33f5fe90bd4d84b23cd3
Provides: bundled(golang(google.golang.org/grpc/credentials)) = %{version}-231b4cfea0e79843053a33f5fe90bd4d84b23cd3
Provides: bundled(golang(google.golang.org/grpc/grpclog)) = %{version}-231b4cfea0e79843053a33f5fe90bd4d84b23cd3
Provides: bundled(golang(google.golang.org/grpc/internal)) = %{version}-231b4cfea0e79843053a33f5fe90bd4d84b23cd3
Provides: bundled(golang(google.golang.org/grpc/metadata)) = %{version}-231b4cfea0e79843053a33f5fe90bd4d84b23cd3
Provides: bundled(golang(google.golang.org/grpc/naming)) = %{version}-231b4cfea0e79843053a33f5fe90bd4d84b23cd3
Provides: bundled(golang(google.golang.org/grpc/peer)) = %{version}-231b4cfea0e79843053a33f5fe90bd4d84b23cd3
Provides: bundled(golang(google.golang.org/grpc/transport)) = %{version}-231b4cfea0e79843053a33f5fe90bd4d84b23cd3
Provides: bundled(golang(gopkg.in/inf.v0)) = %{version}-3887ee99ecf07df5b447e9b00d9c0b2adaa9f3e4
Provides: bundled(golang(gopkg.in/yaml.v2)) = %{version}-a83829b6f1293c91addabc89d0571c246397bbf4
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/api)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/api/endpoints)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/api/errors)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/api/meta)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/api/meta/metatypes)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/api/pod)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/api/resource)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/api/service)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/api/unversioned)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/api/unversioned/validation)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/api/util)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/api/v1)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/api/validation)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apimachinery)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apimachinery/registered)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/autoscaling)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/batch)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/extensions)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/auth/user)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/capabilities)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/conversion)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/conversion/queryparams)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/fields)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/labels)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/runtime)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/runtime/serializer)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/runtime/serializer/json)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/runtime/serializer/protobuf)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/runtime/serializer/recognizer)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/runtime/serializer/streaming)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/runtime/serializer/versioning)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/security/apparmor)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/selection)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/third_party/forked/golang/reflect)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/types)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/clock)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/config)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/crypto)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/errors)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/flowcontrol)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/framer)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/hash)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/integer)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/intstr)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/json)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/labels)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/net)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/net/sets)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/parsers)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/rand)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/runtime)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/sets)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/uuid)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/validation)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/validation/field)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/wait)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/yaml)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/version)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/watch)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/watch/versioned)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/rest)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/tools/clientcmd/api)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/tools/metrics)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/client-go/1.4/transport)) = %{version}-f8e519fcc08881bcfe82d8755046df62ea30fda0
Provides: bundled(golang(k8s.io/kubernetes/federation/apis/federation)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/federation/apis/federation/install)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/federation/apis/federation/v1beta1)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/federation/client/clientset_generated/federation_internalclientset)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/federation/client/clientset_generated/federation_internalclientset/typed/core/unversioned)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/federation/client/clientset_generated/federation_internalclientset/typed/extensions/unversioned)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/federation/client/clientset_generated/federation_internalclientset/typed/federation/unversioned)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/api)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/annotations)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/endpoints)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/errors)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/install)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/meta)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/meta/metatypes)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/pod)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/resource)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/rest)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/service)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/unversioned)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/unversioned/validation)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/util)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/v1)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/validation)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/apimachinery)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/apimachinery/registered)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/apps)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/apps/install)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/apps/v1alpha1)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/authentication)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/authentication/install)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/authentication/v1beta1)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/authorization)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/authorization/install)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/authorization/v1beta1)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/autoscaling)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/autoscaling/install)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/autoscaling/v1)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/batch)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/batch/install)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/batch/v1)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/batch/v2alpha1)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/certificates)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/certificates/install)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/certificates/v1alpha1)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/componentconfig)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/componentconfig/install)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/componentconfig/v1alpha1)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/extensions)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/extensions/install)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/extensions/v1beta1)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/extensions/validation)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/policy)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/policy/install)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/policy/v1alpha1)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/rbac)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/rbac/install)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/rbac/v1alpha1)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/storage)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/storage/install)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/storage/v1beta1)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/auth/authenticator)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/auth/user)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/capabilities)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/cache)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/clientset_generated/internalclientset)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/clientset_generated/internalclientset/typed/authentication/unversioned)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/clientset_generated/internalclientset/typed/authorization/unversioned)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/clientset_generated/internalclientset/typed/autoscaling/unversioned)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/clientset_generated/internalclientset/typed/batch/unversioned)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/clientset_generated/internalclientset/typed/certificates/unversioned)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/clientset_generated/internalclientset/typed/core/unversioned)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/clientset_generated/internalclientset/typed/extensions/unversioned)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/clientset_generated/internalclientset/typed/rbac/unversioned)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/clientset_generated/internalclientset/typed/storage/unversioned)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/metrics)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/record)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/restclient)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/transport)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/typed/discovery)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/typed/dynamic)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/unversioned)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/unversioned/adapters/internalclientset)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/unversioned/auth)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/unversioned/clientcmd)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/unversioned/clientcmd/api)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/unversioned/clientcmd/api/latest)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/unversioned/clientcmd/api/v1)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/controller)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/controller/deployment/util)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/controller/framework)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/controller/framework/informers)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/controller/replication)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/conversion)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/conversion/queryparams)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/credentialprovider)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/fieldpath)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/fields)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/kubectl)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/kubectl/cmd/util)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/kubectl/resource)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/kubelet/qos)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/kubelet/types)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/labels)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/master/ports)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/registry/generic)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/registry/thirdpartyresourcedata)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/runtime)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/runtime/serializer)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/runtime/serializer/json)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/runtime/serializer/protobuf)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/runtime/serializer/recognizer)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/runtime/serializer/streaming)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/runtime/serializer/versioning)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/security/apparmor)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/security/podsecuritypolicy/util)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/securitycontextconstraints/util)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/selection)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/serviceaccount)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/storage)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/storage/etcd)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/storage/etcd/metrics)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/storage/etcd/util)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/storage/etcd3)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/storage/storagebackend)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/storage/storagebackend/factory)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/types)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/cache)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/certificates)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/clock)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/config)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/crypto)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/diff)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/errors)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/exec)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/flag)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/flowcontrol)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/framer)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/hash)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/homedir)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/integer)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/interrupt)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/intstr)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/json)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/jsonpath)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/labels)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/metrics)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/net)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/net/sets)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/parsers)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/pod)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/rand)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/replicaset)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/runtime)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/sets)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/slice)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/strategicpatch)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/term)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/uuid)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/validation)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/validation/field)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/wait)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/workqueue)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/yaml)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/version)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/watch)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/pkg/watch/versioned)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/plugin/pkg/client/auth)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/plugin/pkg/client/auth/gcp)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/plugin/pkg/client/auth/oidc)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/third_party/forked/golang/json)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/third_party/forked/golang/netutil)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/third_party/forked/golang/reflect)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
Provides: bundled(golang(k8s.io/kubernetes/third_party/forked/golang/template)) = %{version}-d19513fe86f3e0769dd5c4674c093a88a5adb8b4
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
BuildRequires: golang(github.com/docker/libcompose/config)
BuildRequires: golang(github.com/docker/libcompose/lookup)
BuildRequires: golang(github.com/docker/libcompose/project)
BuildRequires: golang(github.com/fatih/structs)
BuildRequires: golang(github.com/ghodss/yaml)
BuildRequires: golang(github.com/openshift/origin/pkg/client)
BuildRequires: golang(github.com/openshift/origin/pkg/cmd/cli/config)
BuildRequires: golang(github.com/openshift/origin/pkg/deploy/api)
BuildRequires: golang(github.com/openshift/origin/pkg/deploy/api/install)
BuildRequires: golang(github.com/openshift/origin/pkg/image/api)
BuildRequires: golang(github.com/openshift/origin/pkg/image/api/install)
BuildRequires: golang(github.com/urfave/cli)
BuildRequires: golang(k8s.io/kubernetes/pkg/api)
BuildRequires: golang(k8s.io/kubernetes/pkg/api/install)
BuildRequires: golang(k8s.io/kubernetes/pkg/api/resource)
BuildRequires: golang(k8s.io/kubernetes/pkg/api/unversioned)
BuildRequires: golang(k8s.io/kubernetes/pkg/apis/extensions)
BuildRequires: golang(k8s.io/kubernetes/pkg/apis/extensions/install)
BuildRequires: golang(k8s.io/kubernetes/pkg/client/unversioned)
BuildRequires: golang(k8s.io/kubernetes/pkg/client/unversioned/clientcmd)
BuildRequires: golang(k8s.io/kubernetes/pkg/kubectl)
BuildRequires: golang(k8s.io/kubernetes/pkg/kubectl/cmd/util)
BuildRequires: golang(k8s.io/kubernetes/pkg/runtime)
BuildRequires: golang(k8s.io/kubernetes/pkg/util/intstr)
%endif

# devel subpackage Requires. This is basically the source code from 
# all of the libraries that kompose imports during build.
Requires:      golang(github.com/Sirupsen/logrus)
Requires:      golang(github.com/docker/libcompose/config)
Requires:      golang(github.com/docker/libcompose/lookup)
Requires:      golang(github.com/docker/libcompose/project)
Requires:      golang(github.com/fatih/structs)
Requires:      golang(github.com/ghodss/yaml)
Requires:      golang(github.com/openshift/origin/pkg/client)
Requires:      golang(github.com/openshift/origin/pkg/cmd/cli/config)
Requires:      golang(github.com/openshift/origin/pkg/deploy/api)
Requires:      golang(github.com/openshift/origin/pkg/deploy/api/install)
Requires:      golang(github.com/openshift/origin/pkg/image/api)
Requires:      golang(github.com/openshift/origin/pkg/image/api/install)
Requires:      golang(github.com/urfave/cli)
Requires:      golang(k8s.io/kubernetes/pkg/api)
Requires:      golang(k8s.io/kubernetes/pkg/api/install)
Requires:      golang(k8s.io/kubernetes/pkg/api/resource)
Requires:      golang(k8s.io/kubernetes/pkg/api/unversioned)
Requires:      golang(k8s.io/kubernetes/pkg/apis/extensions)
Requires:      golang(k8s.io/kubernetes/pkg/apis/extensions/install)
Requires:      golang(k8s.io/kubernetes/pkg/client/unversioned)
Requires:      golang(k8s.io/kubernetes/pkg/client/unversioned/clientcmd)
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

%build
# set up temporary build gopath in pwd
mkdir -p src/%{provider}.%{provider_tld}/%{project}
ln -s ../../../ src/%{import_path}
%if ! 0%{?with_bundled}
export GOPATH=$(pwd):%{gopath}
%else
# No dependency directories so far
export GOPATH=$(pwd):%{gopath}
%endif

export LDFLAGS=%{ldflags}
%gobuild %{buildflags} -o bin/kompose %{import_path}/

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
%doc CHANGELOG.md CONTRIBUTING.md code-of-conduct.md README.md RELEASE.md
%{_bindir}/kompose

%if 0%{?with_devel}
%files devel -f devel.file-list
%license LICENSE
%doc CHANGELOG.md CONTRIBUTING.md code-of-conduct.md README.md RELEASE.md
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%files unit-test-devel -f unit-test-devel.file-list
%license LICENSE
%doc CHANGELOG.md CONTRIBUTING.md code-of-conduct.md README.md RELEASE.md
%endif

%changelog
* Sat Nov 26 2016 Dusty Mabe <dusty@dustymabe.com> - 0.1.2-0.1.git92ea047
- Update to kompose version 0.1.2

* Thu Sep 22 2016 dustymabe - 0.1.0-0.1.git8227684
- First package for Fedora
