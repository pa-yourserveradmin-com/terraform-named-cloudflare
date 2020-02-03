# terraform-named-cloudflare

Python module and tool to easily convert Bind9 (named) zones into Terraform
CloudFlare provider records definitions.

This module parses Bind9 (named) zone file and generates Terraform code with
CloudFlare resources definitions.

To make the result code organized, code separated based on DNS records types.

## Installation

### Production

The simplest way to install the module is to use PIP:

```bash
pip install terraform-named-cloudflare
```

### Development

To install the module from sources, just clone the repository and install the
module:

```bash
git clone https://github.com/pa-yourserveradmin-com/terraform-named-cloudflare.git
cd terraform-named-cloudflare
python3 setup.py install
```

## Usage

Example usage scenario is the next:

```bash
terraform-named-cloudflare \
    --file <NAMED_ZONE_FILE> \
    --zone-id <CLOUDFLARE_ZONE_ID> \
    --zone-name <CLOUDFLARE_ZONE_NAME>
```

Where:

- `NAMED_ZONE_FILE` - the absolute or relative path to zone file in Bind9 (named)
format.
- `CLOUDFLARE_ZONE_ID` - the optional CloudFlare zone ID (can be found in CloudFlare
WEB interface).
- `CLOUDFLARE_ZONE_NAME` - the optional CloudFlare zone name (the same as domain
name).

Since not all records need to be converted in Terraform code, the script ignores
some of them and just prints ignored records to standard output to provide ability
review them and add manually.

## Requirements

There are no specific requirements except a few weel-known and widelly used Python
modules listed in the [requirements.txt](requirements.txt) and automatically
installed with module.

## Limitations

The module does not understand DNS RRD records and always will create only one
resource with the same name. The rest will be ignored and printed to standard
output for review and manual changes in Terraform code.

## Supported DNS records types

Currently this module supports the next types of DNS records:

- A
- AAAA
- CNAME
- MX
- SRV
- TXT

Other types of DNS records can be added based on the need. Also, contrinutions
are always welcome.
