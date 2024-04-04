import re
import tkinter
import customtkinter
import multiprocessing
import class_call
import pickle


pull = []


class Tkinter(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title('Номер телефона')
        self.geometry('380x220')
        self.resizable(False, False)
        self.iconbitmap('Icon.ico')

        self.text = customtkinter.CTkLabel(self, text='Введите номер телефона в поле ниже')
        self.text.pack()

        self.check = (self.register(self.is_valid), "%P")

        self.entry = customtkinter.CTkEntry(self, validate="key", width=280, validatecommand=self.check)
        self.entry.pack(pady=5)

        self.btn = customtkinter.CTkButton(self, text='Применить', command=self.accept)
        self.btn.pack(pady=10)

        self.errmsg = tkinter.StringVar()
        self.text_info = customtkinter.CTkLabel(self, textvariable=self.errmsg, text_color='#66CD00')
        self.text_info.pack()

        self.errmsg_warning = tkinter.StringVar()
        self.text_info_warning = customtkinter.CTkLabel(self, textvariable=self.errmsg_warning, text_color='#FF4040')
        self.text_info_warning.pack()

        Tkinter.loading()

        self.phone = customtkinter.CTkLabel(self, text=f'{pull[0]}', text_color='#FFD700')
        self.phone.pack()

        customtkinter.set_appearance_mode("dark")

    @staticmethod
    def loading():
        with open('config.pkl', 'rb') as f:
            loaded_list = pickle.load(f)
            pull.clear()
            pull.append(loaded_list[0])
            return loaded_list[0]

    @staticmethod
    def uploading(uploading_dict):
        with open('config.pkl', 'wb') as f:
            pickle.dump(uploading_dict, f)

    def accept(self):
        a1 = self.entry.get()
        if a1 != None and len(a1) == 12:
            pull.clear()
            pull.append(a1)
            Tkinter.uploading(pull)
            Tkinter.loading()
            self.phone.destroy()
            self.phone = customtkinter.CTkLabel(self, text=f'{pull[0]}', text_color='#FFD700')
            self.phone.pack()
            self.errmsg.set('Номер телефона применен!\n'
                            f'Звонки теперь будут происходить с номера: {a1}')

            self.entry.configure(border_color='')
            self.entry.delete(0, len(self.entry.get()))
            if self.errmsg_warning:
                self.errmsg_warning.set('')
        elif a1 == '':
            self.errmsg_warning.set('Необходимо заполнить поле выше!')
            self.entry.configure(border_color='#FF4040')
        else:
            self.errmsg_warning.set('Номер телефона должен быть в формате\n'
                                    '375xxxxxxxxх, где x представляет цифру')

    def is_valid(self, val):
        result = re.match("^\d{0,12}$", val) is not None
        if not result and len(val) <= 13:
            if self.errmsg:
                self.errmsg.set('')
            self.errmsg_warning.set('Номер телефона должен быть в формате\n'
                                    '375xxxxxxxxх, где x представляет цифру')
        else:
            self.errmsg_warning.set('')
        return result


if __name__ == '__main__':
    multiprocessing.freeze_support()
    process_1 = multiprocessing.Process(target=class_call.key, daemon=True)
    process_1.start()
    gui = Tkinter()
    gui.mainloop()
