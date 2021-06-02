[![Linux install](https://github.com/joakimono/conan-android-cmdline-tools/workflows/Linux%20install/badge.svg)](https://github.com/joakimono/conan-android-cmdline-tools/actions?query=workflow%3A"Linux+install")
[![Windows install](https://github.com/joakimono/conan-android-cmdline-tools/workflows/Windows%20install/badge.svg)](https://github.com/joakimono/conan-android-cmdline-tools/actions?query=workflow%3A"Windows+install")

[Conan.io](https://conan.io) recipe for [android cmdline tools](https://developer.android.com/studio/command-line/sdkmanager).

The recipe generates library packages, which can be found at [Bintray](https://bintray.com/joakimono/conan/android-cmdline-tools%3Ajoakimono).
The package is usually consumed using the `conan install` command or a *conanfile.txt*.

## How to use this package

1. Add remote to conan's package [remotes](https://docs.conan.io/en/latest/reference/commands/misc/remote.html?highlight=remotes):

   ```bash
   $ conan remote add sintef https://artifactory.smd.sintef.no/artifactory/api/conan/conan-local
   $ conan remote add bincrafters https://bincrafters.jfrog.io/artifactory/api/conan/public-conan
   $ conan config set general.revisions_enabled=1
   ```

2. Using *conanfile.txt* in your project with *cmake*

   Add a [*conanfile.txt*](http://docs.conan.io/en/latest/reference/conanfile_txt.html) to your project. This file describes dependencies and your configuration of choice, e.g.:

   ```
   [build_requires]
   android-cmdline-tools/[>=6858069]@joakimono/testing # or stable?

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
