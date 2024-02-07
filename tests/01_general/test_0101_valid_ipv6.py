import pytest

from piracyshield_component.validation.validator import Validator
from piracyshield_component.validation.rules.ipv6 import IPv6

from piracyshield_component.validation.validator import ValidatorRuleNonValidException

class TestGeneral:

    valid_ipv6_list = [
        "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
        "fe80:0000:0000:0000:0204:61ff:fe9d:f156",
        "2001:0db8:0000:0000:0000:0000:0000:0001",
        "fe80:0000:0000:0000:0204:61ff:fe9d:f157",
        "2001:0db8:1234:5678:90ab:cdef:0000:0000",
        "2606:2800:220:1:248:1893:25c8:1946",
        "2001:4860:4860:0:0:0:0:6464",
        "2001:4860:4860:0:0:0:0:8844",
        "2001:4860:4860:0:0:0:0:8888",
        "2001:4860:4860:0:0:0:0:64",
        "2606:4700:4700:0:0:0:0:64",
        "2606:4700:4700:0:0:0:0:1001",
        "2606:4700:4700:0:0:0:0:1111",
        "2606:4700:4700:0:0:0:0:6400",
        "2a01:4f8:10a:1::4",
        "::1",
        "::"
    ]

    def test_valid_ipv6(self):
        """
        Check if the IPv6 list is valid.
        """

        for ipv6 in self.valid_ipv6_list:
            rules = [
                IPv6()
            ]

            v = Validator(ipv6, rules)

            v.validate()

            if len(v.errors) != 0:
                print(ipv6, v.errors)

            assert len(v.errors) == 0
