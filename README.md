# X11Libre RPMs

This repository contains RPM build trees for XLibre, XLibre input/video drivers, and supporting dependency packages.

## Build XLibre xserver

Set `RELEASE_TAG` to the upstream XLibre release tag that matches the source archive you want to build.

~~~~ {.bash}
export RELEASE_TAG=25.1.6
cd xlibre-xserver/rpmbuild/SPECS

rpmbuild -bs \
    --define "_topdir $(cd .. && pwd)" \
    --define "dist .el<releasever>" \
    --define "upstream_version ${RELEASE_TAG}" \
    xlibre-xserver.spec

mock -r <mock-template> --rebuild ../SRPMS/xlibre-xserver-${RELEASE_TAG}-1.el<releasever>.src.rpm
~~~~

## Install XLibre

After publishing the rebuilt RPMs to your local repository, install the XLibre server and libinput driver:

~~~~ {.bash}
sudo dnf install xlibre-xserver xlibre-xf86-input-libinput
~~~~

Optional subpackages must be installed explicitly when needed:

~~~~ {.bash}
sudo dnf install \
    xlibre-xserver-Xvfb \
    xlibre-xserver-devel \
    xlibre-xserver-source
~~~~
