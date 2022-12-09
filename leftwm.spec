# Optimize for build time or performance
%bcond_without release_build

%global debug_package %{nil}

Name:           leftwm
Version:        0.4.0
Release:        1%{?dist}
Summary:        A tiling window manager for Adventurers

License:        MIT
URL:            http://leftwm.org/
Source0:        https://github.com/leftwm/leftwm/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cargo >= 1.59
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  rust >= 1.59

Recommends:     dmenu

%description
LeftWM is a tiling window manager written in Rust that aims to be stable and
performant. LeftWM is designed to do one thing and to do that one thing well:
be a window manager. LeftWM follows the following mantra:

  * LeftWM is not a compositor.
  * LeftWM is not a lock screen.
  * LeftWM is not a bar. But, there are lots of good bars out there. With
    themes, picking one is as simple as setting a symlink.

%prep
%autosetup
# curl https://sh.rustup.rs -sSf | sh -s -- \
#     --profile minimal \
#     --default-toolchain nightly -y


%build
%dnl export CARGO_HOME=$HOME/.cargo/
%dnl export PATH=$HOME/.cargo/bin/

%if %{with release_build}
%dnl $HOME/.cargo/bin/cargo build --release
cargo build --release
%else
%dnl $HOME/.cargo/bin/cargo build
cargo build
%endif


%install
install -Dpm 0644 %{name}.desktop -t %{buildroot}%{_datadir}/xsessions/
install -Dpm 0644 %{name}/doc/%{name}.1 -t %{buildroot}%{_mandir}/man1/

install -Dpm 0755 \
    target/release/%{name} \
    target/release/%{name}-check \
    target/release/%{name}-command \
    target/release/%{name}-state \
    target/release/%{name}-worker \
    target/release/lefthk-worker \
    -t %{buildroot}%{_bindir}

mkdir -p %{buildroot}%{_datadir}/%{name}
cp -a themes %{buildroot}%{_datadir}/%{name}/

strip --strip-all %{buildroot}%{_bindir}/*


%files
%license LICENSE.md
%doc README.md CHANGELOG
%{_bindir}/%{name}
%{_bindir}/%{name}-*
%{_datadir}/%{name}/
%{_datadir}/xsessions/%{name}.desktop
%{_mandir}/man1/*.1*


%changelog
* Fri Dec 9 2022 TH3 S4LM0N <TH3-S4LM0N@outlook.com> - 0.4.0-1
- New package