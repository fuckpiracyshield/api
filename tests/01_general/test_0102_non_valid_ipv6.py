import pytest

from piracyshield_component.validation.validator import Validator
from piracyshield_component.validation.rules.ipv6 import IPv6

from piracyshield_component.validation.validator import ValidatorRuleNonValidException

class TestGeneral:

    valid_ipv6_list = [
        # wrong length
        "2001:0db8:85a3:0000:0000:8a2e:0370:7334:1234",
        "FE80:0000:0000:0000:0202:B3FF:FE1E:8329:ABCD:EF12",
        "1234:5678:9ABC:DEF0:1234:5678:9ABC:DEF0:1234",

        # non valid characters
        "2001:0db8:85a3:0000:0000:8a2e:0370:73G4",
        "FE80:0000:0000:0000:0202:B3FF:FE1E:832Z",
        "2001:0db8::85a3::7334",

        # too many segments
        "FE80:0000:0000:0000:0202:B3FF:FE1E:8329:1234",
        "2001:0db8:85a3:0000:0000:8a2e:0370:7334:5678",

        # too few segments
        "2001:0db8:85a3:0000:8a2e:0370",
        "FE80:0000:B3FF:FE1E:8329",

        # consecutive double colons
        "2001:0db8::85a3::7334",
        "::1234::5678::9ABC",

        # leading zeros in a quad

        "2001:0db8:85a3:00001:0000:8a2e:0370:7334",
        "FE80:00000:0000:0000:0202:B3FF:FE1E:8329",

        # non valid dot in notation
        "2001:0db8:85a3:0000:0000:8a2e:0370.7334",
        "FE80:0000:0000:0000:0202:B3FF:FE1E:8329.1234",

        # mixed ipv6/ipv4

        "2001:0db8:85a3:0000:0000:8a2e:192.168.1.1.1",
        "::ffff:192.168.0.256",

        # segment with more than 4 hex characters

        "2001:0db8:85a3:00000:0000:8a2e:0370:7334",
        "FE80:0000:0000:10000:0202:B3FF:FE1E:8329",

        # segment with non-hex characters
        "2001:0db8:85g3:0000:0000:8a2e:0370:7334",
        "FE80:0000:0000:0000:0202:B3ZZ:FE1E:8329",

        # incorrect ipv4 mapping
        "::ffff:192.168.0.999",
        "::ffff:299.255.255.255"
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

            if len(v.errors) == 0:
                print(ipv6, v.errors)

            assert len(v.errors) != 0
