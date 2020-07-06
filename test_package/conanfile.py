#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile


class AndroidCmdlineToolsTestConan(ConanFile):
    settings = "os_build"

    def build(self):
        pass

    def test(self):

        suffix = ".bat" if self.settings.os_build == "Windows" else ""
        self.run("sdkmanager{} --list".format(suffix),
                 run_environment=True)
