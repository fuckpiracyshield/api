import pytest

from piracyshield_component.validation.validator import Validator
from piracyshield_component.validation.rules.cidr_syntax_ipv4 import CIDRSyntaxIPv4

from piracyshield_component.validation.validator import ValidatorRuleNonValidException

from random import randint

class TestGeneral:

    max_cidr_classes = 10000

    valid_cidr_ipv4_list = []

    def setup_method(self):
        self.valid_cidr_ipv4_list = self.__generate_random_list(self.max_cidr_classes)

    def test_valid_cidr_ipv4(self):
        """
        Check if the CIDR IPv4 syntax is valid.
        """

        for cidr_ipv4 in self.valid_cidr_ipv4_list:
            rules = [
                CIDRSyntaxIPv4()
            ]

            v = Validator(cidr_ipv4, rules)

            v.validate()

            if len(v.errors) != 0:
                print(cidr_ipv4, v.errors)

            assert len(v.errors) == 0

    def __generate_random_list(self, size: int):
        cidr_list = []
        subnet_variety = [8, 16, 24]  # Different subnet masks for variety

        for i in range(0, size):
            for subnet in subnet_variety:
                cidr_list.append(f"{randint(1, 254)}.0.0.0/{subnet}")

        return cidr_list
