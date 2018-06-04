# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivymd.textfields import MDTextField
from kivymd.bottomsheet import MDListBottomSheet, MDGridBottomSheet
from kivymd.button import MDIconButton
from kivymd.date_picker import MDDatePicker
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivymd.list import ILeftBody, ILeftBodyTouch, IRightBodyTouch, BaseListItem
from kivymd.material_resources import DEVICE_TYPE
from kivymd.navigationdrawer import MDNavigationDrawer, NavigationDrawerHeaderBase
from kivymd.selectioncontrols import MDCheckbox
from kivymd.snackbar import Snackbar
from kivymd.theming import ThemeManager
from kivymd.toolbar import Toolbar
from kivy.utils import get_color_from_hex
from kivymd.color_definitions import colors
import sqlite3
import re
from predict_modul import *
from kivymd.time_picker import MDTimePicker

main_widget_kv = '''
#:import Toolbar kivymd.toolbar.Toolbar
#:import ThemeManager kivymd.theming.ThemeManager
#:import MDNavigationDrawer kivymd.navigationdrawer.MDNavigationDrawer
#:import NavigationLayout kivymd.navigationdrawer.NavigationLayout
#:import NavigationDrawerDivider kivymd.navigationdrawer.NavigationDrawerDivider
#:import NavigationDrawerToolbar kivymd.navigationdrawer.NavigationDrawerToolbar
#:import NavigationDrawerSubheader kivymd.navigationdrawer.NavigationDrawerSubheader
#:import MDCheckbox kivymd.selectioncontrols.MDCheckbox
#:import MDSwitch kivymd.selectioncontrols.MDSwitch
#:import MDList kivymd.list.MDList
#:import OneLineListItem kivymd.list.OneLineListItem
#:import TwoLineListItem kivymd.list.TwoLineListItem
#:import ThreeLineListItem kivymd.list.ThreeLineListItem
#:import OneLineAvatarListItem kivymd.list.OneLineAvatarListItem
#:import OneLineIconListItem kivymd.list.OneLineIconListItem
#:import OneLineAvatarIconListItem kivymd.list.OneLineAvatarIconListItem
#:import MDTextField kivymd.textfields.MDTextField
#:import MDSpinner kivymd.spinner.MDSpinner
#:import MDCard kivymd.card.MDCard
#:import MDSeparator kivymd.card.MDSeparator
#:import MDDropdownMenu kivymd.menu.MDDropdownMenu
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import colors kivymd.color_definitions.colors
#:import SmartTile kivymd.grid.SmartTile
#:import MDSlider kivymd.slider.MDSlider
#:import MDTabbedPanel kivymd.tabs.MDTabbedPanel
#:import MDTab kivymd.tabs.MDTab
#:import MDProgressBar kivymd.progressbar.MDProgressBar
#:import MDAccordion kivymd.accordion.MDAccordion
#:import MDAccordionItem kivymd.accordion.MDAccordionItem
#:import MDAccordionSubItem kivymd.accordion.MDAccordionSubItem
#:import MDThemePicker kivymd.theme_picker.MDThemePicker
#:import MDBottomNavigation kivymd.tabs.MDBottomNavigation
#:import MDBottomNavigationItem kivymd.tabs.MDBottomNavigationItem

NavigationLayout:
    id: nav_layout
    MDNavigationDrawer:
        id: nav_drawer
        NavigationDrawerToolbar:
            title: "NBA Prediction App"        
       
        
        NavigationDrawerIconButton:
            icon: 'checkbox-blank-circle'
            text: "Выбор даты"
            on_release: app.root.ids.scr_mngr.current = 'pickers'         
        NavigationDrawerIconButton:
            icon: 'checkbox-blank-circle'
            text: "Сохраненные прогнозы"
            on_release: app.root.ids.scr_mngr.current = 'tabs'
        NavigationDrawerIconButton:
            icon: 'checkbox-blank-circle'
            text: "Вход"
            on_release: app.root.ids.scr_mngr.current = 'dialog'    
        NavigationDrawerIconButton:
            icon: 'checkbox-blank-circle'
            text: "Регистрация"
            on_release: app.root.ids.scr_mngr.current = 'textfields'
        NavigationDrawerIconButton:
            icon: 'checkbox-blank-circle'
            text: "Темы"
            on_release: app.root.ids.scr_mngr.current = 'theming'
        
    BoxLayout:
        orientation: 'vertical'
        Toolbar:
            id: toolbar
            title: 'NBA Prediction App'
            md_bg_color: app.theme_cls.primary_color
            background_palette: 'Primary'
            background_hue: '500'
            left_action_items: [['menu', lambda x: app.root.toggle_nav_drawer()]]
            right_action_items: [['dots-vertical', lambda x: app.root.toggle_nav_drawer()]]
        ScreenManager:
            id: scr_mngr
            Screen:
                name: 'bottomsheet'
                MDRaisedButton:
                    text: "Выбор параметров обновления"
                    opposite_colors: True
                    size_hint: None, None
                    size: 4 * dp(48), dp(48)
                    pos_hint: {'center_x': 0.5, 'center_y': 0.6}
                    on_release: app.show_example_bottom_sheet()
                MDRaisedButton:
                    text: "Обновить статистику"
                    opposite_colors: True
                    size_hint: None, None
                    size: 4 * dp(48), dp(48)
                    pos_hint: {'center_x': 0.5, 'center_y': 0.3}
                    on_release: app.show_example_grid_bottom_sheet()
            
            Screen:
                name: 'game-toolbar'
                Toolbar:
                    id: game_header
                    title: "Toolbar with right buttons"
                    pos_hint: {'center_x': 0.5, 'center_y': 0.95}
                    md_bg_color: get_color_from_hex(colors['Amber']['700'])
                    background_palette: 'Amber'
                    background_hue: '700'
                    right_action_items: [['sd', lambda x: None]]
                    
                ScrollView:
                    do_scroll_x: False
                    pos_hint: {'center_x': 0.5, 'center_y': 0.35}
                    GridLayout:
                        cols: 3
                        row_default_height: (self.width - self.cols*self.spacing[0])/self.cols
                        row_force_default: True
                        size_hint_y: None
                        height: self.minimum_height
                        padding: dp(4), dp(4)
                        spacing: dp(4)
                        Image:
                            id: image1                           
                            source: 'nba_logos/Bulls.png'
                             
                        MDLabel:
                            id: game_head_label
                            font_style: 'Subhead'
                            theme_text_color: 'Primary'
                            text: "Дата проведения"
                            halign: 'center'                  
                                  
                        Image:
                            id: image2                            
                            source: '58419c20a6515b1e0ad75a5c.png'
                        BoxLayout: 
                            orientation: "vertical"
                            size_hint_y: None
                            height: dp(180)
                            padding: dp(48)
                            spacing: 5   
                            MDLabel:
                                id: conf_visitor
                                font_style: 'Subhead'
                                theme_text_color: 'Primary'
                                text: "Subhead label"
                                halign: 'center'
                            MDLabel:
                                id: div_visitor
                                font_style: 'Subhead'
                                theme_text_color: 'Primary'
                                text: "Subhead label"
                                halign: 'center'  
                            MDLabel:
                                id: pos_visitor
                                font_style: 'Subhead'
                                theme_text_color: 'Primary'
                                text: "Subhead label"
                                halign: 'center'
                            MDLabel:
                                id: wins_visitor
                                font_style: 'Subhead'
                                theme_text_color: 'Primary'
                                text: "Subhead label"
                                halign: 'center'    
                            MDLabel:
                                id: losses_visitor
                                font_style: 'Subhead'
                                theme_text_color: 'Primary'
                                text: "Subhead label"
                                halign: 'center' 
                            MDLabel:
                                id: pred_visitor
                                font_style: 'Title'
                                theme_text_color: 'Primary'
                                text: "-"
                                halign: 'center'                         
                        BoxLayout:
                            orientation: 'vertical'
                            size_hint_y: None
                            height: dp(180)
                            padding: dp(48)
                            spacing: 5 
                            MDLabel:
                                font_style: 'Subhead'
                                theme_text_color: 'Primary'
                                text: "Конференция"
                                halign: 'center'
                            MDLabel:
                                font_style: 'Subhead'
                                theme_text_color: 'Primary'
                                text: "Дивизион"
                                halign: 'center'
                            MDLabel:
                                font_style: 'Subhead'
                                theme_text_color: 'Primary'
                                text: "Место"
                                halign: 'center'
                            MDLabel:
                                font_style: 'Subhead'
                                theme_text_color: 'Primary'
                                text: "Победы"
                                halign: 'center'
                            MDLabel:
                                font_style: 'Subhead'
                                theme_text_color: 'Primary'
                                text: "Поражения"
                                halign: 'center' 
                            MDLabel:
                                font_style: 'Title'
                                theme_text_color: 'Primary'
                                text: "Прогноз:"
                                halign: 'center'           
                                    
                            
                        BoxLayout
                            orientation: 'vertical'
                            size_hint_y: None
                            height: dp(180)
                            padding: dp(48)
                            spacing: 5
                            MDLabel:
                                id: conf_home
                                font_style: 'Subhead'
                                theme_text_color: 'Primary'
                                text: "Subhead label"
                                halign: 'center'      
                            MDLabel:
                                id: div_home
                                font_style: 'Subhead'
                                theme_text_color: 'Primary'
                                text: "Subhead label"
                                halign: 'center'        
                            MDLabel:
                                id: pos_home
                                font_style: 'Subhead'
                                theme_text_color: 'Primary'
                                text: "Subhead label"
                                halign: 'center'    
                            MDLabel:
                                id: wins_home
                                font_style: 'Subhead'
                                theme_text_color: 'Primary'
                                text: "Subhead label"
                                halign: 'center' 
                            MDLabel:
                                id: losses_home
                                font_style: 'Subhead'
                                theme_text_color: 'Primary'
                                text: "Subhead label"
                                halign: 'center'  
                            MDLabel:
                                id: pred_home
                                font_style: 'Title'
                                theme_text_color: 'Primary'
                                text: "-"
                                halign: 'center'                            
                MDLabel:                            
                    font_style: 'Subhead'
                    theme_text_color: 'Primary'
                    text: ""
                    halign: 'center'         
                MDRaisedButton:
                    text: "Расcчитать"
                    size_hint: None, None
                    size: 3 * dp(48), dp(48)
                    pos_hint: {'center_x': 0.5, 'center_y': 0.1}
                    opposite_colors: True
                    on_release: app.show_result()   
                MDLabel:                            
                    font_style: 'Subhead'
                    theme_text_color: 'Primary'                            
                    halign: 'center'                                             
                            
                                                       
                                
            
            Screen:
                name: 'dialog'
                MDRaisedButton:
                    text: "Вход"
                    size_hint: None, None
                    size: 3 * dp(48), dp(48)
                    pos_hint: {'center_x': 0.5, 'center_y': 0.7}
                    opposite_colors: True
                    on_release: app.show_example_dialog()
                
            
            
            
            
            Screen:
                name: 'textfields'
                ScrollView:
                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_y: None
                        height: self.minimum_height
                        padding: dp(48)
                        spacing: 10
                        MDTextField:
                            hint_text: "Имя"
                            required: True
                            helper_text: "Обязательное поле"
                            helper_text_mode: "on_error"
                            min_text_length: 2
                            color_mode: 'accent'
                        MDTextField:
                            hint_text: "Пароль"
                            required: True
                            helper_text: "Не меньше 8 символов"
                            helper_text_mode: "on_error"
                            min_text_length : 8
                            color_mode: 'accent'
                        MDTextField:
                            hint_text: "Подтверждение пароля"
                            required: True
                            helper_text: "Обязательное поле"
                            helper_text_mode: "on_error"
                            min_text_length : 8
                            color_mode: 'accent'
                        MDTextField:
                            hint_text: "e-mail"
                            required: True
                            helper_text: "Обязательное поле"
                            helper_text_mode: "on_error"
                            min_text_length: 2
                            color_mode: 'accent'
                MDRaisedButton:
                    text: "Зарегистрироваться"
                    size_hint: None, None
                    size: 3 * dp(48), dp(48)
                    pos_hint: {'center_x': 0.5, 'center_y': 0.2}
                    opposite_colors: True
                               

            Screen:
                name: 'theming'
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: dp(80)
                    center_y: self.parent.center_y
                    MDRaisedButton:
                        size_hint: None, None
                        size: 3 * dp(48), dp(48)
                        center_x: self.parent.center_x
                        text: 'Сменить тему'
                        on_release: MDThemePicker().open()
                        opposite_colors: True
                        pos_hint: {'center_x': 0.5}
                    MDLabel:
                        text: "Текущая тема: " + app.theme_cls.theme_style + ", " + app.theme_cls.primary_palette
                        theme_text_color: 'Primary'
                        pos_hint: {'center_x': 0.5}
                        halign: 'center'

            
            Screen:
                name: 'tabs'
                MDTabbedPanel:
                    id: tab_panel
                    tab_display_mode:'text'

                    MDTab:
                        name: 'predictions'
                        text: 'Все прогнозы'
                        icon: "check-all"

                        ScrollView:
                            do_scroll_x: False
                            MDList:
                                id: ml                                
                                OneLineAvatarIconListItem:
                                    text: "Los Angeles Lakers vs Boston Celtics"
                                    IconRightSampleWidget:                                        
                                        
                                OneLineAvatarIconListItem:
                                    text: "Brooklyn Nets vs Boston Celtics"
                                    IconRightSampleWidget:                                        
                                           
                                        
                    MDTab:
                        name: 'good'
                        text: 'Удачные прогнозы'
                        icon: "plus"

                        MDLabel:
                            font_style: 'Body1'
                            theme_text_color: 'Primary'
                            text: "Тут будут прогнозы"
                            halign: 'center'
                    MDTab:
                        name: 'bad'
                        text: 'Неудачные прогнозы'
                        icon: "minus"

                        MDLabel:
                            font_style: 'Body1'
                            theme_text_color: 'Primary'
                            text: "Тут будут прогнозы"
                            halign: 'center'                

                    
                BoxLayout:
                    size_hint_y:None
                    height: '48dp'
                    padding: '12dp'
                    MDLabel:
                        font_style: 'Body1'
                        theme_text_color: 'Primary'
                        text: "Use icons"
                        size_hint_x:None
                        width: '64dp'
                    MDCheckbox:
                        on_state: tab_panel.tab_display_mode = 'icons' if tab_panel.tab_display_mode=='text' else 'text'
            
            Screen:
                name: 'pickers'
                BoxLayout:
                    spacing: dp(40)
                    orientation: 'vertical'
                    size_hint_x: None
                    pos_hint: {'center_x': 0.5, 'center_y': 0.9}                    
                    BoxLayout:
                        orientation: 'vertical'
                        # size_hint: (None, None)
                        MDRaisedButton:
                            text: "Выбор даты"
                            size_hint: None, None
                            size: 3 * dp(48), dp(48)
                            pos_hint: {'center_x': 0.9, 'center_y': 0.5}
                            opposite_colors: True
                            on_release: app.show_example_date_picker()
                        
                        BoxLayout:
                            size: dp(48)*3, dp(48)
                            size_hint: (None, None)
                            pos_hint: {'center_x': 0.9, 'center_y': 0.5}
                            MDLabel:
                                theme_text_color: 'Primary'
                                text: "Выбрать предыдущую дату"
                                size_hint: None, None
                                size: dp(130), dp(48)
                            MDCheckbox:
                                id: date_picker_use_previous_date
                                size_hint: None, None
                                size: dp(48), dp(48)
                              
            
            Screen:
                name: 'nav_drawer'
                HackedDemoNavDrawer:
                    # NavigationDrawerToolbar:
                    #     title: "Navigation Drawer Widgets"
                    NavigationDrawerIconButton:
                        icon: 'checkbox-blank-circle'
                        text: "Badge text ---->"
                        badge_text: "99+"
                    NavigationDrawerIconButton:
                        active_color_type: 'accent'
                        text: "Accent active color"
                    NavigationDrawerIconButton:
                        active_color_type: 'custom'
                        text: "Custom active color"
                        active_color: [1, 0, 1, 1]
                    NavigationDrawerIconButton:
                        use_active: False
                        text: "Use active = False"
                    NavigationDrawerIconButton:
                        text: "Different icon"
                        icon: 'alarm'
                    NavigationDrawerDivider:
                    NavigationDrawerSubheader:
                        text: "NavigationDrawerSubheader"
                    NavigationDrawerIconButton:
                        text: "NavigationDrawerDivider \/"
                    NavigationDrawerDivider:

'''


class HackedDemoNavDrawer(MDNavigationDrawer):
    # DO NOT USE
    def add_widget(self, widget, index=0):
        if issubclass(widget.__class__, BaseListItem):
            self._list.add_widget(widget, index)
            if len(self._list.children) == 1:
                widget._active = True
                self.active_item = widget
            # widget.bind(on_release=lambda x: self.panel.toggle_state())
            widget.bind(on_release=lambda x: x._set_active(True, list=self))
        elif issubclass(widget.__class__, NavigationDrawerHeaderBase):
            self._header_container.add_widget(widget)
        else:
            super(MDNavigationDrawer, self).add_widget(widget, index)


class KitchenSink(App):
    theme_cls = ThemeManager()
    previous_date = ObjectProperty()
    title = "NBA Prediction App"

    menu_items = [
        {'viewclass': 'MDMenuItem',
         'text': 'Example item'},
        {'viewclass': 'MDMenuItem',
         'text': 'Example item'},
        {'viewclass': 'MDMenuItem',
         'text': 'Example item'},
        {'viewclass': 'MDMenuItem',
         'text': 'Example item'},
        {'viewclass': 'MDMenuItem',
         'text': 'Example item'},
        {'viewclass': 'MDMenuItem',
         'text': 'Example item'},
        {'viewclass': 'MDMenuItem',
         'text': 'Example item'},
    ]

    def build(self):
        main_widget = Builder.load_string(main_widget_kv)
        # self.theme_cls.theme_style = 'Dark'

        # main_widget.ids.text_field_error.bind(
        #     on_text_validate=self.set_error_message,
        #     on_focus=self.set_error_message)
        self.bottom_navigation_remove_mobile(main_widget)
        return main_widget

    def bottom_navigation_remove_mobile(self, widget):
        # Removes some items from bottom-navigation demo when on mobile
        if DEVICE_TYPE == 'mobile':
            widget.ids.bottom_navigation_demo.remove_widget(widget.ids.bottom_navigation_desktop_2)
        if DEVICE_TYPE == 'mobile' or DEVICE_TYPE == 'tablet':
            widget.ids.bottom_navigation_demo.remove_widget(widget.ids.bottom_navigation_desktop_1)

    def show_example_snackbar(self, snack_type):
        if snack_type == 'simple':
            Snackbar(text="This is a snackbar!").show()
        elif snack_type == 'button':
            Snackbar(text="This is a snackbar", button_text="with a button!", button_callback=lambda *args: 2).show()
        elif snack_type == 'verylong':
            Snackbar(text="This is a very very very very very very very long snackbar!").show()

    def show_example_dialog(self):
        content1 = MDTextField(hint_text= "Имя",required= True,helper_text= "Обязательное поле",
                              helper_text_mode= "on_error")
        content2 = MDTextField(hint_text="Парол", required=True, helper_text="Обязательное поле",
                               helper_text_mode="on_error")
        content1.hint_text = "Имя пользователя"
        content1.helper_text = "Некорректный ввод"
        content1.min_text_length= 2
        content1.color_mode= 'accent'
        content2.hint_text = "Пароль"
        content2.helper_text = "Некорректный ввод"
        content2.min_text_length = 8
        content2.color_mode = 'accent'
        layout1 = BoxLayout(orientation= 'vertical', size_hint_y= None, height= dp(180), padding= dp(48),spacing= 10)
        layout1.add_widget(content1)
        layout1.add_widget(content2)


        # content.bind(texture_size=content.setter('size'))
        self.dialog = MDDialog(title="Вход",
                               content=layout1,
                               size_hint=(.8, None),
                               height=dp(300),
                               auto_dismiss=False)
        self.dialog.add_action_button("ОК",
                                      action=lambda *x: self.dialog.dismiss())
        self.dialog.add_action_button("Отмена",
                                      action=lambda *x: self.dialog.dismiss())
        self.dialog.open()





    def set_previous_date(self, date_obj):
        self.previous_date = date_obj

        connect = sqlite3.connect("nbadb.db")
        cursor = connect.cursor()

        r = str(date_obj)+'T00:00:00'
        cursor.execute("""SELECT GAME_ID, HOME_TEAM_ID, VISITOR_TEAM_ID FROM calendar
                          WHERE GAME_DATE_EST = (?)
                      """, (r,))

        l = cursor.fetchall()
        self.output_string = []
        bs = MDListBottomSheet()
        bs.add_item("Список игр: " + str(date_obj), lambda x: x)

        for i in range(len(l)):
            self.output_string.append('')
            cursor.execute("""SELECT TEAM_CITY, TEAM_NAME FROM team
                                      WHERE TEAM_ID = (?)
                                  """, (l[i][2],))
            fetchall = cursor.fetchall()[0]
            self.output_string[i] += str(fetchall[0]) + " " + str(fetchall[1]) + ' vs '
            cursor.execute("""SELECT TEAM_CITY, TEAM_NAME FROM team
                                                  WHERE TEAM_ID = (?)
                                              """, (l[i][1],))
            fetchall = cursor.fetchall()[0]
            self.output_string[i] += str(fetchall[0]) + " " + str(fetchall[1])
            bs.add_item(self.output_string[i],self.show_game_info, icon='bomb')

        bs.open()

        connect.commit()

    def show_game_info(self,date):

        self.root.ids.scr_mngr.current = 'game-toolbar'
        self.root.ids.game_header.title = date.text
        result = re.split(' ',str(date.text))
        connect = sqlite3.connect("nbadb.db")
        cursor = connect.cursor()

        if (result[0] == 'New') or (result[0] == 'San') or (result[0] == 'Los') or (result[0] == 'Golden') or (result[0] == 'Oklahoma') or (result[0] == 'Portland'):
            self.root.ids.image1.source = 'nba_logos/'+result[2]+'.png'
            self.root.ids.image2.source = 'nba_logos/'+result[len(result)-1]+'.png'
            team_name_away = str(result[0]+' '+result[1]+' '+result[2])

        else:
            self.root.ids.image1.source = 'nba_logos/' + result[1] + '.png'
            self.root.ids.image2.source = 'nba_logos/' + result[len(result) - 1] + '.png'
            team_name_away = str(result[0] + ' ' + result[1])

        if (result[len(result)-3] == 'New') or (result[len(result)-3] == 'San') or (result[len(result)-3] == 'Los') or (result[len(result)-3] == 'Golden') or (
                                                                                result[len(result)-3] == 'Oklahoma') or (result[len(result)-3] == 'Portland'):
            team_name_home = str(result[len(result)-3] + ' ' + result[len(result)-2] + ' ' + result[len(result)-1])
        else:
            team_name_home = str(result[len(result) - 2] + ' ' + result[len(result) - 1])
        cursor.execute("""SELECT W, L, TEAM_ID FROM team_adv_stats
                                                          WHERE TEAM_NAME = (?)
                                                      """, (team_name_away,))

        wins_visitor, losses_visitor,self.team_id_visitor = cursor.fetchall()[0]
        self.root.ids.wins_visitor.text = str(wins_visitor)
        self.root.ids.losses_visitor.text = str(losses_visitor)

        cursor.execute("""SELECT W, L,TEAM_ID FROM team_adv_stats
                                                          WHERE TEAM_NAME = (?)
                                                      """, (team_name_home,))

        wins_home, losses_home,self.team_id_home = cursor.fetchall()[0]

        self.root.ids.wins_home.text = str(wins_home)
        self.root.ids.losses_home.text = str(losses_home)

        cursor.execute("""SELECT TEAM_CONFERENCE, TEAM_DIVISION,CONF_RANK FROM team
                                                                          WHERE TEAM_ID = (?)
                                                                      """, (self.team_id_visitor,))
        away_team_conf, away_team_div, away_team_conf_rank = cursor.fetchall()[0]
        self.root.ids.conf_visitor.text = str(away_team_conf)
        self.root.ids.div_visitor.text = str(away_team_div)
        self.root.ids.pos_visitor.text = str(away_team_conf_rank)


        cursor.execute("""SELECT TEAM_CONFERENCE, TEAM_DIVISION,CONF_RANK, TEAM_CITY FROM team
                                                                  WHERE TEAM_ID = (?)
                                                              """, (self.team_id_home,))
        home_team_conf, home_team_div, home_team_conf_rank,city = cursor.fetchall()[0]
        self.root.ids.conf_home.text = str(home_team_conf)
        self.root.ids.div_home.text = str(home_team_div)
        self.root.ids.pos_home.text = str(home_team_conf_rank)
        self.root.ids.game_head_label.text = "Дата:\n" + str(self.previous_date) +"\nГород:\n" +str(city)
        self.root.ids.pred_home.text = '-'
        self.root.ids.pred_visitor.text = '-'

    def show_result(self):
        score_home,score_away,home,guest = get_tempo(self.team_id_home,self.team_id_visitor)
        score_home, score_away, home, guest = get_refs(score_home,score_away,home,guest)
        score_home, score_away, home, guest = get_reb(score_home,score_away,home,guest)
        score_home, score_away = get_clutch(score_home,score_away,home,guest)
        self.root.ids.pred_home.text = str(round(score_home))
        self.root.ids.pred_visitor.text = str(round(score_away))



    def show_example_date_picker(self):
        if self.root.ids.date_picker_use_previous_date.active:
            pd = self.previous_date
            try:
                MDDatePicker(self.set_previous_date,
                             pd.year, pd.month, pd.day).open()
            except AttributeError:
                MDDatePicker(self.set_previous_date).open()
        else:
            MDDatePicker(self.set_previous_date).open()

    def show_example_bottom_sheet(self):
        bs = MDListBottomSheet()
        bs.add_item("Here's an item with text only", lambda x: x)
        bs.add_item("Here's an item with an icon", lambda x: x,
                    icon='clipboard-account')
        bs.add_item("Here's another!", lambda x: x, icon='nfc')
        bs.open()

    def show_example_grid_bottom_sheet(self):
        bs = MDGridBottomSheet()
        bs.add_item("Facebook", lambda x: x,
                    icon_src='./assets/facebook-box.png')
        bs.add_item("YouTube", lambda x: x,
                    icon_src='./assets/youtube-play.png')
        bs.add_item("Twitter", lambda x: x,
                    icon_src='./assets/twitter.png')
        bs.add_item("Da Cloud", lambda x: x,
                    icon_src='./assets/cloud-upload.png')
        bs.add_item("Camera", lambda x: x,
                    icon_src='./assets/camera.png')
        bs.open()

    def set_error_message(self, *args):
        if len(self.root.ids.text_field_error.text) == 2:
            self.root.ids.text_field_error.error = True
        else:
            self.root.ids.text_field_error.error = False

    def on_pause(self):
        return True

    def on_stop(self):
        pass


class AvatarSampleWidget(ILeftBody, Image):
    pass


class IconLeftSampleWidget(ILeftBodyTouch, MDIconButton):
    pass


class IconRightSampleWidget(IRightBodyTouch, MDCheckbox):
    pass


if __name__ == '__main__':
    KitchenSink().run()
