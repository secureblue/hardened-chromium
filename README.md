# hardened-chromium

A hardened chromium for desktop Linux inspired by [Vanadium](https://github.com/GrapheneOS/Vanadium). Intended for use with [hardened_malloc](https://github.com/GrapheneOS/hardened_malloc) as packaged and provided by [secureblue](https://github.com/secureblue/secureblue).

## Scope

### In scope

* Desktop-relevant patches from Vanadium (located in vanadium_patches)
* Changes that increase hardening against known and unknown vulnerabilities 
* Changes that make secondary browser features opt-in instead of opt-out (for example, making the password manager and search suggestions opt-in)
* Changes that disable opt-in metrics and data collection, so long as they have no security implications

### Out of scope

* Any changes that sacrifice security for "privacy" (for example, enabling MV2)