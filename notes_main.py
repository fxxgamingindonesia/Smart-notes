#start to create smart notes app
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout

import json

# notes = {
#     "Judul catatan!" : {
#         "text" : "ini digunakan untuk menyimpan catatan",
#         "tags" : ["tag1", "tag2"]
#     }
# }

# with open("notes_data.json", "w") as file:
#     json.dump(notes, file, ensure_ascii=False)

app = QApplication([])
window = QWidget()
window.setWindowTitle('Smart Notes')
window.resize(900, 600)

field_text = QTextEdit()

lb_list_notes = QLabel('List of notes')
list_notes =  QListWidget()

btn_note_create = QPushButton('Create note')
btn_note_delete = QPushButton('Delete note')
btn_note_save = QPushButton('Save note')

lb_list_tags = QLabel('List of tags')
list_tags = QListWidget()

field_tags = QLineEdit()
field_tags.setPlaceholderText('Enter tag... ')

btn_tags_add = QPushButton('Add to note')
btn_tags_untag = QPushButton('Untag from note')
btn_tags_search = QPushButton('Search notes by tag')

main_layout = QHBoxLayout()
layout_left = QVBoxLayout()
layout_right = QVBoxLayout()
layout_btn_notes = QHBoxLayout()
layout_btn_tags = QHBoxLayout()

layout_left.addWidget(field_text)
layout_right.addWidget(lb_list_notes)
layout_right.addWidget(list_notes)
layout_btn_notes.addWidget(btn_note_create)
layout_btn_notes.addWidget(btn_note_delete)
layout_right.addLayout(layout_btn_notes)

layout_right.addWidget(btn_note_save)
layout_right.addWidget(lb_list_tags)
layout_right.addWidget(list_tags)
layout_right.addWidget(field_tags)
layout_btn_tags.addWidget(btn_tags_add)
layout_btn_tags.addWidget(btn_tags_untag)
layout_right.addLayout(layout_btn_tags)

layout_right.addWidget(btn_tags_search)
main_layout.addLayout(layout_left, stretch= 2)
main_layout.addLayout(layout_right, stretch= 1)
window.setLayout(main_layout)

def show_note():
    key = list_notes.selectedItems()[0].text()
    field_text.setText(notes[key]['text'])
    list_tags.clear()
    list_tags.addItems(notes[key]['tags'])

def add_note():
    note_name, ok = QInputDialog.getText(window, "Add note", "Note name: ")
    if ok and note_name != '':
        notes[note_name] = {"text" : "", "tags": []}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]['tags'])
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, ensure_ascii=False)

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_tags.clear()
        list_notes.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, ensure_ascii=False)

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]['text'] = field_text.toPlainText()
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, ensure_ascii=False)
        
def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tags.text()
        if not tag in notes[key]['tags']:
            notes[key]['tags'].append(tag)
            list_tags.addItem(tag)
            field_tags.clear()
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, ensure_ascii=False)

def del_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]['tags'].remove(tag)
        
        list_tags.clear()
        list_tags.addItems(notes[key]['tags'])
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, ensure_ascii=False)

def search_tag():
    tag = field_tags.text()
    if btn_tags_search.text() == "Search notes by tag" and tag:
        print(tag)
        notes_filtered = {}
        for note in notes:
	            if tag in notes[note]["tags"]:
                        notes_filtered[note]=notes[note]
        btn_tags_search.setText("Reset search")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
    elif btn_tags_search.text() == "Reset search":
        field_tags.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        btn_tags_search.setText("Search notes by tag")

with open("notes_data.json", "r") as file:
    notes = json.load(file)
list_notes.addItems(notes)


list_notes.itemClicked.connect(show_note)
btn_note_create.clicked.connect(add_note)
btn_note_delete.clicked.connect(del_note)
btn_note_save.clicked.connect(save_note)
btn_tags_add.clicked.connect(add_tag)
btn_tags_untag.clicked.connect(del_tag)
btn_tags_search.clicked.connect(search_tag)
window.show()
app.exec_()
