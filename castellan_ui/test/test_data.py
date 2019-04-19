#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from castellan.common.objects import opaque_data as op_data
from castellan.common.objects import passphrase as passp
from castellan.common.objects import private_key as pri_key
from castellan.common.objects import public_key as pub_key
from castellan.common.objects import symmetric_key as sym_key
from castellan.common.objects import x_509
from castellan.tests import utils as castellan_utils

x509_cert = x_509.X509(
    data=castellan_utils.get_certificate_der(),
    name='test cert',
    created=1448088699,
    id=u'00000000-0000-0000-0000-000000000000')

nameless_x509_cert = x_509.X509(
    data=castellan_utils.get_certificate_der(),
    name=None,
    created=1448088699,
    id=u'11111111-1111-1111-1111-111111111111')

private_key = pri_key.PrivateKey(
    key=castellan_utils.get_private_key_der(),
    algorithm="RSA",
    bit_length=2048,
    name=u'test private key',
    created=1448088699,
    id=u'00000000-0000-0000-0000-000000000000')

nameless_private_key = pri_key.PrivateKey(
    key=castellan_utils.get_private_key_der(),
    algorithm="RSA",
    bit_length=2048,
    name=None,
    created=1448088699,
    id=u'11111111-1111-1111-1111-111111111111')

public_key = pub_key.PublicKey(
    key=castellan_utils.get_public_key_der(),
    algorithm="RSA",
    bit_length=2048,
    name=u'test public key',
    created=1448088699,
    id=u'00000000-0000-0000-0000-000000000000')

nameless_public_key = pub_key.PublicKey(
    key=castellan_utils.get_public_key_der(),
    algorithm="RSA",
    bit_length=2048,
    name=None,
    created=1448088699,
    id=u'11111111-1111-1111-1111-111111111111')

symmetric_key = sym_key.SymmetricKey(
    key=castellan_utils.get_symmetric_key(),
    algorithm="AES",
    bit_length=128,
    name=u'test symmetric key',
    created=1448088699,
    id=u'00000000-0000-0000-0000-000000000000')

nameless_symmetric_key = sym_key.SymmetricKey(
    key=castellan_utils.get_symmetric_key(),
    algorithm="AES",
    bit_length=128,
    name=None,
    created=1448088699,
    id=u'11111111-1111-1111-1111-111111111111')

opaque_data = op_data.OpaqueData(
    data=b'\xde\xad\xbe\xef',
    name=u'test opaque data',
    created=1448088699,
    id=u'00000000-0000-0000-0000-000000000000')

nameless_opaque_data = op_data.OpaqueData(
    data=b'\xde\xad\xbe\xef',
    name=None,
    created=1448088699,
    id=u'11111111-1111-1111-1111-111111111111')

passphrase = passp.Passphrase(
    passphrase=u'P@ssw0rd',
    name=u'test passphrase',
    created=1448088699,
    id=u'00000000-0000-0000-0000-000000000000')

nameless_passphrase = passp.Passphrase(
    passphrase=u'P@ssw0rd',
    name=None,
    created=1448088699,
    id=u'11111111-1111-1111-1111-111111111111')
