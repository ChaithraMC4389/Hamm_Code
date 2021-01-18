import sys
from os import path

sys.path.append('../')

from utils.exceptions import ErrorCantBeDetectedException


class HammingCode:
    """

    """

    def __init__(self, **kwargs):
        """
        """
        if 'inp_data' in kwargs:
            self.inp_data = kwargs['inp_data'][::-1]
        else:
            self.inp_data = None

        if 'ham_code' in kwargs:
            self.ham_code = kwargs['ham_code']
        else:
            self.ham_code = None

        self.no_parity_bits = 0

    def cal_parity_bit_cnt(self):
        """
        """
        parity_cntr = 0
        while (len(self.inp_data) + parity_cntr + 1) > pow(2, parity_cntr):
            parity_cntr += 1

        return parity_cntr

    def position_parity_bits(self):
        """
        """
        no_parity_bits = self.cal_parity_bit_cnt()
        parity_pos = 0
        data_pos = 0
        par_pos_list = list()

        for i in range(0, no_parity_bits + len(self.inp_data)):
            pos = 2 ** parity_pos

            if pos == i + 1:
                par_pos_list.append(0)
                parity_pos += 1

            else:
                par_pos_list.append(int(self.inp_data[data_pos]))
                data_pos += 1

        return par_pos_list

    def calc_parity_bits(self):
        """
        """
        par_pos_list = self.position_parity_bits()
        parity_pos = 0

        for parity in range(0, len(par_pos_list)):
            pos = 2 ** parity_pos

            if pos == (parity + 1):
                start_index = pos - 1
                i = start_index
                xor_list = list()

                while i < len(par_pos_list):
                    block = par_pos_list[i:i + pos]
                    xor_list.extend(block)
                    i += 2 * pos

                for z in range(1, len(xor_list)):
                    par_pos_list[start_index] ^= xor_list[z]

                parity_pos += 1

        par_pos_list.reverse()

        return par_pos_list

    def generate_hamming_code(self):
        ham_code_lst = self.calc_parity_bits()
        return int(''.join(map(str, ham_code_lst)))

    def dtct_err_in_hamcode(self):
        data = list(self.ham_code)
        data.reverse()
        c, parity_pos, error, msg, parity_list, msg_copy = 0, 0, 0, [], [], []

        for k in range(0, len(data)):
            p = (2 ** c)
            msg.append(int(data[k]))
            msg_copy.append(data[k])
            if p == (k + 1):
                c = c + 1

        self.process_parity_for_dtct_ham(parity_pos, msg, parity_list)
        parity_list.reverse()
        error = sum(int(parity_list) * (2 ** i) for i, parity_list in enumerate(parity_list[::-1]))

        if error == 0:
            print('There is no error in the hamming code received')

        elif error >= len(msg_copy):
            print('Error cannot be detected')
            raise ErrorCantBeDetectedException

        else:
            print('Error is in', error, 'bit')

            if msg_copy[error - 1] == '0':
                msg_copy[error - 1] = '1'

            elif msg_copy[error - 1] == '1':
                msg_copy[error - 1] = '0'
                print('After correction hamming code is:- ')
            msg_copy.reverse()
            print(int(''.join(map(str, msg_copy))))

        # The following exception needs to be called when ever
        # We can't detect the error based on the code provided


    def process_parity_for_dtct_ham(self, parity_pos, msg, parity_list):
        for parity in range(0, (len(msg))):
            pos = (2 ** parity_pos)
            if pos == (parity + 1):
                start_index = pos - 1
                i = start_index
                xor_list= list()

                while i < len(msg):
                    block = msg[i:i + pos]
                    xor_list.extend(block)
                    i += 2 * pos

                for z in range(1, len(xor_list)):
                    msg[start_index] = msg[start_index] ^ xor_list[z]
                parity_list.append(msg[parity])
                parity_pos += 1
