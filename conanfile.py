import os
from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration


class AndroidCmdlineToolsConan(ConanFile):
    name = "android-cmdline-tools"
    version = "6858069"
    description = "Android command line tools"
    url = "https://github.com/joakimono/conan-android-cmdline-tools"
    homepage = "https://developer.android.com/studio/command-line/sdkmanager"
    topics = ("CLI", "android", "SDK", "tools")
    license = "Apache-2.0,GPL-2.0,MIT,LGPL-2.1"
    short_paths = True
    no_copy_source = True

    settings = {"os_build": ["Windows", "Linux", "Macos"],
                "arch_build": ["x86_64"]}

    options = {
        "platform_tools": [True, False],
        "emulator": [True, False],
        "extra_packages": "ANY"
    }

    default_options = ("platform_tools=True",
                       "emulator=True",
                       "extra_packages=")

    requires = (
        "java_installer/[>=8.0.0 <9]@bincrafters/stable",
        "android_ndk_installer/r21d@bincrafters/stable"
    )

    def configure(self):
        if self.settings.os_build == "Macos":
            raise ConanInvalidConfiguration("Recipe not implemented for Macos")
        pass

    @property
    def _extra_packages(self):
        return str(self.options.get_safe('extra_packages'))\
            .replace(";", "\;").split(',')

    @property
    def _packages(self):
        packages = []
        if self.options.platform_tools:
            packages.append('platform-tools')
        if self.options.emulator:
            packages.append('emulator')

        packages.extend(self._extra_packages)
        return packages

    def source(self):
        variant = self._platform
        archive_name = \
            "commandlinetools-{0}-{1}_latest.zip".format(variant,
                                                         self.version)
        source_url = "https://dl.google.com/android/repository/" + archive_name
        sha256 = {
            "win": "d2f6c9bb7db0362995c0b8dd2fd5949ce23c1dccb7f9392350b5e29b6d5fec7d",
            "mac": "58a55d9c5bcacd7c42170d2cf2c9ae2889c6797a6128307aaf69100636f54a13",
            "linux": "87f6dcf41d4e642e37ba03cb2e387a542aa0bd73cb689a9e7152aad40a6e7a08"}\
            .get(variant)

        tools.get(source_url, sha256=sha256,
                  destination="cmdline-tools", keep_permissions=True)

    @property
    def _platform(self):
        return {"Windows": "win",
                "Macos": "mac",
                "Linux": "linux"}.get(str(self.settings.os_build))

    def build(self):

        if self.settings.os_build == "Windows":
            suffix = ".bat"
            confirm = "yes | "
        else:
            suffix = ""
            confirm = "yes | "

        self.run(confirm + os.path.join(self.source_folder,
                                        "cmdline-tools",
                                        "cmdline-tools",
                                        "bin",
                                        "sdkmanager{} --licenses"
                                        .format(suffix)))

        base_cmd = os.path.join(self.source_folder,
                                "cmdline-tools",
                                "cmdline-tools",
                                "bin",
                                "sdkmanager{} --install ".format(suffix))

        for pack in self._packages:
            if pack != '':
                self.output.info(
                    "sdkmanager is installing package: {}".format(pack))
                cmd = '{}"\"{}\""'.format(base_cmd, pack)
                self.run(confirm + cmd)

    def package(self):
        self.copy(pattern="*", keep_path=True, symlinks=True)
        self.copy(pattern="*NOTICE.txt", src="tools", dst="licenses")

    def package_info(self):
        self.output.info("Creating ANDROID_SDK_ROOT environment variable: {}"
                         .format(self.package_folder))
        self.env_info.ANDROID_SDK_ROOT = self.package_folder
        self.env_info.PATH.append(os.path.join(
            self.package_folder, "cmdline-tools", "cmdline-tools", "bin"))
        self.env_info.PATH.append(os.path.join(
            self.package_folder, "emulator"))
        self.env_info.PATH.append(os.path.join(
            self.package_folder, "platform-tools"))

        self.output.info(
            "Remapping ANDROID_NDK_ROOT environment variable from android_ndk_installer: {}"
            .format(self.deps_env_info["android_ndk_installer"].ANDROID_NDK_HOME))
        self.env_info.ANDROID_NDK_ROOT = \
            self.deps_env_info["android_ndk_installer"].ANDROID_NDK_HOME

        excludes = [
            "add-ons", "extras", "platforms", "sources", "system-images"]

        for package in self._extra_packages:
            skip = False
            for exclude in excludes:
                if exclude in package:
                    skip = True

            if not skip:
                package_subdirs = package.split(";")
                self.env_info.PATH.append(os.path.join(
                    self.package_folder, *package_subdirs))

            # Probably need to hand-configure all packages paths to be added to environment
            # Are there subfolders in addition to be appended, e.g. 'bin'?
