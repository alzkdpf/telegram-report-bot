#!/usr/bin/env python

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'telbot',
        version = '1.0.5',
        description = 'telegram report bot',
        long_description = 'bot project',
        author = 'Michael LIM',
        author_email = 'code21032@gmail.com',
        license = 'MIT, LGPL-3, Apache-2.0',
        url = 'https://github.com/alzkdpf/telegram-report-bot',
        scripts = [],
        packages = ['telegram_service'],
        namespace_packages = [],
        py_modules = [],
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python'
        ],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = [
            'flask',
            'python-telegram-bot'
        ],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        keywords = '',
        python_requires = '',
        obsoletes = [],
    )
