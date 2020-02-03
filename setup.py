from setuptools import setup


def readme():
    with open('README.md', 'r') as fp:
        return fp.read()


def requirements():
    with open('requirements.txt', 'r') as fp:
        return fp.read().split()


setup(
    author='Andrew Poltavchenko',
    author_email='pa@yourserveradmin.com',
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    description='Module to easily convert Bind9 (named) zones into Terraform CloudFlare provider records definitions',
    include_package_data=True,
    install_requires=requirements(),
    license='MIT',
    long_description=readme(),
    long_description_content_type='text/markdown',
    name='terraform_named_cloudflare',
    packages=[
        'terraform_named_cloudflare'
    ],
    scripts=[
        'scripts/terraform-named-cloudflare'
    ],
    url='https://github.com/pa-yourserveradmin-com/terraform-named-cloudflare',
    version='0.0.2',
)
