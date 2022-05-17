from tkinter import *
from tkinter import ttk,filedialog,messagebox
import os
from PIL import Image,ImageTk,ImageEnhance
import cv2
import numpy as np

# Applcation Class
class Application:

    def __init__(self):
        self.title = "Filter"
        self.IMG_ALLOWED = [".png",".jpg",".jpeg"]
        self.LISTS = []
        self.original_img = ""
        self.filter_img = ""
        self.thumbnail = (1000,700)
        self.filters_allow = ["Default","Red","Green","Blue","Yellow","Aqua","Pink","Bright","Sharphen","Blur"]
        pass

    def User_Interface(self,*args):
        """This method creates the GUI(Graphical User Interface)"""
        self.root = Tk()
        self.root.title(self.title)
        self.root.columnconfigure(0,weight=1)
        self.root.rowconfigure(1,weight=1)
        self.root.config(bg="#292929")
        self.root.state("zoomed")

        # Styles
        self.STYLE = ttk.Style()
        self.STYLE.theme_use("winnative")
        self.STYLE.configure("TNotebook",background="#292929")
        self.STYLE.configure("TNotebook.Tab",font=("arial",13,"bold"),background="yellow")
        # Frame 1
        self.F1 = Frame(self.root,borderwidth=1,relief=SOLID,bg="#292929")
        self.F1.columnconfigure(2,weight=1)
        # Open Image
        Button(self.F1,text="Open Image",bg="yellow",fg="black",border=1,relief=SOLID,font=("arial",13,"bold"),cursor="hand2",command=self.Open_Image_FUNC).grid(row=0,column=0,padx=2,pady=2,sticky="nswe")

        # Images
        Label(self.F1,text="Image:",bg="#292929",fg="white",font=("arial",13,"bold")).grid(row=0,column=1,padx=2,pady=2,sticky="nswe")

        self.Img_List = StringVar()
        self.Img_List_Combo = ttk.Combobox(self.F1,font=("arial",13,"bold"),state=DISABLED,textvariable=self.Img_List)
        self.Img_List_Combo.grid(row=0,column=2,padx=2,pady=2,sticky="nswe")

        # Filters
        Label(self.F1,text="Filter:",bg="#292929",fg="white",font=("arial",13,"bold")).grid(row=0,column=3,padx=2,pady=2,sticky="nswe")

        self.Filter_List = StringVar()
        self.Filter_List_Combo = ttk.Combobox(self.F1,font=("arial",13,"bold"),state=DISABLED,textvariable=self.Filter_List)
        self.Filter_List_Combo.grid(row=0,column=4,padx=2,pady=2,sticky="nswe")
        self.Filter_List_Combo["values"] = self.filters_allow
        self.Filter_List_Combo.set("Default")

        # Save Image
        Button(self.F1,text="Save Image",bg="yellow",fg="black",border=1,relief=SOLID,font=("arial",13,"bold"),cursor="hand2",command=self.Save_Filter_Image_FUNC).grid(row=0,column=5,padx=2,pady=2,sticky="nswe")

        self.F1.grid(row=0,column=0,padx=1,pady=1,sticky="nswe")

        # Note Book
        self.F2 = ttk.Notebook(self.root)

        # Original Image
        self.Org_Img_Label = Label(self.F2,bg="#1f1f1f",text="There is no Image",fg="yellow",font=("arial",20,"bold"))
        self.Org_Img_Label.pack(fill=BOTH,expand=True)

        # Filtered Image
        self.Filter_Img_Label = Label(self.F2,bg="#1f1f1f",text="There is no Image",fg="yellow",font=("arial",20,"bold"))
        self.Filter_Img_Label.pack(fill=BOTH,expand=True)

        self.F2.add(self.Org_Img_Label,text="Original Image",padding=(-2,-2,-3,-3))
        self.F2.add(self.Filter_Img_Label,text="Filter Image",padding=(-2,-2,-3,-3))
        self.F2.grid(row=1,column=0,padx=2,pady=2,sticky="nswe")

        self.Img_List_Combo.bind("<<ComboboxSelected>>",self.Image_Change_Filter_FUNC)
        self.Filter_List_Combo.bind("<<ComboboxSelected>>",self.Image_Change_Filter_FUNC)
        self.root.mainloop()
        pass

    def Open_Image_FUNC(self,*args):
        """This method is used to open one or multiple images"""
        files = filedialog.askopenfilenames(title="Open Image")
        if files:
            for i in files:
                if os.path.splitext(os.path.basename(i))[1].lower() in self.IMG_ALLOWED and i not in self.LISTS:
                    self.LISTS.append(i)
            if len(self.LISTS):
                self.Img_List_Combo["values"] = self.LISTS
                self.Img_List_Combo.set(self.LISTS[0])
                self.Filter_List_Combo.config(state="readonly")
                self.Img_List_Combo.config(state="readonly")

                self.original_img = Image.open(self.Img_List_Combo.get())
                self.thumbnail = (self.Org_Img_Label.winfo_width()-10,self.Org_Img_Label.winfo_height()-10)
                self.filter_img = np.array(self.original_img)
                img = self.original_img.copy()
                img.thumbnail(self.thumbnail)
                img = ImageTk.PhotoImage(img)
                self.Org_Img_Label.config(image=img)
                self.Org_Img_Label.image = img

                self.Filter_Img_Label.config(image=img)
                self.Filter_Img_Label.image = img
        pass

    def Image_Change_Filter_FUNC(self,*args):
        """The method which changes the filter"""
        x = self.Filter_List_Combo.get()
        self.original_img = Image.open(self.Img_List_Combo.get())
        self.filter_img = np.array(self.original_img)
        try:
            self.filter_img = Image_Process.Image_Process_FUNC(self.filter_img,x)

            img = self.original_img.copy()
            img.thumbnail(self.thumbnail)
            img = ImageTk.PhotoImage(img)
            self.Org_Img_Label.config(image=img)
            self.Org_Img_Label.image = img

            self.filter_img = Image.fromarray(self.filter_img)
            imgfilter = self.filter_img.copy()
            imgfilter.thumbnail(self.thumbnail)
            imgfilter = ImageTk.PhotoImage(imgfilter)
            self.Filter_Img_Label.config(image=imgfilter)
            self.Filter_Img_Label.image = imgfilter
        except:
            self.filter_img = self.original_img.copy()
            imgfilter = self.filter_img.copy()
            imgfilter.thumbnail(self.thumbnail)
            imgfilter = ImageTk.PhotoImage(imgfilter)
            self.Filter_Img_Label.config(image=imgfilter)
            self.Filter_Img_Label.image = imgfilter
        pass

    def Save_Filter_Image_FUNC(self,*args):
        """The Method which saves the filter image"""
        file_loc = filedialog.asksaveasfilename(title="Save File",defaultextension="jpg",filetypes=[("JPG Image","*.jpg"),("PNG Image","*.png")])
        if file_loc:
            os.chdir(os.path.dirname(file_loc))
            self.filter_img.save(f"{os.path.basename(file_loc)}")
            messagebox.showinfo("Successful",f"{file_loc} has been save")
        pass
    pass

# Image Processing Class
class Image_Process:

    def Image_Process_FUNC(img,txt):
        try:
            if txt == "Default":
                return img

            if txt == "Red":
                b,g,r=cv2.split(img)
                # creating a zero matrix image
                zeros=np.zeros(img.shape[:2],dtype="uint8")
                return cv2.merge([r,zeros,zeros])

            if txt == "Green":
                b,g,r=cv2.split(img)
                # creating a zero matrix image
                zeros=np.zeros(img.shape[:2],dtype="uint8")
                return cv2.merge([zeros,g,zeros])

            if txt == "Blue":
                b,g,r=cv2.split(img)
                # creating a zero matrix image
                zeros=np.zeros(img.shape[:2],dtype="uint8")
                return cv2.merge([zeros,zeros,b])

            if txt == "Yellow":
                b,g,r=cv2.split(img)
                # creating a zero matrix image
                zeros=np.zeros(img.shape[:2],dtype="uint8")
                return cv2.merge([b,b,zeros])

            if txt == "Aqua":
                b,g,r=cv2.split(img)
                # creating a zero matrix image
                zeros=np.zeros(img.shape[:2],dtype="uint8")
                return cv2.merge([zeros,g,g])

            if txt == "Pink":
                b,g,r=cv2.split(img)
                # creating a zero matrix image
                zeros=np.zeros(img.shape[:2],dtype="uint8")
                return cv2.merge([r,zeros,r])
            
            if txt == "Bright":
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                h, s, v = cv2.split(hsv)

                lim = 255 - 50
                v[v > lim] = 255
                v[v <= lim] = 50+v[v <= lim]

                final_hsv = cv2.merge((h, s, v))
                imgbright = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
                return imgbright

            if txt == "Sharphen":
                img = Image.fromarray(img)
                img = ImageEnhance.Sharpness(img).enhance(3)
                return np.array(img)

            if txt == "Blur":
                return cv2.medianBlur(img,3)

            return None
        except Exception as e:
            messagebox.showerror("Error",f"{e}")
    pass

if __name__ == "__main__":
    Application().User_Interface()