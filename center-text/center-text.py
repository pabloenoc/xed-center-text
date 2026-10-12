import json
import os

from gi.repository import GObject, GLib, Gtk, PeasGtk, Xed

LANGUAGES = {"markdown"}     
DEFAULT_WIDTH = 72
CONFIG_PATH = os.path.join(GLib.get_user_config_dir(), "xed", "center-text.json")


_instances = set()


def load_width():
    try:
        with open(CONFIG_PATH) as f:
            return int(json.load(f).get("text_width", DEFAULT_WIDTH))
    except (OSError, ValueError, AttributeError):
        return DEFAULT_WIDTH


def save_width(width):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump({"text_width": width}, f)


settings = {"text_width": load_width()}


class CenterText(GObject.Object, Xed.ViewActivatable):
    __gtype_name__ = "Center Text"
    view = GObject.property(type=Xed.View)

    def __init__(self):
        GObject.Object.__init__(self)
        self._pending = 0

    def do_activate(self):
        self._buffer = self.view.get_buffer()
        self._orig_left = self.view.get_left_margin()
        self._orig_right = self.view.get_right_margin()
        self._handlers = [
            (self.view, self.view.connect("size-allocate", self._schedule)),
            (self.view, self.view.connect("style-updated", self._schedule)),
            (self._buffer, self._buffer.connect("notify::language", self._schedule)),
        ]
        _instances.add(self)
        self._schedule()

    def do_deactivate(self):
        _instances.discard(self)
        for obj, handler_id in self._handlers:
            obj.disconnect(handler_id)
        if self._pending:
            GLib.source_remove(self._pending)
            self._pending = 0
        self.view.set_left_margin(self._orig_left)
        self.view.set_right_margin(self._orig_right)


    def _schedule(self, *args):
        if not self._pending:
            self._pending = GLib.idle_add(self._update)

    def _update(self):
        self._pending = 0
        lang = self._buffer.get_language()

        if lang is None or lang.get_id() not in LANGUAGES:
            self._set_margins(self._orig_left, self._orig_right)
            return False

        sample = "0" * settings["text_width"]
        text_px = self.view.create_pango_layout(sample).get_pixel_size()[0]
        gutter = self.view.get_border_window_size(Gtk.TextWindowType.LEFT)
        available = self.view.get_allocated_width() - gutter
        margin = max(self._orig_left, (available - text_px) // 2)

        self._set_margins(margin, margin)
        return False  

    def _set_margins(self, left, right):
        if self.view.get_left_margin() != left:
            self.view.set_left_margin(left)
        if self.view.get_right_margin() != right:
            self.view.set_right_margin(right)


class CenterTextConfigurable(GObject.Object, PeasGtk.Configurable):
    __gtype_name__ = "CenterTextConfigurable"

    def do_create_configure_widget(self):
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        box.set_border_width(12)

        label = Gtk.Label(label="Text width (characters):")
        spin = Gtk.SpinButton.new_with_range(30, 200, 1)
        spin.set_value(settings["text_width"])
        spin.connect("value-changed", self._on_changed)

        box.pack_start(label, False, False, 0)
        box.pack_start(spin, False, False, 0)
        box.show_all()
        return box

    def _on_changed(self, spin):
        settings["text_width"] = spin.get_value_as_int()
        save_width(settings["text_width"])
        for instance in list(_instances):
            instance._schedule()
