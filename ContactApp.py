import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.actionbar import ActionBar ,ActionView, ActionPrevious, ActionButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
import json
kv = Builder.load_file ("contactApp.kv") #this import the Gui kv file 


class ContactScreen (Widget) :
    def __init__ (self,**kwargs):
        super().__init__(**kwargs)
        self.names = {}
        self.load_contact()
        #self.ids.yea.add_widget (self.action_bar)
        
    def load_contact(self) :
        try :
                 with open ("database.json","r+") as file :
                    self.names = json.load(file)
        except (FileNotFoundError,json.JSONDecodeError) :
                with open ("database.json","x") as file :
                    self.names = {"Bulus Hamnu": "+234 9068556962"}
                    json.dump (self.names,file)
             
                with open ("database.json","r+") as file :
                     self.names = json.load (file)               
                 
        scroll_list = self.ids.Contactscroll
        for name,number in self.names.items() :
            contact = Label (text = "{} : {}".format(name,number))
            contact.font_size = 40
            scroll_list.add_widget (contact)
            
    def reload (self)  :
        with open ("database.json","r+") as file :
                    self.names = json.load(file)
        scroll_list = self.ids.Contactscroll
        scroll_list.clear_widgets()
        for name,number in self.names.items() :
            contact = Label (text = "{} : {}".format(name,number))
            contact.font_size = 40
            scroll_list.add_widget (contact)
             
    def show_add_popup (self) :
            add_pop = Addcontact ()
            popup_window1 = Popup (title = "Add Contacts", content = add_pop, size_hint = (None,None) , size = (700,700) )
            popup_window1.open()    
    #the show_remove popup display a popup window where the user can remove a new number from the database
 
    def show_remove_popup (self) :
            remove_pop = Removecontact ()
            popup_windom2 = Popup (title = "Remove Contacts", content = remove_pop, size_hint = (None,None) , size = (700,700) )
            popup_windom2.open()    
       


#this class hold the add_contact pop up window Gui and it func to save new number to the database
class Addcontact (BoxLayout) :
    def __init__ (self,**kwargs):
        super().__init__(**kwargs)
        self.db_instance = ContactScreen ()
#the save_contact func save the number add to the file after the update it then call the load funct to load it to the scroll view again        
    def save_contact (self):
              
        self.db_instance.names [self.ids.addname.text] = self.ids.addnumber.text
        self.ids.addname.text = ""
        self.ids.addnumber.text = ""
        with open ("database.json","w") as file :
            json.dump (self.db_instance.names,file, indent = 4)
        self.db_instance.reload()
        

#this class hold the removecontact pop up window Gui and it func to remove any number from the database   
class Removecontact (BoxLayout) :
    def __init__ (self,**kwargs):
        super().__init__(**kwargs)
        self.remove_name = self.ids.removename.text
        self.remove_number = self.ids.removenumber.text
        self.db_instance = ContactScreen ()
#the delete_contact func delete the number add to the file after the update it then call the load funct to load it to the scroll view again         
    def delete_contact (self):
        key = self.ids.removename.text   
        del self.db_instance.names [key] 
        self.ids.removename.text = ""
        self.ids.removenumber.text = ""
        with open ("database.json","w+") as file :
            json.dump (self.db_instance.names,file)
        self.db_instance.reload()


class ContactApp (App) :
    title = 'Contact App'
    def build(self) :
        return ContactScreen ()

if __name__ == "__main__" :
    ContactApp().run()
    
    