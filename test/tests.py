import pytest
import sys
from os import path

sys.path.append('../')
from lib.hamming import HammingCode


def test_hamming_code():
    assert HammingCode(inp_data='1101').generate_hamming_code() == 1100110
    assert HammingCode(inp_data='11011').generate_hamming_code() == 111010100
    assert HammingCode(ham_code='10101110111').dtct_err_in_hamcode() == None


