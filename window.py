from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext 
from change import dealwith
import tkinter.font as tf



#规则和例子
txt = '使用规则：1、在左边框框内输入你想要转调的简谱，再在下面选择原谱调性和目标的调性，点'\
        '击“开始转调”按钮进行转调，也可以“清空所有”来重置；\n\t 2、在小括号内表示降一个八度，在中'\
        '括号表示升一个八度，表示声一个半音就在数字前加一个#，括号不分中英文（转调后都为英文括号），'\
        '目前暂不支持#(123)、#[123]语义；\n\t 3、当前文本框每行最多输入60字符，超出字符自动换行，所以'\
        '为了美观，请自行整理谱子格式；\n\t 4、可以选中内容，在框框内进行ctrl+c和ctrl+v操作；\n\t'\
        ' 5、由于程序问题，输入谱子时候请尽量少输入*符号和一些错误的格式，避免报错。'

lizi = '''例如：《起风了》
#1(7)# 1(7)#1# 2#4# 2
#1(7)# 1(7)#1# 2#1(7# 5)
#1(7)# 1(7)#1# 2#4# 2 #1# 2#1(7)# 1
#1(7)# 1(7)#1# 2#4# 2 #1# 2#1(7# 5)
#2#1(7)# 1(7) #2#1(7)# 1(7)
(#4)#2#1(7)# 1(7)
(7)#1# 2(7) #5#4# 5 (7) #6#5#6
#6#5#6 #27【#1】7#6#5#4
#5#4# 5#4# 5#4#1# 4#2
(7)#1# 2(7) #5#4# 5 (7) #6#5#6
#6#5#6 #27【#1】7#6#5#4
~#5【#2#2】 #4# 5【#2#2】#4# 5

(7)#1# 2 #5#4 #5#4 #5#4
#1# 2 #5#4 #5#4 #5#4
#2#1(7# 5 7)#1(7# 5 7~)#23#2#1# 2
(7)#1# 2 #5#4 #5#4 #5#4
#1# 2 #5#4 #5#4 #5#4
#2#1(7# 5) #2#1(7# 5 77)
(#4# 5)#2#1(7# 5) #2#1(7# 577)

#1(7)# 1(7)#1# 2#4# 2
#1(7)# 1(7)#1# 2#1(7# 5)
#1(7)# 1(7)#1# 2#4# 2 #1# 2#1(7)# 1
#1(7)# 1(7)#1# 2#4# 2 #1# 2#1(7# 5)
#2#1(7)# 1(7) #2#1(7)# 1(7)
(#4)#2#1(7)# 1(7)

(7)#1# 2(7) #5#4# 5 (7) #6#5#6 #2
#6#5#6 #27【#1】7#6#5#4
#5#4# 5#4# 5#4#1# 4#2
(7)#1# 2(7) #5#4# 5 (7) #6#5#6 #2
#6#5#6 #27【#1】7#6#5#4
~#5【#2#2】 #4# 5【#2#2】#4# 5

(7)#1# 2 #5#4 #5#4 #5#4
#1# 2 #5#4 #5#4 #5#4
#2#1(7# 5 7)#1(7# 5 7~)#23#2#1# 2
(7)#1# 2 #5#4 #5#4 #5#4
#1# 2 #5#4 #5#4 #5#4
#2#1(7# 5) #2#1(7# 5 77)
（重复）
'''

class MyWindow():
    def __init__(self):
        ########################################################################
        #                             part one                                 #
        ########################################################################
        ############################
        #       窗口设计           #
        ############################
        win = Tk()
        win.title('转调器')
        win.geometry('1200x700')
        win.resizable(0,0) #防止用户调整尺寸

        widths = 57#输入/出文本框的大小，字符数
        heights = 30#行数
        ft = tf.Font(family='华文隶书',size=13)



        #####################
        #       开头的文字  #
        #####################
        frame1 = Frame(win)
        frame1.pack(fill=X)
        label1 = Label(frame1,text=txt,justify=LEFT)
        label1.pack(side=LEFT,anchor=N)#anchor为N，靠北（上）

        ########################################################################
        #                             part two                                 #
        ########################################################################

        ####################
        ##        输入框   #
        ####################
        frame2 = Frame(win)#第二部分：输入框和输出框
        frame2.pack(anchor=NW,padx=10,pady=10,side=LEFT)

        frame2_0 = Frame(frame2)
        frame2_0.pack(side=LEFT)
        self.text_in = scrolledtext.ScrolledText(frame2_0,width=widths,
                                                 height=heights,
                                                 font=ft)#输入框，设置长和高
        self.text_in.pack(fill=X)
        self.text_in.insert(INSERT,lizi)

        
        #self.text_in.config(xscrollcommand=scroll_x1.set,yscrollcommand=scroll_y1.set)
        ########################
        ##        原调性选择   #
        ########################
        Label(frame2_0,text='原调性：').pack(side=LEFT)

        number1 = StringVar()
        self.cmb1 = ttk.Combobox(frame2_0,width=10,textvariable=number1,
                                 state='readonly')#state设置只读
        self.cmb1.pack(side=LEFT)
        self.cmb1['values'] = [u"G", u"#G/Ab", u"A", u"#A/Bb", u"B", u"C",\
                          u"#C/Db", u"D", u"#D/Eb", u"E", u"F", u"#F"]
        self.cmb1.current(5)

        #########################
        ##      转调\清除按钮   #
        #########################
        frame2_1 = Frame(frame2)
        frame2_1.pack(side=LEFT)
        Button(frame2_1,text='开始转调=》',command=self.callback).pack(fill=X,padx=10)
        Button(frame2_1,text='清空所有',command=self.delete).pack(fill=X,padx=10,pady=10)

        ####################
        ##        输出框   #
        ####################
        frame2_2 = Frame(frame2)
        frame2_2.pack(side=LEFT)
        self.text_out = scrolledtext.ScrolledText(frame2_2,width=widths,height=heights,
                                                  font=ft)
        self.text_out.pack(fill=X)
        ########################
        ##        目标调性选择 #
        ########################
        Label(frame2_2,text='目标调性：').pack(side=LEFT)  
        number2 = StringVar()
        self.cmb2 = ttk.Combobox(frame2_2,width=10,textvariable=number2,
                                 state='readonly')
        self.cmb2.pack(side=LEFT)
        self.cmb2['values'] = [u"G", u"#G/Ab", u"A", u"#A/Bb", u"B", u"C", \
                          u"#C/Db", u"D", u"#D/Eb", u"E", u"F", u"#F"]
        self.cmb2.current(6)      
        
        win.mainloop()#不要忘记



    def callback(self):#转调时候调用的函数
        r = self.text_in.get('0.0',END)
        cha = self.cmb2.current() - self.cmb1.current()
        r = dealwith(r,cha)
        self.text_out.delete('0.0',END)
        self.text_out.insert(INSERT,r)
        return r
        #print(r)

    def delete(self):#清除函数
        self.text_in.delete('0.0',END)
        self.text_out.delete('0.0',END)
        #text_out.delete('0.0',END)


    #d = dealwith('342423',3)
    #mainloop()

if __name__ == '__main__':
    win = MyWindow()
