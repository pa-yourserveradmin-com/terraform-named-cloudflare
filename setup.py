from setuptools import setup

setup(
    author='Andrew Poltavchenko',
    author_email='pa@yourserveradmin.com',
    description='Module to easily convert Bind9 (named) zones into Terraform CloudFlare provider records definitions',
    include_package_data=True,
    license='MIT',
    name='terraform_named_cloudflare',
    packages=[
        'terraform_named_cloudflare'
    ],
    scripts=[
        'scripts/terraform-named-cloudflare'
    ],
    url='https://github.com/pa-yourserveradmin-com',
    version='0.0.1',
)
