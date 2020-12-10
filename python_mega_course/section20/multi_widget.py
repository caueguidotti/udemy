#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# File        : multi_widget.py
# Project     : udemy
# Created By  : Caue Guidotti
# Created Date: 12/9/2020
# =============================================================================
"""
Multi-widget practice from course part #167
- my own improved version...
"""
# =============================================================================

import tkinter as tk


class MassConverter(tk.Tk):
    def __init__(self):
        super(MassConverter, self).__init__()

        self.en_value2convert = None
        self.tx_converted_list = []
        self.possible_conversion = ['kg', 'g', 'lb', 'oz']
        self.base_conversion_prop = 'kg'
        self.base_conversion_val_dict = {'kg': 1, 'g': 1000, 'lb': 2.20462, 'oz': 35.274}
        self.radio_var = tk.StringVar(value=self.possible_conversion[0])

        assert all(prop in self.base_conversion_val_dict for prop in self.possible_conversion)
        assert (self.base_conversion_prop in self.base_conversion_val_dict and
                self.base_conversion_val_dict[self.base_conversion_prop] == 1)
        self.conversion_error_txt = 'Error'

        self.create_widgets()

    def create_widgets(self):

        # create label informing to select source
        label_kg = tk.Label(self, text='Select Source: ')
        label_kg.grid(row=0, column=0, sticky=tk.E)

        # frame to hold radio buttons
        radio_frame = tk.Frame(self)
        radio_frame.grid(row=0, column=1, sticky=tk.W + tk.E)

        # radios to select source
        for num, prop in enumerate(self.possible_conversion):
            radio = tk.Radiobutton(radio_frame, text=prop, variable=self.radio_var, value=prop,
                                   tristatevalue='-', command=self.convert_mass)
            radio.grid(row=0, column=num)

        # create kg entry
        self.en_value2convert = tk.Entry(self)
        self.en_value2convert.grid(row=0, column=2, sticky=tk.W + tk.E)

        # create conversion button
        convert_button = tk.Button(self, text='Convert', command=self.convert_mass)
        convert_button.grid(row=0, column=3, sticky=tk.W + tk.E)

        # create conversion result texts
        for num in range(len(self.possible_conversion)-1):
            tx_converted = tk.Text(self, height=1, width=20)
            tx_converted.grid(row=1, column=num+1)
            self.tx_converted_list.append(tx_converted)

    def clear_all_txs(self):
        for tx_converted in self.tx_converted_list:
            tx_converted.delete(1.0, tk.END)

    def get_converted_str(self, value, conversion_ratio, round_ndigits=4):
        if not value:
            return ''
        try:
            converted_value = str(round(float(value)*conversion_ratio, round_ndigits))
        except ValueError:
            converted_value = self.conversion_error_txt
        return converted_value

    def get_conversion_ratio(self, source_prop, dst_prop):
        return (self.base_conversion_val_dict[self.base_conversion_prop] /
                self.base_conversion_val_dict[source_prop])/(self.base_conversion_val_dict[self.base_conversion_prop] /
                                                             self.base_conversion_val_dict[dst_prop])

    def insert_to_tx(self, tx_widget, txt, prop, idx=tk.END):
        if txt and txt != self.conversion_error_txt:
            txt += ' ' + prop
        tx_widget.insert(idx, txt)

    def convert_mass(self):
        value2convert = self.en_value2convert.get()
        source_prop = self.radio_var.get()
        converted_props = list(filter(lambda x: x != source_prop, self.possible_conversion))
        conversion_dict = {prop: self.get_conversion_ratio(source_prop, prop) for prop in converted_props}

        self.clear_all_txs()

        for num, (tx_converted, (prop, prop_conversion)) in enumerate(zip(self.tx_converted_list, conversion_dict.items())):
            self.insert_to_tx(tx_converted, self.get_converted_str(value2convert, prop_conversion), prop)


main_window = MassConverter()
main_window.mainloop()
