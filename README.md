This repository provides the prerequisites to build [Ungoogled Chromium](https://github.com/Eloston/ungoogled-chromium) on [COPR](https://copr.fedorainfracloud.org/) for Fedora. It uses the [Chromium](https://src.fedoraproject.org/rpms/chromium) package from the Fedora Project as its base.

To build your own ungoogled-chromium for e.g. Fedora 39:
1. Set up your COPR access as described in the [User Documentation](https://docs.pagure.org/copr.copr/user_documentation.html)
2. Run
    ```
    copr create ungoogled-chromium \
                --chroot fedora-39-x86_64
    ```
    to create your project.
3. Run
    ```
    copr add-package-custom ungoogled-chromium \
                            --name ungoogled-chromium \
                            --script-builddeps "git rpkg" \
                            --script copr_script.sh
    ```
    to add your package.
4. Run
    ```
    copr build-package ungoogled-chromium \
                       --timeout 108000 \
                       --name ungoogled-chromium
    ```
    to build your package.