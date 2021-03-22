# FYI:
# https://packaging.python.org/tutorials/packaging-projects/
# https://realpython.com/pypi-publish-python-package/

from setuptools import setup
gh_repo = 'https://github.com/weaming/cargo-vcs'

setup(
    name='cargo-vcs',  # Required
    version='2.3',  # Required
    description='Print the content of `.cargo_vcs_info.json` in the downloaded `.crate` file.',  # Required
    long_description=open('README.md').read().strip(),
    long_description_content_type="text/markdown",
    url=gh_repo,  # Optional
    author='weaming',  # Optional
    author_email='garden.yuen@gmail.com',  # Optional
    install_requires=['requests'],
    py_modules=['cargo_vcs'],
    entry_points={  # Optional
        'console_scripts': [
            'cargo-vcs=cargo_vcs:main',
        ],
    },
    keywords='cli,develop,cargo',  # Optional
    project_urls={  # Optional
        'Bug Reports': gh_repo,
        'Source': gh_repo,
    },
)
