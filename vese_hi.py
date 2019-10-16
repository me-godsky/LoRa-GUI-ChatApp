from tkinter import *
import tkMessageBox
import socket
import sys
from threading import Thread
from ttt_server import ttt_server
import pygame
from grid import Grid

L_FONT = ("Verdana", 35)
M_FONT = ("Times new roman", 15)
S_FONT = ("Verdana",10)

m = ''




import time, base64, sys
from Crypto.Cipher import AES
from SX127x.constants import add_lookup, MODE, BW, CODING_RATE, GAIN, PA_SELECT, PA_RAMP, MASK, REG
from SX127x.LoRa import set_bit, getter, setter


from SX127x.LoRa import LoRa
from SX127x.board_config import BOARD


BOARD.setup()
BOARD.reset()


class mylora(LoRa):
    def __init__(self, verbose=False):
        super(mylora, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)
        self.var=0
        self.key = '1234567890123456'

    def on_rx_done(self):
        
        BOARD.led_on()
        
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        mens=payload[4:-1] 
        mens=bytes(mens).decode("utf-8",'ignore')
        cipher = AES.new(self.key)
        decodemens=base64.b64decode(mens)
        decoded = cipher.decrypt(decodemens)
        decoded = bytes(decoded).decode("utf-8",'ignore')
        
        BOARD.led_off()
        time.sleep(2) 
        
        self.var=1
        return decoded

    def on_tx_done(self):
        print("\nTxDone")
        print(self.get_irq_flags())

    def on_cad_done(self):
        print("\non_CadDone")
        print(self.get_irq_flags())

    def on_rx_timeout(self):
        print("\non_RxTimeout")
        print(self.get_irq_flags())

    def on_valid_header(self):
        print("\non_ValidHeader")
        print(self.get_irq_flags())

    def on_payload_crc_error(self):
        print("\non_PayloadCrcError")
        print(self.get_irq_flags())

    def on_fhss_change_channel(self):
        print("\non_FhssChangeChannel")
        print(self.get_irq_flags())

    def start(self, msg_text):    
    	      
        while True:
           
			cipher = AES.new(self.key)
			encoded = base64.b64encode(cipher.encrypt(msg_text))
			lista=list(encoded)
			lista.insert(0,0)
			lista.insert(0,0)
			lista.insert(0,255)
			lista.insert(0,255)
			lista.append(0)
			self.write_payload(lista)
			                
		self.var=0
		self.reset_ptr_rx()
            




class Godsky(Tk):

    def __init__(self, *args, **kwargs):
        
        Tk.__init__(self)
        container = Frame(self, width = 1600, height = 800)

        container.pack(side="top",fill="both", expand = False)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        



class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        controller.title("G0D$KY's GUI Game")
        one = Label(self, text ='''
LICENSE''', fg = "red", font = L_FONT)
        one.pack(fill = BOTH, side = "top")
        two = Label(self, text = ''' 

This tool is designed by G0d$ky solely for educational purposes. 
Do not copy the content or try to use for selling it.
Just ask for permission if you want to use any of the
specified content.

You can help me make the code better (just ask permission for pull request) 
or report bug; after examining the code if i feel the branch to be 
useful, i'd be more than happy to make the code better :)

''', fg = "black", font = M_FONT)
        two.pack(fill = BOTH, side = "top")
        var = IntVar()
        c = Checkbutton(self, text = "I have read all the LICENSE and accept all the conditions", font = S_FONT, variable= var)
        c.pack(side = "top")
        x = Label(self , text = '''
''')
        x.pack(side="top")
        button1 = Button(self, text = "Next", fg = "white",bg="black", font = S_FONT, command = lambda: controller.show_frame(PageOne) if var.get() else -1) 
        button1.pack(side = "top")





firstclick = True

class PageOne(Frame):
	global m
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		label = Label(self, text="NICK_NAME",fg="orange" ,font=L_FONT)
		label.pack(pady=150,padx=50)
		self.ma=StringVar()
		m = self.ma
		m.set("Type username here...")
		l1 = Label(self, text= "Username", font = M_FONT)
		self.e1 = Entry(self, textvariable=m)
		self.e1.bind('<FocusIn>', self.on_entry_click)
		self.e1.bind("<Return>", self.set)

		l1.pack(side = "top",fill = BOTH, padx = 20, pady = 20)
		self.e1.pack(side = "top")
		
		button2 = Button(self, text="Login", command= lambda : self.getter(controller))
		button2.pack(side = "bottom",pady=30)

	def on_entry_click(self,event):
		       
		global firstclick
		if firstclick:
			firstclick = False
			self.e1.delete(0, "end")

	def set(self):
		global m
		m = m + self.e1.get()

	def getter(self, controller):
		self.set()
		controller.show_frame(PageTwo) 
        






firstclic = True
game_script = ''

class PageTwo(Frame, mylora):
	global m, game_script
	def __init__(self, parent, controller):

		self.lora = mylora(verbose=False)


		self.lora.set_pa_config(pa_select=1, max_power=21, output_power=15)
		self.lora.set_bw(BW.BW125)
		self.lora.set_coding_rate(CODING_RATE.CR4_8)
		self.lora.set_spreading_factor(12)
		self.lora.set_rx_crc(True)

		self.lora.set_low_data_rate_optim(True)

		assert(self.lora.get_agc_auto_on() == 1)

		receive_thread = Thread(target=self.receive)
		receive_thread.start()
		controller.protocol("WM_DELETE_WINDOW", self.onClosing(controller))

		Frame.__init__(self, parent)
		menu = Menu(self, tearoff=0)
		controller.config(menu= menu)
		subMenu = Menu(menu)
		menu.add_cascade(label="File", menu = subMenu)
		subMenu.add_command(label="New", command=lambda : self.doNothing())
		subMenu.add_command(label="Save", command=lambda : self.doNothing())
		subMenu.add_separator()
		subMenu.add_command(label="Exit", command=controller.quit)
		editMenu = Menu(menu)
		menu.add_cascade(label="Edit", menu = editMenu)
		editMenu.add_command(label="Redo", command=lambda : self.doNothing())


		label = Label(self, text="G0D$KY's CHATaPP", fg = "brown", font=L_FONT)
		label.pack(pady=50,padx=10)
		y = "Hey Wassup..."

		l2 = Label(self, text = y, font = M_FONT, fg = "red")
		l2.pack(side = "top")

		send_request = Button(self, text="Play Tic-Tac-Toe",bd = 5, bg = "grey", fg = "white",command=lambda : self.send1(controller))
		send_request.pack(pady = 15)

		messages_frame = Frame(self)
		  
		self.my_msg.set("Type your messages here.")
		scrollbar = Scrollbar(messages_frame)  		
		self.msg_list = Listbox(messages_frame, height=15, width=80, yscrollcommand=scrollbar.set)
		scrollbar.pack(side=RIGHT, fill=Y)
		self.msg_list.pack(side=LEFT, fill=BOTH)
		self.msg_list.pack()
		messages_frame.pack()


		self.entry_field = Entry(self, textvariable=self.my_msg, bd = 10 )
		self.entry_field.bind('<FocusIn>', self.on_entry_click)
		self.entry_field.bind("<Return>", self.send)
		self.entry_field.pack(fill = X, padx = 160, pady = 5)
		send_button = Button(self, text="Send", command=self.send(controller,self.lora))
		send_button.pack()

		

	def on_entry_click(self,event):
		       
		global firstclic
		if firstclic:
			firstclic = False
			self.entry_field.delete(0, "end")
	
	def send2(self, controller):
		global game_script
		answer = tkMessageBox.askquestion('connection request by player, do you want to play Tic-Tac-Toe?')
		if answer == 'yes':
			self.send("$-$-$-cool$-$-$-")-----------------------------------------------
			game_script = 'client'
			controller.show_frame(PageFour)
			x = ttt_client(self.lora)
		        

	def send(self,controller):
		try:
			self.lora.set_mode(MODE.TX)
			msg = self.my_msg.get()
			self.msg_list.insert(END, m + ':' + msg)
			self.my_msg.set("")
			if len(msg)<48:
				if msg == '$-$-$-play$-$-$-':
					self.lora.start(msg)
					return
				msg = msg + ' '*(48 - len(msg))
			else:
				msg = msg[:48]

			msg = msg[::16]
			start_time = time.time()
			while (time.time() - start_time < 3): 
				for i in range(0,3):
           			self.lora.start(msg[i])-------------------------------------------------
           	self.prev_msg = msg
           	self.lora.set_mode(MODE.RXCONT) 

		except KeyboardInterrupt:
		    sys.stdout.flush()
		    print("Exit")
		    sys.stderr.write("KeyboardInterrupt\n")
		

	def send1(self, controller):
		global game_script 
		answer = tkMessageBox.askquestion('Request connection..','  ' + m.upper() + ' , do you want to send request to play Tic-Tac-Toe?')
		if answer == 'yes':
			self.my_msg.set("$-$-$-play$-$-$-")
			self.send(controller)-----------------------------------------------
			game_script = 'server'
			x = ttt_server(self.lora)
			controller.show_frame(PageThree)


	def receive(self,controller):
		try:
			self.lora.set_mode(MODE.RXCONT)
			message = self.lora.on_rx_done()
			if message == '$-$-$-cool$-$-$-':
				message = ''
				send2(controller)
			elif message == '!resend!':
				while (time.time() - start_time < 3): 
					for i in range(0,3):
           				self.lora.start(self.prev_msg[i])
			else:
				start_time = time.time()
				while time.time()-start_time < 3:
		    		message = message  + self.lora.on_rx_done()
		    	if len(message) < 48:
		    		self.lora.start("!resend!")
		    		return
		    	self.msg_list.insert(END, 'user : ' + message)	-----------------------------------------
		    	message = ''


		except KeyboardInterrupt:
		    sys.stdout.flush()
		    print("Exit")
		    sys.stderr.write("KeyboardInterrupt\n")
		finally:
		    sys.stdout.flush()
		    print("Exit")
		    lora.set_mode(MODE.SLEEP)
		BOARD.teardown()

	def onClosing(self,controller):
		self.my_msg.set("!quit!")
		self.send(controller)







class PageThree(Frame, mylora, PageTwo):
	global game_script
	def __init__(self, parent, controller):	

		
		controller.protocol("WM_DELETE_WINDOW", self.onClosing(controller))

		Frame.__init__(self, parent)

		label = Label(self, text="Waiting for reply...", fg = "Black", font=L_FONT)
		label.pack(pady=250,padx=10)

		send_button = Button(self, text="Back", command=lambda :controller.show_frame(PageTwo))
		send_button.pack()

		PageTwo.receive(self,controller)---------------------------------------------------------------------------------

		

	def onClosing(self, controller):
		controller.show_frame(PageTwo)



class PageFour(Frame):

	def __init__(self, parent, controller):	

		controller.protocol("WM_DELETE_WINDOW", self.onClosing(controller))

		Frame.__init__(self, parent)

		label = Label(self, text="Game Started!", fg = "Black", font=L_FONT)
		label.pack(pady=250,padx=10)

		send_button = Button(self, text="Back", command=lambda :controller.show_frame(PageTwo))
		send_button.pack()
		

	def onClosing(self, controller):
		controller.show_frame(PageTwo)




def main():
	try:
		app = Godsky()
		app.geometry("1200x700+350+150")

		app.mainloop()

	except:
		raise

	finally:
	    sys.stdout.flush()
	    print("Exit")
	    lora.set_mode(MODE.SLEEP)
		BOARD.teardown()

if __name__ == '__main__':
	main()