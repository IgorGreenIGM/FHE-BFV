import ctypes
import backend
import customtkinter
from typing import Tuple
from tkinter import messagebox

customtkinter.set_appearance_mode('light')
customtkinter.set_default_color_theme("green")
DPI_SCALE = float(ctypes.windll.shcore.GetScaleFactorForDevice(0)) / 100

class App(customtkinter.CTk):

    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        
        # création de la fenetre 
        self.title("Projet SI -- Chiffrement Homomorphe")
        self.w_width = 1000; self.w_height = 600
        self.geometry(f"{self.w_width}x{self.w_height}+{int((self.winfo_screenwidth()-self.w_width) * DPI_SCALE // 2)}+{int((self.winfo_screenheight()-self.w_height) * DPI_SCALE // 2)}")
        self.resizable(False, False)

        # varaibles de tracking : 
        self.operand1 = customtkinter.StringVar(self, "0")
        self.operand2 = customtkinter.StringVar(self, "0")
        self.operator = customtkinter.StringVar(self, "Addition")
        self.mu = customtkinter.StringVar(self, "0")
        self.sigma = customtkinter.StringVar(self, "1.6")
        self.ring_size = customtkinter.StringVar(self, "1024")
        self.ct_size = customtkinter.StringVar(self, "132120577")
        self.psi = customtkinter.StringVar(self, "73993")

        # barre de navigation (à gauche)
        self.nav_bar = customtkinter.CTkLabel(self, width=200, text='', corner_radius=0)
        self.nav_bar.grid(row=0, column=0, sticky='nsew')

        # valeur 1
        self.value1 = customtkinter.CTkLabel(self.nav_bar, text="Valeur 1", width=20)
        self.value1.grid(row=0, column=0, sticky='nw', padx=20, pady=(5, 10))
        self.value_entry1 = customtkinter.CTkEntry(self.nav_bar, placeholder_text="1ere Opérande", textvariable=self.operand1)
        self.value_entry1.grid(row=1, column=0, sticky='nw', padx=20, pady=(0, 20))

        # operateur
        self.operator_text = customtkinter.CTkLabel(self.nav_bar, text="Opérateur")
        self.operator_text.grid(row=2, column=0, sticky='nw', padx=20, pady=(0, 5))
        self.operator_list = customtkinter.CTkOptionMenu(self.nav_bar, values=[f"Addition{' '*15}+", f"Soustraction{' '*6}-", f"Multiplication{' '*4}x"], variable=self.operator)
        self.operator_list.grid(row=3, column=0, sticky='nw', padx=20, pady=(0, 20))
        
        # valeur 2
        self.value2 = customtkinter.CTkLabel(self.nav_bar, text="Valeur 2", width=20)
        self.value2.grid(row=4, column=0, sticky='nw', padx=20, pady=(0, 10))
        self.value_entry2 = customtkinter.CTkEntry(self.nav_bar, placeholder_text="2eme Opérande", textvariable=self.operand2)
        self.value_entry2.grid(row=5, column=0, sticky='nw', padx=20, pady=(0, 20))

        # bouton calculer
        self.compute_button = customtkinter.CTkButton(self.nav_bar, text=f"Calculer{' '*19}| ⚙", anchor='right', command=self.compute)
        self.compute_button.grid(row=6, column=0, sticky='nw', padx=20, pady=(10, 0))

        # frame des paramètres de generation
        self.params = customtkinter.CTkScrollableFrame(self.nav_bar, height=170, label_text="Paramètres")
        self.params.grid(row=7, column=0, padx=20, pady=20)

        # paramètres mu
        self.param_mu = customtkinter.CTkLabel(self.params, text="mu ")
        self.param_mu.grid(row=0, column=0, sticky='w')
        self.param_mu_entry = customtkinter.CTkEntry(self.params, placeholder_text='0.123', width=120, textvariable=self.mu)
        self.param_mu_entry.grid(row=0, column=1, padx=(35, 0))

        # paramètres sigma
        self.param_sigma = customtkinter.CTkLabel(self.params, text="sigma ")
        self.param_sigma.grid(row=1, column=0, pady=15, sticky='w')
        self.param_sigma_entry = customtkinter.CTkEntry(self.params, placeholder_text='0.725', width=120, textvariable=self.sigma)
        self.param_sigma_entry.grid(row=1, column=1, padx=(35, 0))

        # paramètre n (taille de l'anneau)
        self.param_ring_size = customtkinter.CTkLabel(self.params, text="anneau")
        self.param_ring_size.grid(row=2, column=0, sticky='w')
        self.param_ring_size_entry = customtkinter.CTkEntry(self.params, placeholder_text='1024', width=120, textvariable=self.ring_size)
        self.param_ring_size_entry.grid(row=2, column=1, padx=(35, 0))

        # paramètre q (anneau cu corps des chiffrés)
        self.param_ct_size = customtkinter.CTkLabel(self.params, text="c-ct")
        self.param_ct_size.grid(row=3, column=0, sticky='w', pady=15)
        self.param_ct_size_entry = customtkinter.CTkEntry(self.params, placeholder_text='132120577', width=120, textvariable=self.ct_size)
        self.param_ct_size_entry.grid(row=3, column=1, padx=(35, 0))

        # paramètre psi
        self.param_psi_size = customtkinter.CTkLabel(self.params, text="psi")
        self.param_psi_size.grid(row=4, column=0, sticky='w')
        self.param_psi_size_entry = customtkinter.CTkEntry(self.params, placeholder_text='73993', width=120, textvariable=self.psi)
        self.param_psi_size_entry.grid(row=4, column=1, padx=(35, 0))

        self.logs = customtkinter.CTkTextbox(self, width=735)
        self.logs.insert('end', f'{" "*70}=====================================================\n')
        self.logs.insert('end', f'{" "*70}=======| Chiffrement Totalement Homomorphe (FHE) |=======\n')
        self.logs.insert('end', f'{" "*70}=====================================================\n\n\n')

        self.logs.insert('end', 'Initialisation des paramètres de génération . . .\n')
        self.logs.focus_force()
        self.logs.grid(row=0, column=1, sticky='nsew')

    def eval_gen_params(self) -> bool:
        if not self.ring_size.get().isnumeric() or not self.ct_size.get().isnumeric():
            print("true here")
            return False
        try:
            float(self.mu.get())
            float(self.sigma.get())
            float(self.psi.get())
        except:
            print("false here")
            return False
        else:
            print("false here 2")
            return True

    def compute(self):
        self.logs.delete('1.0', customtkinter.END)
        # verification des paramètres de générations
        if not self.eval_gen_params():
            messagebox.showerror("Gen Error", "Erreur lors de la générations des paramètres. Veuillez essayer à nouveau!")
            return

        # verification des opérandes
        op1 : int = 0; op2 : int = 0
        try:
            op1 = int(self.operand1.get())
            op2 = int(self.operand2.get())
        except:
            messagebox.showerror("Type Error", "les Opérandes 1 et 2 doivent être des entiers")
            return
        
        # création de l'évaluateur
        Evaluator = backend.init_params(float(self.mu.get()), 
                                        float(self.sigma.get()), 
                                        int(self.ring_size.get()), 
                                        int(self.ct_size.get()), 
                                        int(self.psi.get()))        

        # Génération des clés publiques et privées
        Evaluator.GenererCleSecrete()
        Evaluator.GenererClePublique()
        Evaluator.EvaluerGenererCleV1(256)
        pk = Evaluator.pk
        sk = Evaluator.sk   


        # encodage de l'operande 1
        poly_op1 = Evaluator.IntEncode(op1)
        self.logs.insert('end', f'\n{str(Evaluator)}\n')
        self.logs.insert('end', f"encodage de l'operande 1 [{op1}]: \n=================================\n")
        self.logs.insert('end', str(poly_op1))        
        # chiffrement de l'operande 1
        ct1 = Evaluator.Chiffrer(poly_op1)
        self.logs.insert('end', f"\n\nChiffrement de l'operande 1 [{op1}]: \n=================================\n")
        self.logs.insert('end', "[0] : " + str(ct1[0])[:105] + "...")
        self.logs.insert('end', "\n[1] : " + str(ct1[1])[:105] + "...")

        # encodage de l'operande 2
        poly_op2 = Evaluator.IntEncode(op2)
        self.logs.insert('end', f"\n\nencodage de l'operande 2 [{op2}]: \n=================================\n")
        self.logs.insert('end', str(poly_op2)) 
        # chiffrement de l'operande 2
        ct2 = Evaluator.Chiffrer(poly_op2)
        self.logs.insert('end', f"\n\nChiffrement de l'operande 2 [{op2}]: \n=================================\n")
        self.logs.insert('end', "[0] : " + str(ct2[0])[:105] + "...")
        self.logs.insert('end', "\n[1] : " + str(ct2[1])[:100] + "...")

        self.logs.insert('end', "\n\nClé Publique : \n===============\n")
        self.logs.insert('end', "[0] : " + str(pk[0])[:105] + "...")
        self.logs.insert('end', "\n[1] : " + str(pk[1]))
        self.logs.insert('end', "\n\nClé Secrete : \n===============\n")
        self.logs.insert('end', str(sk))

        # verification de l'operateur
        operator = self.operator.get().strip().split()[0].lower()
        if operator == 'addition':
            ct = Evaluator.HomomorphicAddition(ct1, ct2)

        elif operator == 'soustraction':
            ct = Evaluator.HomomorphicSubtraction(ct1, ct2)

        elif operator == 'multiplication':
            ct = Evaluator.HomomorphicMultiplication(ct1, ct2)

        else:
            messagebox.showerror('operator error', "veuillez selectionnez l'operateur dans la liste!")
            return
        
        self.logs.insert('end', "\n\nRésultat de l'operation sur les chiffrés: \n=================================\n")
        self.logs.insert('end', "[0] : " + str(ct[0])[:105] + "...")
        self.logs.insert('end', "\n[1] : " + str(ct[1])[:105] + "...")

        # déchiffrement
        mt = Evaluator.Dechiffrer(ct)
        nr = Evaluator.IntDecode(mt)
        self.logs.insert('end', "\n\nDéchiffrement des Résultats : \n=================================\n")
        self.logs.insert('end', f"Résultat Obtenu après chiffrement : {nr}\n\n")

app = App()
app.mainloop()