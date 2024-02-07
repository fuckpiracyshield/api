import pytest

from piracyshield_component.validation.validator import Validator
from piracyshield_component.validation.rules.cidr_syntax_ipv6 import CIDRSyntaxIPv6

from piracyshield_component.validation.validator import ValidatorRuleNonValidException

from random import randint, getrandbits

from ipaddress import IPv6Address

class TestGeneral:

    max_cidr_classes = 10000

    valid_cidr_ipv6_list = []

    def setup_method(self):
        self.valid_cidr_ipv6_list = self.__generate_random_list(self.max_cidr_classes)

    def test_valid_cidr_ipv6(self):
        """
        Check if the CIDR IPv6 syntax is valid.
        """

        for cidr_ipv6 in self.valid_cidr_ipv6_list:
            rules = [
                CIDRSyntaxIPv6()
            ]

            v = Validator(cidr_ipv6, rules)

            v.validate()

            if len(v.errors) != 0:
                print(cidr_ipv6, v.errors)

            assert len(v.errors) == 0

    def __generate_random_list(self, size: int):
        cidr_list = []

        for _ in range(size):
            # Generating a random IPv6 address
            random_ip = IPv6Address(getrandbits(128))

            # Choosing a random subnet mask
            subnet_mask = randint(1, 128)

            # Combining to form CIDR notation
            cidr = f"{random_ip}/{subnet_mask}"
            cidr_list.append(cidr)

        return cidr_list
