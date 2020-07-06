[![Linux install](https://github.com/joakimono/conan-android-cmdline-tools/workflows/Linux%20install/badge.svg)](https://github.com/joakimono/conan-android-cmdline-tools/actions?query=workflow%3A"Linux+install")
[![Windows install](https://github.com/joakimono/conan-android-cmdline-tools/workflows/Windows%20install/badge.svg)](https://github.com/joakimono/conan-android-cmdline-tools/actions?query=workflow%3A"Windows+install")
[![Download](https://api.bintray.com/packages/joakimono/conan/android-cmdline-tools%3Ajoakimono/images/download.svg)](https://bintray.com/sintef-ocean/conan/qwt%3Asintef/_latestVersion)


[Conan.io](https://conan.io) recipe for [android cmdline tools](https://developer.android.com/studio/command-line/sdkmanager).

The recipe generates library packages, which can be found at [Bintray](https://bintray.com/joakimono/conan/android-cmdline-tools%3Ajoakimon).
The package is usually consumed using the `conan install` command or a *conanfile.txt*.

## How to use this package

1. Add remote to conan's package [registry.txt](http://docs.conan.io/en/latest/reference/config_files/registry.txt.html):

   ```bash
   $ conan remote add kimono https://api.bintray.com/conan/joakimono/conan
   $ conan remote add bincrafters https://api.bintray.com/conan/bincrafters/public-conan
   ```

2. Using *conanfile.txt* in your project with *cmake*

   Add a [*conanfile.txt*](http://docs.conan.io/en/latest/reference/conanfile_txt.html) to your project. This file describes dependencies and your configuration of choice, e.g.:

   ```
   [build_requires]
   android-cmdline-tools/[>=6609375]@joakimono/stable

   [options]
   android-cmdline-tools:extra_packages=system-images;android-30;google_apis;x86_64,platforms;android-30

   [imports]
   licenses, * -> ./licenses @ folder=True

   [generators]
   virtualenv
   ```

   ```bash
   $ mkdir build && cd build
   $ conan install .. --profile=android -s os=Android
   $ source activate.sh
   $ sdkmanager --list
   ```
   The environment gives you access to android command line tools, android ndk and java compiler version 8. For details on how to use the command line tools, please consult [Android Command line tools](https://developer.android.com/studio/command-line)

## Package options

Option | Default | Domain
---|---|---
platform_tools | True | [True, False]
emulator | True | [True, False]
extra_packages |  | ANY

## Known recipe issues
