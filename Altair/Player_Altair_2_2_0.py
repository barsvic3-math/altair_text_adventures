from tkinter import *
from tkinter import font
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
import random as R
import copy


class Work_Canvas(object):
    def __init__(self, w, h):
        self.root = Tk()
        self.width = w
        self.height = h
        self.root.minsize(self.width,self.height)
        self.root.maxsize(self.width,self.height)

        self.root.title('Altair 2.2.0 Quest')

        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()




class Global_Storage(object):
    def __init__(self):
        with open('Scripts/Architecture.txt', 'r', encoding='utf-8') as file:
            file_text = file.read().splitlines()
            s = file_text[0][11:]
            width = int(s[:s.find('x')])
            height = int(s[s.find('x')+1:])
        self.Workplace = Work_Canvas(width, height)
        self.Global_Vars = {'__canvas_width':width, '__canvas_height':height,'__bg_image':False, '__bg':'white', '__indent_up':0, '__History':[]}
        self.Local_Vars = {}
        self.Buttons = []
        self.Images = []
        self.Global_Vars['__y'] = 0
        self.n_string = 0
        self.Shift = 0
        self.History = []
        self.stop = False


    def hex_to_rgb(self, hex_color):

      hex_color = hex_color.lstrip('#')
      r = int(hex_color[0:2], 16)
      g = int(hex_color[2:4], 16)
      b = int(hex_color[4:6], 16)
      return r, g, b
        

    def Decode_Code(self, s):
        new_s = ''
        n = 0
        while n <= len(s)-1:
            if s[n] == '#':
                ss = s[n:]
                ind = 0
                while ind < len(ss) and ss[ind] not in [' ', '.', '[', '/', '*', '+', '-', '>', '<', '=', ']', ')','(', ',', '%']:
                    ind+=1
                if ind < len(ss):
                    new_s+="self.Global_Vars['"+ss[1:ind]+"']"+ss[ind]
                else:
                    new_s+="self.Global_Vars['"+ss[1:]+"']"
                n += ind

            elif s[n] == '&':
                ss = s[n:]
                ind = 0
                while ind < len(ss) and ss[ind] not in [' ', '.', '[', '/', '*', '+', '-', '>', '<', '=', ']', ')', '(', ',', '%']:
                    ind+=1
                if ind < len(ss):
                    new_s+="self.Local_Vars['"+ss[1:ind]+"']"+ss[ind]
                else:
                    new_s+="self.Local_Vars['"+ss[1:]+"']"
                n += ind

            else:
                new_s+=s[n]
        
        
            n += 1

        return new_s

    def Decode_Text(self, s):
        new_s = ''
        n = 0

        while n <= len(s)-1:
            if s[n] in ['#', '&']:
                ss = s[n:]
                ind = 0
                while ind < len(ss) and ss[ind] not in [' ', '.', '[', '/', '*', '+', '-', '>', '<', '=', ']', ')','(', ',', '%']:
                    ind += 1
                new_s+=str(eval(self.Decode_Code(ss[:ind])))
                n+=ind-1

            else:
                new_s+=s[n]
            
            n+=1
        new_s.replace("~","#")
        return new_s

    def Import(self, prefix, name_of_file):
        with open(prefix+name_of_file+'.txt', 'r', encoding='utf-8') as file:
            file_text = file.read().splitlines()

        return file_text

    def Paste(self, text_file, inc, flag=0):
        if inc >= 0:
            for n, string in enumerate(text_file):
                if string != '':
                    k = 0
                    while string[k] == ' ':
                        k+=1
                    if string[k:] == '}':
                        flag -= 1
                    elif string[k:] == '{ --imm':
                        flag += 1
                    elif len(string[k:]) > 1+flag:
                        if string[k:k+1+flag] == '>'*(1+flag):
                            text_file[n] = string[:k+1+flag] + '>'*inc + string[k+1+flag:]
                        elif string[-1-flag:] == '>'*(1+flag):
                            text_file[n] = string[:] + '>'*inc
                        elif len(string[k:]) > 1+flag+2:
                            if string[-1-flag-2:] == '>'*(1+flag)+' {':
                                text_file[n] = string[:-2] + '>'*inc + ' {'
                                flag += 1
                            elif '>'*(1+flag)+' (' in string and ') {' in string:
                                index = string.find('>'*(1+flag)+' (')
                                text_file[n] = string[:index] + '>'*inc + string[index:]
                                flag += 1
                            elif '>'*(1+flag)+' (' in string and ')' in string:
                                index = string.find('>'*(1+flag)+' (')
                                text_file[n] = string[:index] + '>'*inc + string[index:]
                text_file[n] = 4*inc*' ' + text_file[n]
        else:
            for n, string in enumerate(text_file):
                if string != '':
                    k = 0
                    while string[k] == ' ':
                        k+=1
                    if string[k:] == '}':
                        flag -= 1
                    elif string[k:] == '{ --imm':
                        flag += 1
                    elif len(string[k:]) > 1+flag:
                        if string[k:k+1+flag] == '>'*(1+flag):
                            text_file[n] = string[:k+1+flag+inc] + string[k+1+flag:]
                        elif string[-1-flag:] == '>'*(1+flag):
                            text_file[n] = string[:inc]
                        elif len(string[k:]) > 1+flag+2:
                            if string[-1-flag-2:] == '>'*(1+flag)+' {':
                                text_file[n] = string[:-2+inc] + ' {'
                                flag += 1
                            elif '>'*(1+flag)+' (' in string and ') {' in string:
                                index = string.find('>'*(1+flag)+' (')
                                text_file[n] = string[:index] + string[index-inc:]
                                flag += 1
                            elif '>'*(1+flag)+' (' in string and ')' in string:
                                index = string.find('>'*(1+flag)+' (')
                                text_file[n] = string[:index] + '>'*inc + string[index-inc:]
                    text_file[n] = text_file[n][4*(-inc):]
        return text_file

    def Get_Args_Text(self, indent='L', anchor='L', colour=0, font=0, size=0, style=0):
        if colour == 0:
            colour=self.Local_Vars['__text_colour'].replace('~', '#')
        if font == 0:
            font=self.Local_Vars['__text_font']
        if size == 0:
            size=self.Local_Vars['__text_size']
        if style == 0:
            style=self.Local_Vars['__text_style']
        return indent, anchor, colour, '"'+font+'" '+str(size)+' '+style
            

    def Create_Text(self, s):
        xx = self.Local_Vars['__indent_left']
        anch = 'sw'
        if s[:3] == '! (' and ') !' in s:
            ind = s.find(') !')
            indent, anchor, colour, text_font = eval('self.Get_Args_Text('+self.Decode_Code(s[3:ind])+')')
            s = s[(ind+4):]
        else:
            indent, anchor, colour, text_font = self.Get_Args_Text()

        if indent == 'L':
            xx = self.Local_Vars['__indent_left']
        elif indent == 'R':
            xx = self.Global_Vars['__canvas_width'] - self.Local_Vars['__indent_right']
        else:
            xx = indent*(self.Global_Vars['__canvas_width'])

        if anchor == 'L':
            anch = 'sw'
        elif anchor == 'R':
            anch = 'se'
        else:
            anch = 's'
            
        s = self.Decode_Text(s)
        ss = ''
        ind = 0
        numb = 1
        if s!=None:
            while ind < len(s):       
                ss+=s[ind]
                if numb%self.Local_Vars['__text_length'] == 0 or ind == len(s)-1:
                    if ss[-1] != ' ':
                        if ind < len(s)-1:
                            checker = s[ind+1] != ' '
                        else:
                            checker = False
                        if checker:
                            while ss[-1] != ' ':
                                ss = ss[:-1]
                                ind-=1
                    while ss[0] == ' ':
                        ss = ss[1:]
                    self.Global_Vars['__y']+=self.Local_Vars['__text_shift']
                    self.Workplace.canvas.create_text(xx, self.Global_Vars['__y'],text=ss, font = text_font ,fill = colour, anchor = anch)
                    ss = ''
                    numb = 0
                ind += 1
                numb+=1

        if s == '':
            self.Global_Vars['__y']+=self.Local_Vars['__text_shift']

    def Button_Func(self, n_string, imm_tup_, flag_, sign_):
        new_file_text_ = copy.deepcopy(self.file_text)
        new_file_text_[n_string] =  4*flag_*' '+'B-Open>'+flag_*'>'+' {'
        if imm_tup_[1] > imm_tup_[0]:
            new_file_text_ = ['B-Open>'+' {'] + self.Paste(self.file_text[imm_tup_[0]+1:imm_tup_[1]], inc=-flag_, flag=flag_+1) + ['}'] + new_file_text_[:imm_tup_[0]] + new_file_text_[imm_tup_[1]+1:]
        self.n_string = 0
        self.Shift = 0
        self.stop = False
        self.Descript(new_file_text_, Replay=True, Cleaning=True, Starter=True)

    def Create_LB_Building(self, Place_, Font_, Style_, Size_ , Fg_, Bg_, Afg_, Abg_, H_, Relief_, sign_, where_, command_, n_str_, imm_tup_, flag_):
        if command_ == 'link':
            self.Buttons.append(Button(text = sign_, width = len(sign_)+2, height = H_, bg = Bg_.replace('~', '#'), fg = Fg_.replace('~', '#'), activebackground = Abg_.replace('~', '#'), activeforeground = Afg_.replace('~', '#'), relief = Relief_, font = '"'+Font_+'" '+str(Size_)+' '+Style_,command = lambda: self.Read(where_[:])))
        elif command_ == 'button':
            self.Buttons.append(Button(text = sign_, width = len(sign_)+2, height = H_, bg = Bg_.replace('~', '#'), fg = Fg_.replace('~', '#'), activebackground = Abg_.replace('~', '#'), activeforeground = Afg_.replace('~', '#'), relief = Relief_, font = '"'+Font_+'" '+str(Size_)+' '+Style_,command = lambda: self.Button_Func(n_str_, imm_tup_, flag_, sign_)))

        if Place_ == 'L':
            xx = 0
            anch = 'nw'
        elif Place_ == 'R':
            xx = self.Global_Vars['__canvas_width']
            anch = 'ne'
        else:
            xx = int(float(Place_)*self.Global_Vars['__canvas_width'])
            anch = 'n'
        self.Buttons[-1].place(x = xx, y = self.Global_Vars['__y'], anchor = anch)

    def Args_For_Link(self, indent = False, Font = False, Style = False, Size = False, Fg = False, Bg = False, Afg = False, Abg = False, H = False, Relief = False):

        if indent == False:
            indent=1/2
        if Font == False:
            Font=self.Local_Vars['__link_text_font']
        if Style == False:
            Style=self.Local_Vars['__link_text_style']
        if Size == False:
            Size=self.Local_Vars['__link_text_size']
        if Fg == False:
            Fg=self.Local_Vars['__link_fg']
        if Bg == False:
            Bg=self.Local_Vars['__link_bg']
        if Afg == False:
            Afg=self.Local_Vars['__link_activeforeground']
        if Abg == False:
            Abg=self.Local_Vars['__link_activebackground']
        if H == False:
            H=self.Local_Vars['__link_height']
        if Relief == False:
            Relief=self.Local_Vars['__link_relief']

        return indent, Font, Style, Size, Fg, Bg, Afg, Abg, H, Relief

    def Args_For_Button(self, indent = False, Font = False, Style = False, Size = False, Fg = False, Bg = False, Afg = False, Abg = False, H = False, Relief = False):

        if indent == False:
            indent=1/2
        if Font == False:
            Font=self.Local_Vars['__button_text_font']
        if Style == False:
            Style=self.Local_Vars['__button_text_style']
        if Size == False:
            Size=self.Local_Vars['__button_text_size']
        if Fg == False:
            Fg=self.Local_Vars['__button_fg']
        if Bg == False:
            Bg=self.Local_Vars['__button_bg']
        if Afg == False:
            Afg=self.Local_Vars['__button_activeforeground']
        if Abg == False:
            Abg=self.Local_Vars['__button_activebackground']
        if H == False:
            H=self.Local_Vars['__button_height']
        if Relief == False:
            Relief=self.Local_Vars['__button_relief']
            
        return indent, Font, Style, Size, Fg, Bg, Afg, Abg, H, Relief

    def Create_LB(self, s, commander, sign = '', where = '', n_str=0, flag_=0, imm_tup=(0,0)):

        indent, Font, Style, Size, Fg, Bg, Afg, Abg, H, Relief = eval('False,'*10)
        
        if commander == 'link':
            if s.count('(') > 1:
                s = s[(s.find('(')+1):]
        
                s_begin = s[:s.find(')')]
                indent, Font, Style, Size, Fg, Bg, Afg, Abg, H, Relief = eval('self.Args_For_Link('+self.Decode_Code(s_begin)+')')
                s = s[s.find(')')+1:]
            else:
                indent, Font, Style, Size, Fg, Bg, Afg, Abg, H, Relief = self.Args_For_Link()

            if s.find('->') != -1:
        
                s = s[(s.find('(')+1):]
                sign = eval(self.Decode_Code(s[:s.find(' -> ')]))
        
                s = s[(s.find(' -> ')+4):]
                where = eval(self.Decode_Code(s[:s.find(')')]))
            else:
                s = s[(s.find('(')+1):]
                where = eval(self.Decode_Code(s[:s.find(')')]))
                sign = where
                
        elif commander == 'button':

            if s.count('(') > 0 and s.count(')') > 0:
                s = s[(s.find('(')+1):]
        
                s_begin = s[:s.find(')')]
                indent, Font, Style, Size, Fg, Bg, Afg, Abg, H, Relief = eval('self.Args_For_Button('+self.Decode_Code(s_begin)+')')
                s = s[s.find(')')+1:]
            else:
                s_begin = ''
                indent, Font, Style, Size, Fg, Bg, Afg, Abg, H, Relief = eval('self.Args_For_Button('+self.Decode_Code(s_begin)+')')
        
        self.Create_LB_Building(indent, Font, Style, Size, Fg, Bg, Afg, Abg, H, Relief, sign, where, commander, n_str, imm_tup, flag_)


    def Get_Args_For(self, start=0, end=1, step=1):
        return start, end, step

    def Get_Args_Img(self, y, place=1/2):
        return place, y

    def Get_Args_Fig_1d(self, coordinates, fill, width, y, a=1):
        return coordinates, fill, width, a, y

    def Get_Args_Fig_2d(self, coordinates, fill, outline, width, y, a=1):
        return coordinates, fill, outline, width, a, y


    def next_line(self, file_text, flag=0, Show_option=True, Replay=False, Cleaning=False, Starter = False, Loop = False):
        if not self.stop:
            self.n_string += 1
            if len(file_text) > 1:
                file_text = file_text[1:]
                self.Descript(file_text, flag, Show_option, Replay, False, False, Loop)


    def Descript(self, file_text, flag=0, Show_option=True, Replay=False, Cleaning=False, Starter = False, Loop = False):
        if Starter:
            self.file_text = file_text[:]

        if Cleaning:
            self.Global_Vars['__y'] = self.Global_Vars['__indent_up']
            self.Workplace.canvas.delete('all')
            for b in self.Buttons:
                b.destroy()
            self.Buttons = []
            self.Images = []
            if self.Global_Vars['__bg_image'] == False:
                col = self.Global_Vars['__bg']
                col = col.replace('~', '#')
                self.Workplace.canvas.create_rectangle(0, 0, self.Global_Vars['__canvas_width'], self.Global_Vars['__canvas_height'], fill = col, outline = col, width = 1)
            else:
                backg = ImageTk.PhotoImage(file="Images/"+self.Global_Vars['__bg_image'])
                self.Workplace.canvas.background = backg
                self.Workplace.canvas.create_image(self.Global_Vars['__canvas_width']//2, self.Global_Vars['__canvas_height']//2, image = backg, anchor = 'center')

        string = file_text[0]
        string = string[4*flag:]
        if string[:1+flag] == '>'+flag*'>':
            if (not Replay and string[1+flag:9+flag] != ' --stat ') or string[1+flag:9+flag] == ' --loop ' or Loop:
                if '--loop' not in string and '--stat' not in string:
                    s = string.find(' ')
                else:
                    s = string[:2+flag].find(' ') + flag + 2
                exec(self.Decode_Code(string[s+1:]))
                
            self.next_line(file_text, flag, Show_option, Replay, False, False, Loop)

        elif string[:2] == 'If':
            k = 1
            while file_text[k][4*flag:] != '}':
                k+=1
                
            if eval(self.Decode_Code(string[string.find(':')+1:string.find(' >'+flag*'>'+' {')])):
                if (not Loop and string[2:10] != ' --loop ') or string[2:10] == ' --stat ':
                    self.file_text[self.n_string] = 4*flag*' ' + 'If: True >'+flag*'>'+' {'
                flag_new = flag+1
                self.n_string += 1
                if k > 1:
                    self.Descript(file_text[1:k], flag_new, Show_option, Replay, False, False, Loop)
                file_text = file_text[k:]
                

                if len(file_text) > 1 and not self.stop:
                    if file_text[1][4*flag:] == 'Else>'+flag*'>'+' {':
                        k = 2
                        while file_text[k][4*flag:] != '}':
                            k+=1
                        file_text = file_text[k:]
                        self.n_string += k
                        
            elif len(file_text) > k+1:    
                if file_text[k+1][4*flag:] == 'Else>'+flag*'>'+' {':
                    if (not Loop and string[2:10] != ' --loop ') or string[2:10] == ' --stat ':
                        self.file_text[self.n_string] = 4*flag*' ' + 'If: False >'+flag*'>'+' {'
                    self.n_string+=k+1
                    file_text = file_text[k+1:]
                    k = 1
                    while file_text[k][4*flag:] != '}':
                        k+=1
                    flag_new = flag+1
                    self.n_string += 1
                    if k > 1:
                        self.Descript(file_text[1:k], flag_new, Show_option, Replay, False, False, Loop)
                    file_text = file_text[k:]
                   
                
                else:
                    if (not Loop and string[2:10] != ' --loop ') or string[2:10] == ' --stat ':
                        self.file_text[self.n_string] = 4*flag*' ' + 'If: False >'+flag*'>'+' {'
                    file_text = file_text[k:]
                    self.n_string += k
                    
                    
            else:
                if (not Loop and string[2:10] != ' --loop ') or string[2:10] == ' --stat ':
                    self.file_text[self.n_string] = 4*flag*' ' + 'If: False >'+flag*'>'+' {'
                file_text = file_text[k:]
                self.n_string += k
                
            self.next_line(file_text, flag, Show_option, Replay, False, False, Loop)


        elif string[:5+flag] == 'Link>'+ flag*'>' and Show_option:
            self.Create_LB(string[5+flag:], 'link')
            self.Global_Vars['__y'] += self.Local_Vars['__link_shift']
            
            self.next_line(file_text, flag, Show_option, Replay, False, False, Loop)


        elif string[:3] == 'B:='and Show_option:
            signer = eval(self.Decode_Code(string[3:string.find('>')]))
            n = self.n_string
            k = 1
            while file_text[k][4*flag:] != '}':
                k+=1
            kk = k + 1
            k_shift = k
            if len(file_text) > k+1:
                if file_text[k+1][4*flag:] == '{ --imm':
                    while file_text[kk][4*flag:] != '}':
                        kk+=1
                    k_shift = kk
            self.Create_LB(string[5+flag:], 'button', signer, n_str=n, imm_tup=(n+k+1, n+kk), flag_=flag)
            self.Global_Vars['__y'] += self.Local_Vars['__button_shift']
            file_text = file_text[k_shift:]
            self.n_string+=k_shift
            self.next_line(file_text, flag, Show_option, Replay, False, False, Loop)

        elif string[:6] == 'B-Open' and Show_option:
            self.file_text[self.n_string]=4*flag*' '+'B-Close>'+flag*'>'+' {'
            k = 1
            while file_text[k][4*flag:] != '}':
                k+=1
            flag_new = flag+1
            self.n_string += 1
            if k > 1:
                self.Descript(file_text[1:k], flag_new, Show_option, False, False, False, Loop)
            file_text = file_text[k:]            
            self.next_line(file_text, flag, Show_option, Replay, False, False, Loop)

        elif string[:7] == 'B-Close' and Show_option:
            k = 1
            while file_text[k][4*flag:] != '}':
                k+=1
            flag_new = flag+1
            self.n_string += 1
            if k > 1:
                self.Descript(file_text[1:k], flag_new, Show_option, Replay, False, False, False)
            file_text = file_text[k:]
            
            self.next_line(file_text, flag, Show_option, Replay, False, False, Loop)

        elif string[:] == 'Loop>'+'>'*flag+' {' and Show_option:
            k = 1
            while file_text[k][4*flag:] != '}':
                k+=1
            flag_new = flag+1
            self.n_string += 1
            self.Descript(file_text[1:k], flag_new, Show_option, Replay, False, False, True)
            file_text = file_text[k:]
            
            self.next_line(file_text, flag, Show_option, Replay, False, False, Loop)


        elif string[:] == 'Stat>'+'>'*flag+' {' and Show_option:
            k = 1
            while file_text[k][4*flag:] != '}':
                k+=1
            
            self.file_text[self.n_string]=4*flag*' '+'Stat-Close>'+flag*'>'+' {'
            flag_new = flag+1
            self.n_string += 1
            self.Descript(file_text[1:k], flag_new, Show_option, Replay, False, False, Loop)
            file_text = file_text[k:]
            
            self.next_line(file_text, flag, Show_option, Replay, False, False, Loop)
            

        elif string[:] == 'Stat-Close>'+'>'*flag+' {' and Show_option:
            k = 1
            while file_text[k][4*flag:] != '}':
                k+=1
            flag_new = flag+1
            self.n_string += 1
            self.Descript(file_text[1:k], flag_new, Show_option, Replay, False, False, False)
            file_text = file_text[k:]
            
            self.next_line(file_text, flag, Show_option, Replay, False, False, Loop)
            #self.n_string += 1
            
            

        elif string[:6] == 'Img:= ' and Show_option:
            sign = eval(self.Decode_Code(string[6:string.find('>'*(flag+1))-1]))
            self.Images.append(ImageTk.PhotoImage(file="Images/"+sign))
            place, yy = eval('self.Get_Args_Img('+self.Decode_Code(string[string.find('(')+1:string.find(')')])+')')
            if place == 'L':
                xx = self.Local_Vars['__indent_left']
                anch = 'nw'
            elif place == 'R':
                xx = self.Global_Vars['__canvas_width'] - self.Local_Vars['__indent_right']
                anch = 'ne'
            else:
                place = float(place)
                xx = place*(self.Global_Vars['__canvas_width'])
                anch = 'n'

            self.Workplace.canvas.foreground = self.Images[-1]
            self.Workplace.canvas.create_image(xx, self.Global_Vars['__y'], image = self.Images[-1], anchor = anch)
            self.Global_Vars['__y'] += yy
            self.next_line(file_text, flag, Show_option, Replay, False, False, Loop)

       
        elif string[:5] == 'Sp:= ' and Show_option:
            num = string[5:string.find('>'*(flag+1))-1]
            pix = eval(self.Decode_Code(num))

            self.Global_Vars['__y'] += pix
            self.next_line(file_text, flag, Show_option, Replay, False, False, Loop)
                
        elif string[:8] == 'Script:=':
            name_of_file = eval(self.Decode_Code(string[8:string.find('>')]))
            new = self.Paste(self.Import('Scripts/', name_of_file), flag)
            self.file_text = self.file_text[:self.n_string] + new[:] + self.file_text[self.n_string+1:]
            file_text = new[:] + file_text[1:]
            self.Descript(file_text, flag, Show_option, Replay, False, False, Loop)

        elif string[:9] == 'Display:=':
            name_of_file = eval(self.Decode_Code(string[8:string.find('>')]))
            new = self.Paste(self.Import('Passages/', name_of_file), inc, flag)
            
            self.file_text = self.file_text[:self.n_string] + new[:] + self.file_text[self.n_string+1:]
            file_text = new[:] + file_text[1:]
            self.Descript(file_text, flag, Show_option, Replay, False, False, Loop)

        elif string[:6] == 'While:' and string[-3-flag:] == '>'*(1+flag)+' {':
            k = 1
            while file_text[k][4*flag:] != '}':
                k+=1
            self.file_text = self.file_text[:self.n_string+1] + self.file_text[self.n_string+k:]
            self.file_text[self.n_string] = 4*flag*' '+'If: True >'+flag*'>'+' {'
            self.n_string += 1
            while eval(self.Decode_Code(string[6:string.find('>')])) and not self.stop:
                self.file_text = self.file_text[:self.n_string] + file_text[1:k] + self.file_text[self.n_string:]
                flag_new = flag+1
                self.Descript(file_text[1:k], flag_new, Show_option, Replay, False, False, Loop)
            file_text = file_text[k:]            
            self.next_line(file_text, flag, Show_option, Replay, False, False, Loop)
            
        elif string[:15] == 'For &index in (' and string[-5-flag:] == ') '+'>'*(1+flag)+' {':
            start, end, step = eval('self.Get_Args_For('+self.Decode_Code(string[15:-5-flag])+')')
            init_strings = []
            init_strings.append(4*flag*' '+'>'*(flag+1)+' '+'&index = '+str(start))
            init_strings.append(4*flag*' '+'While: &index < '+str(end)+' '+'>'*(flag+1)+' {')
            init_strings.append(4*(flag+1)*' '+(flag+2)*'>'+' &index += '+str(step))
            k = 1
            while file_text[k][4*flag:] != '}':
                k+=1
            self.file_text = self.file_text[:self.n_string]+init_strings[:2]+self.file_text[self.n_string+1:self.n_string+k]+init_strings[2:]+self.file_text[self.n_string+k:]
            file_text = self.file_text[self.n_string:]
            self.Descript(file_text, flag, Show_option, Replay, False, False, Loop)

        elif string[:5] == 'Fig:=' and '>'*(1+flag) in string:
            fig_type = eval(self.Decode_Code(string[6:string.find('>')]))
            if fig_type  == 'rectangle':
                coordinates, fill, outline, width, a, yy = eval('self.Get_Args_Fig_2d('+self.Decode_Code(string[string.find('(')+1:-1])+')')
                img = Image.new('RGBA', (coordinates[2] - coordinates[0], coordinates[3] - coordinates[1]), None)
                draw = ImageDraw.Draw(img)
                rect_coords = [0,0, coordinates[2] - coordinates[0], coordinates[3] - coordinates[1]]
                rect_color = self.hex_to_rgb(fill[1:])
                rect_color_out = self.hex_to_rgb(outline[1:])
                a = int(a*255)
                draw.rectangle(rect_coords, fill=(rect_color[0], rect_color[1], rect_color[2], a), outline=(rect_color_out[0], rect_color_out[1], rect_color_out[2], a), width=width)
                self.Images.append(ImageTk.PhotoImage(img))
                self.Workplace.canvas.create_image(coordinates[0], self.Global_Vars['__y'] + coordinates[1], image = self.Images[-1], anchor = 'nw')

            elif fig_type  == 'ellipse':
                coordinates, fill, outline, width, a, yy = eval('self.Get_Args_Fig_2d('+self.Decode_Code(string[string.find('(')+1:-1])+')')
                img = Image.new('RGBA', (coordinates[2] - coordinates[0], coordinates[3] - coordinates[1]), None)
                draw = ImageDraw.Draw(img)
                rect_coords = [0,0, coordinates[2] - coordinates[0], coordinates[3] - coordinates[1]]
                rect_color = self.hex_to_rgb(fill[1:])
                rect_color_out = self.hex_to_rgb(outline[1:])
                a = int(a*255)
                draw.ellipse(rect_coords, fill=(rect_color[0], rect_color[1], rect_color[2], a), outline=(rect_color_out[0], rect_color_out[1], rect_color_out[2], a), width=width)
                self.Images.append(ImageTk.PhotoImage(img))
                self.Workplace.canvas.create_image(coordinates[0], self.Global_Vars['__y'] + coordinates[1], image = self.Images[-1], anchor = 'nw')

            elif fig_type  == 'line':
                coordinates, fill, width, a, yy = eval('self.Get_Args_Fig_1d('+self.Decode_Code(string[string.find('(')+1:-1])+')')
                img = Image.new('RGBA', (coordinates[2] - coordinates[0], coordinates[3] - coordinates[1]), None)
                draw = ImageDraw.Draw(img)
                rect_coords = [0,0, coordinates[2] - coordinates[0], coordinates[3] - coordinates[1]]
                rect_color = self.hex_to_rgb(fill[1:])
                a = int(a*255)
                draw.line(rect_coords, fill=(rect_color[0], rect_color[1], rect_color[2], a), width=width)
                self.Images.append(ImageTk.PhotoImage(img))
                self.Workplace.canvas.create_image(coordinates[0], self.Global_Vars['__y'] + coordinates[1], image = self.Images[-1], anchor = 'nw')

            elif fig_type  == 'polygon':
                coordinates, fill, outline, width, a, yy = eval('self.Get_Args_Fig_2d('+self.Decode_Code(string[string.find('(')+1:-1])+')')
                x_coords = [coordinates[2*i] for i in range(len(coordinates)//2)]
                y_coords = [coordinates[2*i + 1] for i in range(len(coordinates)//2)]
                img = Image.new('RGBA', (max(x_coords) - min(x_coords), max(y_coords) - min(y_coords)), None)
                draw = ImageDraw.Draw(img)
                polygon_coords = [x_coords[i//2] - min(x_coords) if i%2==0 else y_coords[i//2] - min(y_coords) for i in range(len(coordinates))]
                polygon_color = self.hex_to_rgb(fill[1:])
                polygon_color_out = self.hex_to_rgb(outline[1:])
                a = int(a*255)
                draw.polygon(polygon_coords, fill=(polygon_color[0], polygon_color[1], polygon_color[2], a), outline=(polygon_color_out[0], polygon_color_out[1], polygon_color_out[2], a), width=width)
                self.Images.append(ImageTk.PhotoImage(img))
                self.Workplace.canvas.create_image(min(x_coords), self.Global_Vars['__y'] + min(y_coords), image = self.Images[-1], anchor = 'nw')
             
                    
            self.Global_Vars['__y'] += yy
            self.next_line(file_text, flag, Show_option, Replay, False, False, Loop)
                
            

        elif string[:6] == 'Undo:=' and string[-1-flag:] == '>'*(1+flag):
            number_back = eval(self.Decode_Code(string[6:-1-flag]))
            name_of_passage = self.Global_Vars['__History'][number_back]
            self.Global_Vars = copy.deepcopy(self.History[number_back])
            self.History = self.History[:number_back]
            self.Read(name_of_passage)
            self.stop = True

        elif Show_option:
            self.Create_Text(string)
            self.next_line(file_text, flag, Show_option, Replay, False, False, Loop)

        else:
             self.next_line(file_text, flag, Show_option, Replay, False, False, Loop)
            
            
                    

    def Read(self, name_of_file, prefix='Passages/', show_option=True, new_passage = True, Cleaning = True, Replay = False):
        self.stop = False
        if Cleaning:
            self.Workplace.canvas.delete('all')
            for b in self.Buttons:
                b.destroy()
            self.Buttons = []
            self.Images = []
            self.Global_Vars['__y'] = self.Global_Vars['__indent_up']
            self.n_string = 0
            self.Shift = 0
                
        if new_passage and show_option:
            self.Local_Vars = copy.deepcopy(self.Global_Vars)
            self.History += [copy.deepcopy(self.Global_Vars)]
            self.Global_Vars['__History'] += [name_of_file]

            if self.Global_Vars['__bg_image'] == False:
                col = self.Global_Vars['__bg']
                col = col.replace('~', '#')
                self.Workplace.canvas.create_rectangle(0, 0, self.Global_Vars['__canvas_width'], self.Global_Vars['__canvas_height'], fill = col, outline = col, width = 1)
            else:
                backg = ImageTk.PhotoImage(file="Images/"+self.Global_Vars['__bg_image'])
                self.Workplace.canvas.background = backg
                self.Workplace.canvas.create_image(self.Global_Vars['__canvas_width']//2, self.Global_Vars['__canvas_height']//2, image = backg, anchor = 'center')

        with open(prefix+name_of_file+'.txt', 'r', encoding='utf-8') as file:
            self.file_text = file.read().splitlines()
            self.Descript(self.file_text[:], 0, show_option, Replay, Cleaning = bool(Cleaning))



MetaSpace = Global_Storage()

MetaSpace.Read('StyleSheet', 'Scripts/', False)
MetaSpace.Read('Start')

MetaSpace.Workplace.root.mainloop()
        
