<!-- omit in toc -->
# Contributing to hardened-chromium

First off, thanks for taking the time to contribute! ❤️

> If you like the project, but just don't have time to contribute, that's fine. There are other easy ways to support the project and show your appreciation, which we would also be very happy about:
> - Star the project
> - Tweet about it
> - Refer this project in your project's readme
> - Mention the project at local meetups and tell your friends/colleagues

<!-- omit in toc -->
## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [I Have a Question](#i-have-a-question)
- [I Want To Contribute](#i-want-to-contribute)
  - [Building locally](#your-first-code-contribution)
  - [Pull Requests](#💫-pull-requests)


## Code of Conduct

This project and everyone participating in it is governed by the
[Code of Conduct](https://github.com/secureblue/hardened-chromium/blob/master/CODE_OF_CONDUCT.md).
By participating, you are expected to uphold this code. Please report unacceptable behavior
to <secureblueadmin@proton.me>.


## I Have a Question

> If you want to ask a question, we assume that you have read the available [Documentation]().

Before you ask a question, it is best to search for existing [Issues](https://github.com/secureblue/hardened-chromium/issues) that might help you. In case you have found a suitable issue and still need clarification, you can write your question in this issue. It is also advisable to search the internet for answers first.

If you then still feel the need to ask a question and need clarification, we recommend the following:

- Open an [Issue](https://github.com/secureblue/hardened-chromium/issues/new).
- Provide as much context as you can about what you're running into.
- Provide project and platform versions (nodejs, npm, etc), depending on what seems relevant.

We will then take care of the issue as soon as possible.

## I Want To Contribute

> ### Legal Notice <!-- omit in toc -->
> When contributing to this project, you must agree that you have authored 100% of the content, that you have the necessary rights to the content and that the content you contribute may be provided under the project license.

### Building locally
#### Setup
Clone this repository:

`git clone --depth 1 --recurse-submodules https://github.com/secureblue/hardened-chromium.git && cd hardened-chromium`

Download chromium-%{version}-clean.tar.xz from the Fedora's server:

`rpkg --path ./chromium sources`

#### Harden
Copy the patches inside the source folder:

`cp vanadium_patches/* ./chromium && cp patches/* ./chromium`

Patch the spec file to build with the hardening patches:

`patch -d ./chromium -p1 < hardening.patch`

#### Build RPM
Build the patched chromium source from the spec file:

`rpmbuild -bs -v --define "_sourcedir $PWD/chromium" --define "_rpmdir $PWD/chromium" --define "_builddir $PWD/chromium" --define "_specdir $PWD/chromium" --define "_srcrpmdir $PWD" chromium/chromium.spec`

Rebuild the source for your system:

`mock --resultdir=dist -r %{distro}-%{version}-%{arch} --rebuild hardened-chromium-%{version}.%{distro}.src.rpm`

Install the built rpm...
### Pull Requests

#### Before Submitting a Pull Request

A good pull request should be ready for review before it is even created. For all pull requests, ensure:

- Your changes are in a single commit
- Your changes passes all the checks
- You have no unnecessary changes, including and especially whitespace changes
- You're code is covered.
- For substantive changes, you include evidence of proper functionality in the pull request in addition to the build results.