#!/usr/bin/env python3

import getpass
import random
import sys

from argparse import ArgumentParser, RawTextHelpFormatter

from typing import List

try:
    import OpenSSL
except Exception:
    print("Failed to import OpenSSL.\n\
Make sure you have \"pyopenssl\" installed", file=sys.stderr)  # Yay E501 :/
    sys.exit(1)


def ask_password(arg) -> bytes:
    pw = getpass.getpass("Enter password for key: ")
    return pw.encode()


def generate_key() -> OpenSSL.crypto.PKey:
    p_key = OpenSSL.crypto.PKey()
    p_key.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)
    return p_key


def generate_csr(key: OpenSSL.crypto.PKey,
                 dns_names: List[str],
                 country_code="DE",
                 state="Hessen",
                 locality="Darmstadt",
                 organization="h-da",
                 organizational_unit="ECS",
                 email="webmaster@ecs.fbi.h-da.de",
                 CN=None,
                 CA=False
                 ) -> OpenSSL.crypto.X509Req:
    req = OpenSSL.crypto.X509Req()
    if len(dns_names) > 0 and CN is None:
        CN = dns_names[0]
    req.get_subject().CN = CN
    req.get_subject().C = country_code
    req.get_subject().ST = state
    req.get_subject().L = locality
    req.get_subject().organizationName = organization
    req.get_subject().OU = organizational_unit
    req.get_subject().emailAddress = email

    req.set_pubkey(key)

    extensions = []
    if len(dns_names) > 0:
        san_names = ""
        san_list = []
        for name in dns_names:
            san_list.append(f"DNS: {name}")
        san_names = ", ".join(san_list)
        extensions.append(OpenSSL.crypto.X509Extension(
                 b"subjectAltName",
                 False,
                 san_names.encode()
                 ))
    ca_val = b"CA:FALSE"
    if CA:
        ca_val = b"CA:TRUE"
    extensions.append(OpenSSL.crypto.X509Extension(
            b"basicConstraints",
            False,
            ca_val
            ))
    extensions.append(OpenSSL.crypto.X509Extension(
            b"keyUsage",
            False,
            b"digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment"  # noqa: E501
            ))
    req.add_extensions(extensions)
    req.set_pubkey(key)
    req.sign(key, "sha512")

    return req


def __save_data(output: str, data: bytes) -> None:
    with open(output, "wb") as out_file:
        out_file.write(data)


def save_key(ssl_key: OpenSSL.crypto.PKey, output: str) -> None:
    key_pem = OpenSSL.crypto.dump_privatekey(
            OpenSSL.crypto.FILETYPE_PEM, ssl_key)
    __save_data(output, key_pem)


def save_req(req: OpenSSL.crypto.X509Req, output: str) -> None:
    req_pem = OpenSSL.crypto.dump_certificate_request(
        OpenSSL.crypto.FILETYPE_PEM, req)
    __save_data(output, req_pem)


def save_cert(cert: OpenSSL.crypto.X509, output: str) -> None:
    req_pem = OpenSSL.crypto.dump_certificate(
        OpenSSL.crypto.FILETYPE_PEM, cert)
    __save_data(output, req_pem)


def __load_data(file_path: str) -> bytes:
    with open(file_path, "rb") as in_file:
        return in_file.read()


def load_key(file_path: str) -> OpenSSL.crypto.PKey:
    key_data = __load_data(file_path)
    return OpenSSL.crypto.load_privatekey(
            OpenSSL.crypto.FILETYPE_PEM, key_data, ask_password)


def load_cert(file_path: str) -> OpenSSL.crypto.X509:
    key_data = __load_data(file_path)
    return OpenSSL.crypto.load_certificate(
            OpenSSL.crypto.FILETYPE_PEM, key_data)


def load_csr(file_path: str) -> OpenSSL.crypto.X509:
    key_data = __load_data(file_path)
    return OpenSSL.crypto.load_certificate_request(
            OpenSSL.crypto.FILETYPE_PEM, key_data)


def sign_req(root_cert: OpenSSL.crypto.X509,
             root_key: OpenSSL.crypto.PKey,
             csr: OpenSSL.crypto.X509Req) -> OpenSSL.crypto.X509:
    serial = random.getrandbits(64)  # should never collide
    out_cert = OpenSSL.crypto.X509()
    out_cert.set_serial_number(serial)
    out_cert.gmtime_adj_notBefore(0)
    out_cert.gmtime_adj_notAfter(2*(3600 * 24 * 365))
    out_cert.set_subject(csr.get_subject())
    out_cert.set_issuer(root_cert.get_subject())
    out_cert.set_pubkey(csr.get_pubkey())
    out_cert.add_extensions(csr.get_extensions())
    out_cert.set_version(2)

    out_cert.sign(root_key, "sha512")
    return out_cert


if __name__ == "__main__":
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument("--ca-key", dest="ca_key", help="Key of the CA",
                        type=str, required=True)
    parser.add_argument("--ca-cert", dest="ca_cert", help="Cert of the CA",
                        type=str, required=True)
    parser.add_argument("--domains", dest="domains",
                        help="Domains to use for the cert. \
                              The first domain is the CN and output name",
                        type=str, nargs="+", default=[])
    parser.add_argument("--csr", dest="csr", help="Use an existing csr",
                        type=str, default=None)
    parser.add_argument("--key", dest="key", help="Use an existing key",
                        type=str, default=None)
    parser.add_argument("--ca", dest="ca", help="Add the CA flag",
                        action="store_true")
    parser.add_argument("-o", dest="output", help="Custom output name",
                        type=str)
    parser.add_argument("--cn", dest="cn", help="Custom common name",
                        type=str, default=None)

    args = parser.parse_args()

    ca_key = load_key(args.ca_key)
    ca_cert = load_cert(args.ca_cert)
    if args.output:
        output_name = args.output
    else:
        output_name = args.domains[0]

    csr = None
    key = None

    if args.csr is not None:
        csr = load_csr(args.csr)
    else:
        if args.key is None:
            key = generate_key()
        else:
            key = load_key(args.key)
        csr = generate_csr(key, args.domains, CA=args.ca, CN=args.cn)

    cert = sign_req(ca_cert, ca_key, csr)
    if args.key is None and args.csr is None:
        save_key(key, f"{output_name}.key")
    save_cert(cert, f"{output_name}.crt")
