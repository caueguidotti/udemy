#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# File        : intro_tk.py
# Project     : udemy
# Created By  : Caue Guidotti
# Created Date: 12/2/2020
# =============================================================================
"""
Basic tkinter functionalities
widget and callbacks
"""
# =============================================================================

import tkinter as tk


class ConverterWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.en_km_value = None
        self.tx_mile_value = None
        self.create_widget()

    def create_widget(self):
        bt_exec = tk.Button(self, text='Execute', command=self.km_to_miles)
        bt_exec.grid(row=1, column=0, columnspan=2, sticky=tk.W + tk.E)

        self.en_km_value = tk.Entry(self)
        self.en_km_value.grid(row=0, column=0)

        self.tx_mile_value = tk.Text(self, height=1, width=20)
        self.tx_mile_value.grid(row=0, column=1)

    def km_to_miles(self):
        km_value = self.en_km_value.get()
        try:
            mile_value = str(round(float(km_value)*1.6, 2))
        except ValueError:
            mile_value = 'Error'
        self.tx_mile_value.delete(1.0, tk.END)
        self.tx_mile_value.insert(tk.END, mile_value)


main_window = ConverterWindow()

main_window.mainloop()
