#!/usr/bin/env python3

import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Pango, GLib
from pysword.canons import canons
from pysword.modules import SwordModules

import pprint

class SwordApp(object):

    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file('biblebrowser.glade')

        self.form1 = self.builder.get_object('swordWindow')
        self.form1.connect('destroy', Gtk.main_quit)

        self.version_store = self.builder.get_object('versionStore')

        self.load_modules()

        self.book_store = self.builder.get_object('bookStore')

        for k in canons['kjv']:
            for b in canons['kjv'][k]:
                self.book_store.append([b[0], b[1]])

        self.book_name = self.book_store[0][0]
        self.chapter_number = 1
        self.verse_number = 1

        self.bible_pane = self.builder.get_object('biblePane')

        bible_view = self.builder.get_object('bibleTextView')
        version_combo = self.builder.get_object('versionCombo')
        bible_view_left = self.builder.get_object('bibleTextViewLeft')
        version_combo_left = self.builder.get_object('versionComboLeft')
        bible_view_right = self.builder.get_object('bibleTextViewRight')
        version_combo_right = self.builder.get_object('versionComboRight')

        self.normal_view = VersionView(self, bible_view, version_combo)
        self.parallel_view = ParallelView(self, bible_view_left, version_combo_left, bible_view_right, version_combo_right)

        self.current_view = self.normal_view

        self.book_combo = self.builder.get_object('bookCombo')

        self.chapter_spin = self.builder.get_object('chapterSpin')
        self.chapter_ad = self.builder.get_object('chapterAdjustment')

        self.verse_spin = self.builder.get_object('verseSpin')
        self.verse_ad = self.builder.get_object('verseAdjustment')

        self.chapter_spin.set_value(self.chapter_number)
        self.verse_spin.set_value(self.verse_number)

        self.book_combo.set_active(0)

        self.builder.connect_signals(self)

        self.normal_view.set_version()
        self.parallel_view.set_version()
        self.set_book()
        self.normal_view.set_passage()
        self.parallel_view.set_passage()

        self.about_dialog = self.builder.get_object('aboutDialog')

        self.form1.show_all()

    def load_modules(self):
        self.modules = SwordModules()
        found_modules = self.modules.parse_modules()

        for module in found_modules.keys():
            if found_modules[module]['moddrv'] in ('zText', 'RawText'):
                self.version_store.append([found_modules[module]['description'], module])

    def book_completed(self, widget, model, iterr, data=None):
        book_name = model.get_value(iterr, 0)
        self.book_name = book_name
        self.set_book()

    def book_entered(self, widget, event=None, data=None):
        book_name = widget.get_text()
        for item in self.book_store:
            print('testing', item[0])
            if item[0].lower() == book_name.lower():
                self.book_name = item[0]
                self.set_book()
        widget.set_text(self.book_name)

    def set_book(self):
        self.book = self.current_view.get_bible().get_structure().find_book(self.book_name)[1]
        num_chapters = self.book.num_chapters
        self.chapter_ad.set_upper(num_chapters)
        self.chapter_number = min(self.chapter_number, num_chapters)
        self.chapter_spin.set_value(self.chapter_number)
        self.current_view.set_passage()

    def set_chapter(self, active=0):
        num_verses = self.book.chapter_lengths[active]
        self.verse_ad.set_upper(num_verses)

    def show_error(self, message):
        dialog = Gtk.MessageDialog(self.form1, 0, Gtk.MessageType.ERROR,
            Gtk.ButtonsType.OK, message)
        dialog.set_title('Error')
        dialog.run()
        dialog.destroy()

    def show_about(self, widget):
        self.about_dialog.run()
        self.about_dialog.hide()

    def main_quit(self, widget):
        Gtk.main_quit()

    def book_combo_changed(self, widget, data=None):
        active = widget.get_active()
        if active >= 0:
            self.book_name = self.book_store[active][0]
            self.set_book()

    def chapter_spin_changed(self, widget):
        self.chapter_number = int(widget.get_value())
        self.set_chapter(self.chapter_number - 1)
        self.current_view.set_passage()

    def verse_spin_changed(self, widget):
        self.verse_number = int(widget.get_value())
        self.current_view.set_current_verse()
        self.current_view.scroll_to_current_verse()

    def stack_changed(self, widget, data=None):
        print('stack changed', data)
        if self.current_view == self.normal_view:
            self.current_view = self.parallel_view
        else:
            self.current_view = self.normal_view
        self.current_view.set_passage()

class VersionView(object):

    def __init__(self, app, bible_view, version_combo):
        self.app = app
        self.bible_view = bible_view
        self.bible_buffer = self.bible_view.get_buffer()
        self.version_combo = version_combo

        self.tag = self.bible_buffer.create_tag('normal', scale=1.2)
        self.bold_tag = self.bible_buffer.create_tag('bold', scale=0.9, weight=Pango.Weight.BOLD)
        self.italic_tag = self.bible_buffer.create_tag('italic', style=Pango.Style.ITALIC)
        self.underline_tag = self.bible_buffer.create_tag('underline', underline=Pango.Underline.SINGLE)

        self.version_combo.connect('changed', self.version_combo_changed)
        self.version_combo.set_active(0)

    def get_bible(self):
        return self.bible

    def set_version(self, active=0):
        self.bible = self.app.modules.get_bible_from_module(self.app.version_store[active][1])

    def set_passage(self):
        iter = self.bible.get_iter(books=[self.app.book_name], chapters=[self.app.chapter_number])
        self.bible_buffer.set_text('')
        try:
            for i, verse in enumerate(iter):
                end_iter = self.bible_buffer.get_end_iter()
                self.bible_buffer.insert_with_tags(end_iter, str(i+1), self.bold_tag)
                end_iter = self.bible_buffer.get_end_iter()
                self.bible_buffer.insert(end_iter, ' ')
                end_iter = self.bible_buffer.get_end_iter()
                self.bible_buffer.insert_with_tags(end_iter, "%s\n" % (verse), self.tag)
        except ValueError as e:
            pass
        self.set_current_verse()

    def set_current_verse(self):
        self.bible_buffer.remove_tag(self.underline_tag, self.bible_buffer.get_start_iter(), self.bible_buffer.get_end_iter())
        line_start_iter = self.bible_buffer.get_iter_at_line_offset(self.app.verse_number - 1, len(str(self.app.verse_number))+1)
        line_end_iter = self.bible_buffer.get_iter_at_line_offset(self.app.verse_number - 1, 10000)
        self.bible_buffer.apply_tag(self.underline_tag, line_start_iter, line_end_iter)

    def scroll_to_current_verse(self):
        scroll_iter = self.bible_buffer.get_iter_at_line(self.app.verse_number)
        self.bible_view.scroll_to_iter(scroll_iter, 0.0, True, 0.5, 0.5)

    def version_combo_changed(self, widget):
        active = widget.get_active()
        self.set_version(active)
        self.set_passage()

class ParallelView(VersionView):

    def __init__(self, app, left_view, left_combo, right_view, right_combo):
        self.left_version = VersionView(app, left_view, left_combo)
        self.right_version= VersionView(app, right_view, right_combo)

    def get_bible(self):
        return self.left_version.get_bible()

    def set_version(self, active=0):
        self.left_version.set_version(active)
        self.right_version.set_version(active)

    def set_passage(self):
        self.left_version.set_passage()
        self.right_version.set_passage()

    def set_current_verse(self):
        self.left_version.set_current_verse()
        self.right_version.set_current_verse()

    def scroll_to_current_verse(self):
        self.left_version.scroll_to_current_verse()
        self.right_version.scroll_to_current_verse()

if __name__ == '__main__':
    try:
        gui = SwordApp()
        Gtk.main()
    except KeyboardInterrupt:
        pass

