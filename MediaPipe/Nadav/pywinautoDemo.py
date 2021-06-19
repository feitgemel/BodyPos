from pywinauto.application import Application
from pywinauto import Desktop

windows = Desktop(backend="uia").windows()
print([w.window_text() for w in windows])

#app = Application().start('"Grid 3.exe" "C:\\Program Files (x86)\\Smartbox\\Grid 3"')
app = Application(backend='uia').connect(title = 'Grid 3 - Nadav - Home',timeout=2)
#app.Grid3NadavHome.print_control_identifiers()
app.top_window().set_focus()



#app.UntitledNotepad.menu_select("Help->About Notepad")
#app.AboutNotepad.OK.click()
#app.UntitledNotepad.Edit.type_keys("pywinauto Works!", with_spaces = True)