Name:           ocaml-findlib
Version:        1.7.3
Release:        7%{?dist}
Summary:        Objective CAML package manager and build helper
License:        BSD

URL:            http://projects.camlcity.org/projects/findlib.html
Source0:        http://download.camlcity.org/download/findlib-%{version}.tar.gz

# Use ocamlopt -g patch to include debug information.
Patch1:         findlib-1.4-add-debug.patch

BuildRequires:  ocaml >= 4.02.0
BuildRequires:  ocaml-camlp4-devel
#BuildRequires:  ocaml-labltk-devel
BuildRequires:  ocaml-ocamlbuild-devel
BuildRequires:  ocaml-compiler-libs
BuildRequires:  ocaml-ocamldoc
BuildRequires:  m4, ncurses-devel
BuildRequires:  gawk
Requires:       ocaml

%global __ocaml_requires_opts -i Asttypes -i Parsetree


%description
Objective CAML package manager and build helper.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n findlib-%{version}
%patch1 -p2


%build
ocamlc -version
ocamlc -where
(cd tools/extract_args && make)
tools/extract_args/extract_args -o src/findlib/ocaml_args.ml ocamlc ocamlcp ocamlmktop ocamlopt ocamldep ocamldoc ||:
cat src/findlib/ocaml_args.ml
./configure -config %{_sysconfdir}/ocamlfind.conf \
  -bindir %{_bindir} \
  -sitelib `ocamlc -where` \
  -mandir %{_mandir} \
  -with-toolbox
make all
%ifarch %{ocaml_native_compiler}
make opt
%endif
rm doc/guide-html/TIMESTAMP


%install
# Grrr destdir grrrr
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man{1,5}
make install \
     prefix=$RPM_BUILD_ROOT \
     OCAMLFIND_BIN=%{_bindir} \
     OCAMLFIND_MAN=%{_mandir}


%files
%doc LICENSE doc/README
%config(noreplace) %{_sysconfdir}/ocamlfind.conf
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_libdir}/ocaml/*/META
%{_libdir}/ocaml/topfind
%{_libdir}/ocaml/findlib
%ifarch %{ocaml_native_compiler}
%exclude %{_libdir}/ocaml/findlib/*.a
%exclude %{_libdir}/ocaml/findlib/*.cmxa
%endif
%exclude %{_libdir}/ocaml/findlib/*.mli
%exclude %{_libdir}/ocaml/findlib/Makefile.config
%exclude %{_libdir}/ocaml/findlib/make_wizard
%exclude %{_libdir}/ocaml/findlib/make_wizard.pattern
%{_libdir}/ocaml/num-top


%files devel
%doc LICENSE doc/README doc/guide-html
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/findlib/*.a
%{_libdir}/ocaml/findlib/*.cmxa
%endif
%{_libdir}/ocaml/findlib/*.mli
%{_libdir}/ocaml/findlib/Makefile.config


%changelog
* Thu Sep 28 2017 Richard W.M. Jones <rjones@redhat.com> - 1.7.3-7
- Rebuild with ocaml-camlp4.
  related: rhbz#1447988

* Fri Sep 22 2017 Richard W.M. Jones <rjones@redhat.com> - 1.7.3-6
- Remove BRs on ocaml-camlp4 and ocaml-labltk.
- Enable stripping and debuginfo on s390x.
- Use ocaml_native_compiler macro instead of opt test.
  related: rhbz#1447988

* Sat Sep 16 2017 Richard W.M. Jones <rjones@redhat.com> - 1.7.3-5
- Rebase to 1.7.3 (same as Fedora Rawhide).
  resolves: rhbz#1447988

* Tue Feb 07 2017 Richard W.M. Jones <rjones@redhat.com> - 1.3.3-7
- Fix a performance problem when ocamlfind links long command lines.
  resolves: rhbz#1403897

* Fri Aug 08 2014 Richard W.M. Jones <rjones@redhat.com> - 1.3.3-6
- Resolves: rhbz#1125627

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.3.3-5
- Mass rebuild 2013-12-27

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Richard W.M. Jones <rjones@redhat.com> - 1.3.3-3
- BR >= OCaml 4.00.1 so we can't build against the wrong OCaml version.

* Tue Oct 16 2012 Richard W.M. Jones <rjones@redhat.com> - 1.3.3-2
- Rebuild for OCaml 4.00.1.

* Sat Jul 28 2012 Richard W.M. Jones <rjones@redhat.com> - 1.3.3-1
- New upstream version 1.3.3.
- Remove patch for OCaml 4 which has been obsoleted by upstream changes.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-2
- Rebuild for OCaml 4.00.0.

* Thu Jun  7 2012 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-1
- New upstream version 1.3.1.
- This is required for programs using findlib and OCaml 4.00.0.
- Add small patch to fix build of topfind.

* Sat Apr 28 2012 Richard W.M. Jones <rjones@redhat.com> - 1.2.8-1
- New upstream version 1.2.8.

* Fri Jan  6 2012 Richard W.M. Jones <rjones@redhat.com> - 1.2.7-1
- New upstream version 1.2.7.

* Thu Dec  8 2011 Richard W.M. Jones <rjones@redhat.com> - 1.2.6-5
- Don't strip bytecode binary (see RHBZ#435559).

* Fri Jun 3 2011 Orion Poplawski - 1.2.6-3
- Add Requires: ocaml (Bug #710290)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan  5 2011 Richard W.M. Jones <rjones@redhat.com> - 1.2.6-1
- New upstream version 1.2.6.

* Tue Dec 29 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.5-4
- Rebuild for OCaml 3.11.2.

* Wed Dec 16 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.5-3
- Use __ocaml_requires_opts / __ocaml_provides_opts.

* Wed Dec 16 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.5-2
- Update to use RPM dependency generator.

* Sun Oct  4 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.5-1
- New upstream version 1.2.5.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 22 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.4-3
- Rebuild for OCaml 3.11.1.
- New upstream version 1.2.4.
- camlp4/META patch is now upstream.

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec  4 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-5
- Change to camlp4/META means that this package really depends on
  the latest OCaml compiler.

* Thu Dec  4 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-4
- camlp4/META: camlp4.lib should depend on dynlink.

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-3
- Rebuild for OCaml 3.11.0+rc1.

* Fri Nov 21 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-2
- Force rebuild.

* Thu Nov 20 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-1
- New upstream version 1.2.3.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.2-2
- Rebuild for OCaml 3.11.0

* Sun Aug 31 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.2-1
- New upstream version 1.2.2.
- Strip ocamlfind binary.
- Remove zero-length file.

* Mon Apr 21 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-3
- New upstream URLs.

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-2
- Experimental rebuild for ppc64.

* Tue Feb 12 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-1
- New upstream version 1.2.1.

* Thu Sep  6 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-14
- Ignore Parsetree module, it's a part of the toplevel.

* Mon Sep  3 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-13
- Bump version to force rebuild against ocaml -6 release.

* Thu Aug 30 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-12
- Added BR: gawk.

* Thu Aug 30 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-11
- Force rebuild because of changed BRs in base OCaml.

* Thu Aug  2 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-10
- BR added ocaml-ocamldoc so that ocamlfind ocamldoc works.
- Fix path of camlp4 parsers in Makefile.

* Thu Jul 12 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-9
- Added ExcludeArch: ppc64

* Thu Jul 12 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-8
- Expanded tabs to spaces.
- Readded conditional opt section for files.

* Wed Jul 04 2007 Xavier Lamien <lxtnow[at]gmail.com> - 1.1.2pl1-7
- Fixed BR.

* Wed Jun 27 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-6
- Fix configure line.
- Install doc/guide-html.
- Added dependency on ncurses-devel.

* Mon Jun 11 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-5
- Build against 3.10.
- Update to latest package guidelines.

* Sat Jun  2 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-4
- Handle bytecode-only architectures.

* Sat May 26 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-3
- Missing builddep m4.

* Fri May 25 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-2
- Use OCaml find-requires and find-provides.

* Fri May 18 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-1
- Initial RPM release.

