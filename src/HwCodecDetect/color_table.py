"""
Custom Color Table Widget for HwCodecDetect GUI.
Provides per-cell color control using tkinter Canvas + Label grid.
"""
import tkinter as tk
from tkinter import ttk
from .theme import (
    BG_ROOT as _BG_ROOT,
    BG_SURFACE as _BG_SURFACE,
    BG_ELEVATED as _BG_ELEVATED,
    BG_HOVER as _BG_HOVER,
    BORDER as _BORDER,
    TEXT_PRIMARY as _TEXT_PRIMARY,
    TEXT_SECONDARY as _TEXT_SECONDARY,
    TEXT_DIM as _TEXT_DIM,
    FAMILY as _FAMILY,
)


class ColorTable(tk.Frame):
    """
    A table widget with per-cell color control.

    Each cell is an independent Label widget that can have its own foreground
    and background colors.  Supports alternating row backgrounds, row hover
    effects, horizontal / vertical scrolling and cell click callbacks.

    Usage::

        table = ColorTable(parent)
        table.set_columns([
            {"title": "Codec", "width": 220, "anchor": "w", "stretch": True},
            {"title": "240p",  "width": 60,  "anchor": "center"},
        ])
        table.insert_row([
            {"text": "H264 Encoder", "fg": "#ecedf2"},
            {"text": "●", "fg": "#4ade80",
             "meta": {"codec_name": "...", "col_name": "...",
                      "status": "succeeded", "error_msg": ""}},
        ], row_tag="row_even")
        table.on_cell_click(callback)
        table.update_cell(row_idx, col_idx, text="●", fg="#ef4444",
                          meta={"status": "failed", ...})
    """

    # ─── Construction ─────────────────────────────────────────────────────

    def __init__(self, parent, **kw):
        kw.setdefault("bg", _BG_ROOT)
        super().__init__(parent, **kw)

        self._columns: list = []
        self._header_frame = None
        self._header_labels: list = []
        self._rows: list = []          # [{"frame": Frame, "labels": [...], "bg": str}]
        self._cell_meta: dict = {}     # (row_idx, col_idx) -> meta dict
        self._on_click_cb = None
        self._sync_pending = False

        self._build_widgets()
        self._setup_scrollbar_styles()

    # ─── Widget Construction ──────────────────────────────────────────────

    def _build_widgets(self):
        """Build the scrollable table structure (canvas + scrollbars)."""
        # Horizontal scrollbar at the bottom of *self*
        self._h_scroll = ttk.Scrollbar(
            self, orient="horizontal",
            style="ColorTable.Horizontal.TScrollbar")
        self._h_scroll.pack(side="bottom", fill="x")

        # Body frame: canvas + vertical scrollbar
        body = tk.Frame(self, bg=_BG_ROOT)
        body.pack(fill="both", expand=True)

        self._v_scroll = ttk.Scrollbar(
            body, orient="vertical",
            style="ColorTable.Vertical.TScrollbar")
        self._v_scroll.pack(side="right", fill="y")

        self._canvas = tk.Canvas(
            body, bg=_BG_ROOT, highlightthickness=0, bd=0,
            xscrollcommand=self._h_scroll.set,
            yscrollcommand=self._v_scroll.set)
        self._canvas.pack(side="left", fill="both", expand=True)

        self._v_scroll.configure(command=self._canvas.yview)
        self._h_scroll.configure(command=self._canvas.xview)

        # Inner frame (holds header row + data rows) inside the canvas
        self._inner = tk.Frame(self._canvas, bg=_BG_ROOT)
        self._win_id = self._canvas.create_window(
            (0, 0), window=self._inner, anchor="nw")

        self._inner.bind("<Configure>", self._on_inner_configure)
        self._canvas.bind("<Configure>", self._on_canvas_configure)

        # Mousewheel scrolling
        self._canvas.bind("<Enter>", lambda _: self._bind_wheel())
        self._canvas.bind("<Leave>", lambda _: self._unbind_wheel())

    def _setup_scrollbar_styles(self):
        """Create ttk scrollbar styles that match the dark theme."""
        style = ttk.Style()
        # Ensure a theme that supports full colour customisation
        if style.theme_use() not in ("clam", "alt"):
            style.theme_use("clam")

        # ── Vertical ──
        style.configure(
            "ColorTable.Vertical.TScrollbar",
            troughcolor=_BG_SURFACE, background=_BG_ELEVATED,
            bordercolor=_BG_SURFACE, arrowcolor=_BG_SURFACE,
            relief="flat", width=8)
        style.map(
            "ColorTable.Vertical.TScrollbar",
            background=[("active", _BG_HOVER), ("!active", _BG_ELEVATED),
                        ("disabled", _BG_SURFACE)],
            arrowcolor=[("active", _BG_HOVER), ("disabled", _BG_SURFACE)])
        style.layout(
            "ColorTable.Vertical.TScrollbar",
            [("ColorTable.Vertical.Scrollbar.trough",
              {"sticky": "ns",
               "children": [("ColorTable.Vertical.Scrollbar.thumb",
                             {"expand": "1", "sticky": "nswe"})]})])

        # ── Horizontal ──
        style.configure(
            "ColorTable.Horizontal.TScrollbar",
            troughcolor=_BG_SURFACE, background=_BG_ELEVATED,
            bordercolor=_BG_SURFACE, arrowcolor=_BG_SURFACE,
            relief="flat", width=8)
        style.map(
            "ColorTable.Horizontal.TScrollbar",
            background=[("active", _BG_HOVER), ("!active", _BG_ELEVATED),
                        ("disabled", _BG_SURFACE)],
            arrowcolor=[("active", _BG_HOVER), ("disabled", _BG_SURFACE)])
        style.layout(
            "ColorTable.Horizontal.TScrollbar",
            [("ColorTable.Horizontal.Scrollbar.trough",
              {"sticky": "ew",
               "children": [("ColorTable.Horizontal.Scrollbar.thumb",
                             {"expand": "1", "sticky": "nswe"})]})])

    # ─── Scrolling ────────────────────────────────────────────────────────

    def _bind_wheel(self):
        self._canvas.bind_all("<MouseWheel>", self._on_wheel)
        self._canvas.bind_all("<Shift-MouseWheel>", self._on_shift_wheel)

    def _unbind_wheel(self):
        self._canvas.unbind_all("<MouseWheel>")
        self._canvas.unbind_all("<Shift-MouseWheel>")

    def _on_wheel(self, event):
        self._canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_shift_wheel(self, event):
        self._canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

    # ─── Canvas / Inner Frame Synchronisation ─────────────────────────────

    def _on_canvas_configure(self, event):
        self._defer_sync()

    def _on_inner_configure(self, event):
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))
        self._defer_sync()

    def _defer_sync(self):
        """Schedule a single width/scroll-region sync on the next idle cycle."""
        if self._sync_pending:
            return
        self._sync_pending = True
        self._canvas.after_idle(self._do_sync)

    def _do_sync(self):
        """Adjust inner-frame width so columns fill the canvas (or scroll)."""
        self._sync_pending = False
        self._inner.update_idletasks()
        cw = self._canvas.winfo_width()
        if cw < 2:
            return
        iw = self._inner.winfo_reqwidth()
        desired = max(cw, iw)
        # Avoid redundant configure (prevents event loops)
        try:
            current = int(self._canvas.itemcget(self._win_id, "width"))
        except (ValueError, TypeError):
            current = 0
        if abs(current - desired) > 1:
            self._canvas.itemconfigure(self._win_id, width=desired)
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    # ─── Column Configuration ─────────────────────────────────────────────

    def set_columns(self, columns):
        """
        Define (or redefine) table columns and rebuild the header row.

        Args:
            columns: list of dicts, each with keys:

                * **title** *(str)* – header text
                * **width** *(int)* – minimum column width in pixels
                * **anchor** *(str)* – ``"w"``, ``"center"`` or ``"e"``
                * **stretch** *(bool)* – expand to fill extra horizontal space
        """
        self._columns = list(columns)
        self._rebuild_header()

    def _rebuild_header(self):
        """Destroy and recreate the header row."""
        if self._header_frame is not None and self._header_frame.winfo_exists():
            self._header_frame.destroy()

        self._header_frame = tk.Frame(self._inner, bg=_BG_ELEVATED)
        # Always place the header at grid row 0 inside _inner
        self._header_frame.grid(row=0, column=0, sticky="ew")
        self._inner.columnconfigure(0, weight=1)

        self._header_labels = []
        for col_idx, col in enumerate(self._columns):
            anchor = col.get("anchor", "center")
            lbl = tk.Label(
                self._header_frame,
                text=col.get("title", ""),
                font=(_FAMILY, 9, "bold"),
                fg=_TEXT_SECONDARY,
                bg=_BG_ELEVATED,
                anchor=anchor,
                padx=8,
                pady=6,
            )
            lbl.grid(row=0, column=col_idx, sticky="nsew")
            self._header_labels.append(lbl)

        # Column sizing
        for col_idx, col in enumerate(self._columns):
            min_w = col.get("width", 80)
            stretch = col.get("stretch", False)
            self._header_frame.columnconfigure(
                col_idx, minsize=min_w, weight=1 if stretch else 0)

    # ─── Data Operations ──────────────────────────────────────────────────

    def clear(self):
        """Remove all data rows (header is preserved)."""
        for row_data in self._rows:
            if row_data["frame"].winfo_exists():
                row_data["frame"].destroy()
        self._rows.clear()
        self._cell_meta.clear()

    def update_cell(self, row_idx, col_idx, text=None, fg=None, meta=None):
        """
        Update the display and metadata of a single cell.

        Args:
            row_idx: zero-based row index (0 = first data row).
            col_idx: zero-based column index (0 = first data column).
            text: new cell text, or ``None`` to keep unchanged.
            fg: new foreground colour, or ``None`` to keep unchanged.
            meta: new metadata dict stored for click callbacks.
                  If provided, **replaces** any existing meta for this cell.
        """
        if row_idx < len(self._rows) and col_idx < len(self._rows[row_idx]["labels"]):
            lbl = self._rows[row_idx]["labels"][col_idx]
            if not lbl.winfo_exists():
                return
            if text is not None:
                lbl.configure(text=text)
            if fg is not None:
                lbl.configure(fg=fg)
            if meta is not None:
                self._cell_meta[(row_idx, col_idx)] = meta

    def insert_row(self, cells, row_tag="row_even"):
        """
        Append one data row.

        Args:
            cells: list of cell descriptors.  Each item is either a plain
                string or a dict with keys:

                * **text** *(str)* – cell text
                * **fg** *(str)* – foreground colour (default TEXT_PRIMARY)
                * **bg** *(str)* – background colour (default from *row_tag*)
                * **meta** *(dict)* – arbitrary metadata passed to click callback

            row_tag: ``"row_even"`` or ``"row_odd"`` – selects the alternating
                row background colour.
        """
        bg_color = _BG_SURFACE if row_tag == "row_even" else _BG_ELEVATED

        row_frame = tk.Frame(self._inner, bg=bg_color)
        row_idx = len(self._rows)
        # Data rows start at grid row 1 (row 0 is the header)
        row_frame.grid(row=row_idx + 1, column=0, sticky="ew")

        labels = []
        for col_idx, cell in enumerate(cells):
            if isinstance(cell, str):
                cell = {"text": cell}

            fg = cell.get("fg", _TEXT_PRIMARY)
            bg = cell.get("bg", bg_color)

            anchor = "w"
            if col_idx < len(self._columns):
                anchor = self._columns[col_idx].get("anchor", "center")

            lbl = tk.Label(
                row_frame,
                text=cell.get("text", ""),
                font=(_FAMILY, 9),
                fg=fg,
                bg=bg,
                anchor=anchor,
                padx=8,
                pady=4,
            )
            lbl.grid(row=0, column=col_idx, sticky="nsew")
            labels.append(lbl)

            # Per-cell metadata
            meta = cell.get("meta")
            if meta is not None:
                self._cell_meta[(row_idx, col_idx)] = meta

            # Click binding
            lbl.bind(
                "<Button-1>",
                lambda _e, r=row_idx, c=col_idx: self._on_label_click(r, c))

        # Mirror column sizing from the header
        for col_idx, col in enumerate(self._columns):
            min_w = col.get("width", 80)
            stretch = col.get("stretch", False)
            row_frame.columnconfigure(
                col_idx, minsize=min_w, weight=1 if stretch else 0)

        # Row-level hover
        for lbl in labels:
            lbl.bind("<Enter>",
                     lambda _e, ri=row_idx: self._on_row_enter(ri))
            lbl.bind("<Leave>",
                     lambda _e, ri=row_idx: self._on_row_leave(ri))
        row_frame.bind("<Enter>",
                       lambda _e, ri=row_idx: self._on_row_enter(ri))
        row_frame.bind("<Leave>",
                       lambda _e, ri=row_idx: self._on_row_leave(ri))

        self._rows.append({
            "frame": row_frame,
            "labels": labels,
            "bg": bg_color,
        })

    # ─── Hover Effects ────────────────────────────────────────────────────

    def _on_row_enter(self, row_idx):
        if row_idx < len(self._rows):
            for lbl in self._rows[row_idx]["labels"]:
                if lbl.winfo_exists():
                    lbl.configure(bg=_BG_HOVER)

    def _on_row_leave(self, row_idx):
        if row_idx < len(self._rows):
            bg = self._rows[row_idx]["bg"]
            for lbl in self._rows[row_idx]["labels"]:
                if lbl.winfo_exists():
                    lbl.configure(bg=bg)

    # ─── Click Handling ───────────────────────────────────────────────────

    def _on_label_click(self, row_idx, col_idx):
        if self._on_click_cb:
            meta = self._cell_meta.get((row_idx, col_idx))
            if meta is not None:
                self._on_click_cb(meta)

    def on_cell_click(self, callback):
        """
        Register a cell-click callback.

        *callback* receives the ``meta`` dict that was stored on the clicked
        cell when ``insert_row`` was called.
        """
        self._on_click_cb = callback