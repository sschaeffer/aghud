#!/usr/bin/env python3
from re import T
from sys import path

path.append("/home/integ/Code/aghud")

from ag.common.aghudconstants import AGHUDConstants
from ag.common.aghudconfig import AGHUDConfig
from ag.advancements.alladvancements import Advancement, AllAdvancements

from os import environ
import curses
from curses import panel

class AdvancementWindow():

    ADVANCEMENT_WINDOW_DOWN=1
    ADVANCEMENT_WINDOW_UP=-1

    ADVANCEMENT_WINDOW_ORIGINAL_ORDER=0
    ADVANCEMENT_WINDOW_REVERSE_ORIGINAL_ORDER=1
    ADVANCEMENT_WINDOW_SORTED_ORDER=2
    ADVANCEMENT_WINDOW_REVERSE_SORTED_ORDER=3
    ADVANCEMENT_WINDOW_COMPLETED_FIRST_ORDER=4
    ADVANCEMENT_WINDOW_COMPLETED_LAST_ORDER=5


    def __init__(self, stdscr:curses.window, aghudconfig):
        self._stdscr:curses.stdscr = stdscr
        self._alladvancements = AllAdvancements(aghudconfig)
        self._alladvancements.update_advancements('de3bf147-8c46-4698-81e1-ca2ef0a3e02d.json')

        self._currentadvancementslist=[]
        self._maxlines = 0
        self._focus = ""

        self._currentadvancement = 0
        self._topadvancement=0
        self._bottomadvancement=0

        self._currentcriteria = 0
        self._topcriteria=0
        self._bottomcriteria=0

        self._advancementsort=self.ADVANCEMENT_WINDOW_ORIGINAL_ORDER

        self._advancementwindow = curses.newwin(0,0)
        self._advancementpanel = panel.new_panel(self._advancementwindow)
        self._advancementpanel.hide()
        self._windowopen = False

    def select_advancement_root(self,advancementroot):
  
        self._advancementroot = advancementroot
        self._currentadvancementslist.clear()
        self._currentadvancement=0
        self._topadvancement=0
        self._currentcriteria=0
        self._topcriteria=0
        self._advancementsort=self.ADVANCEMENT_WINDOW_ORIGINAL_ORDER
        self._currentadvancementslist = self._alladvancements.advancement_list(self._advancementroot)

    def scroll_advancements(self, direction):
        nextline = self._currentadvancement + direction
        if (direction == self.ADVANCEMENT_WINDOW_UP) and (self._topadvancement > 0 and self._currentadvancement == 0):
            self._topadvancement += direction
        elif ((direction == self.ADVANCEMENT_WINDOW_DOWN) and (nextline == self._maxlines) and
                (self._topadvancement + self._maxlines < self._bottomadvancement)):
            self._topadvancement += direction
        elif (direction == self.ADVANCEMENT_WINDOW_UP) and (self._topadvancement > 0 or self._currentadvancement > 0):
            self._currentadvancement = nextline
        elif ((direction == self.ADVANCEMENT_WINDOW_DOWN) and (nextline < self._maxlines) and 
                (self._topadvancement + nextline < self._bottomadvancement)):
            self._currentadvancement = nextline

    def scroll_criteria(self, direction):
        if (direction == self.ADVANCEMENT_WINDOW_UP) and (self._topcriteria > 0):
            self._topcriteria += direction
        elif (direction == self.ADVANCEMENT_WINDOW_DOWN) and (self._topcriteria + self._maxlines < self._bottomcriteria):
            self._topcriteria += direction

    def change_sort_order(self):
        if(self._advancementsort == self.ADVANCEMENT_WINDOW_ORIGINAL_ORDER):
            self.select_advancement_root(self._advancementroot)
        elif(self._advancementsort == self.ADVANCEMENT_WINDOW_REVERSE_ORIGINAL_ORDER):
            self._currentadvancementslist = list(reversed(self._currentadvancementslist))
        elif(self._advancementsort == self.ADVANCEMENT_WINDOW_SORTED_ORDER):
            self._currentadvancementslist.sort(key = self._alladvancements.advancement_title)
        elif(self._advancementsort == self.ADVANCEMENT_WINDOW_REVERSE_SORTED_ORDER):
            self._currentadvancementslist.sort(key = self._alladvancements.advancement_title,reverse=True)
        elif(self._advancementsort == self.ADVANCEMENT_WINDOW_COMPLETED_FIRST_ORDER):
            self._currentadvancementslist.sort(key = self._alladvancements.advancement_complete,reverse=True)
        elif(self._advancementsort == self.ADVANCEMENT_WINDOW_COMPLETED_LAST_ORDER):
            self._currentadvancementslist.sort(key = self._alladvancements.advancement_complete)

    def event_handler(self,input):
        if input in [27]:
            if self._focus != "":
                self._focus = ""
                self._topcriteria=0
            else:
                if self._advancementroot != "":
                    self._advancementroot = ""
                    self.select_advancement_root(self._advancementroot)
        elif input in [curses.KEY_ENTER,ord('\n')]:
            if self._advancementroot == "":
                self.select_advancement_root(self._currentadvancementslist[self._topadvancement+self._currentadvancement])
            else:
                self._focus = self._advancementroot
        elif input in [curses.KEY_DOWN,ord('j')]:
            if self._focus == "":
                self.scroll_advancements(self.ADVANCEMENT_WINDOW_DOWN) 
            else:
                self.scroll_criteria(self.ADVANCEMENT_WINDOW_DOWN) 
        elif input in [curses.KEY_UP,ord('k')]:
            if self._focus == "":
                self.scroll_advancements(self.ADVANCEMENT_WINDOW_UP) 
            else:
                self.scroll_criteria(self.ADVANCEMENT_WINDOW_UP) 
        elif input == ord('c'):
            if self._advancementsort == self.ADVANCEMENT_WINDOW_COMPLETED_FIRST_ORDER:
                self._advancementsort = self.ADVANCEMENT_WINDOW_COMPLETED_LAST_ORDER
            else:
               self._advancementsort = self.ADVANCEMENT_WINDOW_COMPLETED_FIRST_ORDER
            self.change_sort_order()
        elif input == ord('o'):
            if self._advancementsort == self.ADVANCEMENT_WINDOW_ORIGINAL_ORDER:
                self._advancementsort = self.ADVANCEMENT_WINDOW_REVERSE_ORIGINAL_ORDER 
            else:
                self._advancementsort = self.ADVANCEMENT_WINDOW_ORIGINAL_ORDER 
            self.change_sort_order()
        elif input == ord('a'):
            if self._advancementsort == self.ADVANCEMENT_WINDOW_SORTED_ORDER:
                self._advancementsort = self.ADVANCEMENT_WINDOW_REVERSE_SORTED_ORDER
            else:
                self._advancementsort = self.ADVANCEMENT_WINDOW_SORTED_ORDER
            self.change_sort_order()

    def render(self,height,width):

        if(height<AGHUDConstants.MINIMUM_HEIGHT or width<AGHUDConstants.MINIMUM_WIDTH):
            return

        self._windowopen = True

        self._maxlines = height-2
        self._advancementwindow.resize(height-2,width)
        self._advancementwindow.clear()

        self._bottomadvancement = len(self._currentadvancementslist)
        if self._bottomadvancement < 1:
            return

        for i in range(len(self._currentadvancementslist))[self._topadvancement:self._topadvancement+self._maxlines]:
            j=i-self._topadvancement
            advancementtitle:str = self._alladvancements.advancement_title(self._currentadvancementslist[i])
            self._advancementwindow.addstr(j,0,advancementtitle)

            if j == self._currentadvancement:
                if(self._alladvancements.advancement_complete(self._currentadvancementslist[i]) == Advancement.ADVANCEMENT_COMPLETED):
                    self._advancementwindow.addstr(j,0,advancementtitle,
                            curses.color_pair(AGHUDConstants.COLOR_ADVANCEMENT_COMPLETE)|curses.A_REVERSE)
                else:
                    self._advancementwindow.addstr(j,0,advancementtitle, curses.A_REVERSE)
            else:
                if(self._alladvancements.advancement_complete(self._currentadvancementslist[i]) == Advancement.ADVANCEMENT_COMPLETED):
                    self._advancementwindow.addstr(j,0,advancementtitle,
                            curses.color_pair(AGHUDConstants.COLOR_ADVANCEMENT_COMPLETE))
                else:
                    self._advancementwindow.addstr(j,0,advancementtitle)

        advancement:Advancement = self._alladvancements._advancements[self._currentadvancementslist[self._topadvancement+self._currentadvancement]]
        self._bottomcriteria = len(advancement._criteria) 
        for i in range(self._bottomcriteria)[self._topcriteria:self._topcriteria+self._maxlines]:
            j=i-self._topcriteria
            if advancement._criteria[i] in advancement._finished:
                self._advancementwindow.addstr(j,30,advancement._criteria[i],
                        curses.color_pair(AGHUDConstants.COLOR_ADVANCEMENT_COMPLETE))
            else:
                self._advancementwindow.addstr(j,30,advancement._criteria[i])

        self._advancementpanel.move(1,0)
        self._advancementpanel.show()
        panel.update_panels()
        self._stdscr.noutrefresh()




# ----
# UNIT TESTING ROUTINES - REMOVE BEFORE DEPLOYING RELEASE
# ----

def main(stdscr:curses.window, aghudconfig):

    aghudconfig.curses_setup(stdscr)
    advancementwindow = AdvancementWindow(stdscr,aghudconfig)
    advancementwindow.select_advancement_root('')

    try:
        pass
        keyboardinput = 0
        while keyboardinput != ord("q"): 
            (height,width) = aghudconfig.check_minimum_size(stdscr)

            advancementwindow.event_handler(keyboardinput)
            advancementwindow.render(height,width)
            curses.doupdate()
            keyboardinput = stdscr.getch()

    except KeyboardInterrupt:
        pass
    finally:
        curses.endwin()


if __name__ == "__main__":
    aghudconfig = AGHUDConfig("/home/integ/Code/aghud/config.json")
    environ.setdefault('ESCDELAY', '25')
    curses.wrapper(main,aghudconfig)