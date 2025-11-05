from dataclasses import dataclass
from typing import List, Optional

from wcwidth import wcswidth


# Line styles consistent with framework.cli_format, but this TUI omits the right-side closing "│"
line_styles = {
    "normal": {"┌": "┌", "─": "─", "┐": "┐", "│": "│", "├": "├", "┤": "┤", "└": "└", "┘": "┘"},
    "bold": {"┌": "┏", "─": "━", "┐": "┓", "│": "┃", "├": "┣", "┤": "┫", "└": "┗", "┘": "┛"},
    "double": {"┌": "╔", "─": "═", "┐": "╗", "│": "║", "├": "╠", "┤": "╣", "└": "╚", "┘": "╝"},
    # Keep dotted visuals; right-side vertical is still omitted on content lines
    "dotted": {"┌": "┌", "─": "╌", "┐": "┐", "│": "╎", "├": "├", "┤": "┤", "└": "└", "┘": "┘"},
    "curly": {"┌": "╭", "─": "─", "┐": "╮", "│": "│", "├": "├", "┤": "┤", "└": "╰", "┘": "╯"},
}


def _display_width(text: str) -> int:
    """Return display width accounting for wide/emoji characters (fallback to len on -1)."""
    width = wcswidth(text)
    return width if width >= 0 else len(text)


@dataclass
class TableRow:
    """Represents a content row for the TUI table."""

    row: str = ""
    padding_adjust: int = 0

    def get_display_width(self) -> int:
        return _display_width(self.row)

    def get_padding_len(self, inner_width: int) -> int:
        width = self.get_display_width()
        pad = inner_width - width + self.padding_adjust
        return pad if pad > 0 else 0

    def left_justified(self, inner_width: int) -> str:
        pad = self.get_padding_len(inner_width)
        return f"{self.row}{' ' * pad}"

    def centered(self, inner_width: int) -> str:
        width = self.get_display_width()
        total_pad = inner_width - width + self.padding_adjust
        if total_pad <= 0:
            return self.row
        left = total_pad // 2
        right = total_pad - left
        return f"{' ' * left}{self.row}{' ' * right}"


class TableFormatter:
    """Formats data into a table-like structure for terminal output.

    Differences vs framework.cli_format.TableFormatter:
    - Omits the right-hand closing vertical bar (│) on content lines.
    - Skips any logic related to that right-side closing bar.
    - Supports content fitting via truncation (default) or wrapping.
    """

    def __init__(
        self,
        line_style_name: str = "normal",
        table_width: int = 100,
        fit_mode: str = "truncate",  # "truncate" | "wrap"
        ellipsis: str = "…",
    ) -> None:
        if line_style_name not in line_styles:
            raise ValueError(
                f"Invalid style: {line_style_name}. Available styles: {', '.join(line_styles.keys())}"
            )

        if fit_mode not in {"truncate", "wrap"}:
            raise ValueError("fit_mode must be either 'truncate' or 'wrap'")

        self._style_name = line_style_name
        self._table_width = max(table_width, 20)
        self._fit_mode = fit_mode
        self._ellipsis = ellipsis

        self._rows: List[TableRow] = []
        self._title: Optional[TableRow] = None

    def add_row(self, row: TableRow, pos: Optional[int] = None) -> None:
        if pos is not None:
            self._rows.insert(pos, row)
        else:
            self._rows.append(row)

    def set_title(self, title: str) -> None:
        self._title = TableRow(title)

    def _inner_width(self) -> int:
        """Compute inner width based on configured table width.

        Inner width excludes the two corner characters on the top/bottom lines.
        """
        return max(self._table_width - 2, 18)

    def _truncate_to_width(self, text: str, max_width: int) -> str:
        """Truncate text to fit display width, appending ellipsis if truncated."""
        if _display_width(text) <= max_width:
            return text

        ell_w = _display_width(self._ellipsis)
        if ell_w >= max_width:
            # Not enough space for ellipsis; hard cut to width
            return self._cut_to_width(text, max_width)

        cut_width = max_width - ell_w
        cut = self._cut_to_width(text, cut_width)
        return f"{cut}{self._ellipsis}"

    def _wrap_to_width(self, text: str, max_width: int) -> List[str]:
        """Wrap text by display width; simple greedy char-based wrap respecting wide chars."""
        if max_width <= 0:
            return [text]

        lines: List[str] = []
        current: List[str] = []
        cur_w = 0
        for ch in text:
            ch_w = wcswidth(ch)
            if ch_w < 0:
                ch_w = 1
            if cur_w + ch_w > max_width and current:
                lines.append("".join(current))
                current = [ch]
                cur_w = ch_w
            else:
                current.append(ch)
                cur_w += ch_w
        if current:
            lines.append("".join(current))
        if not lines:
            lines = [""]
        return lines

    def _cut_to_width(self, text: str, max_width: int) -> str:
        out: List[str] = []
        cur_w = 0
        for ch in text:
            ch_w = wcswidth(ch)
            if ch_w < 0:
                ch_w = 1
            if cur_w + ch_w > max_width:
                break
            out.append(ch)
            cur_w += ch_w
        return "".join(out)

    def _fit_lines(self, text: str, inner_width: int) -> List[str]:
        if self._fit_mode == "truncate":
            return [self._truncate_to_width(text, inner_width)]
        return self._wrap_to_width(text, inner_width)

    def _pad_left(self, text: str, inner_width: int) -> str:
        w = _display_width(text)
        pad = inner_width - w
        return f"{text}{' ' * (pad if pad > 0 else 0)}"

    def _pad_center(self, text: str, inner_width: int) -> str:
        w = _display_width(text)
        total = inner_width - w
        if total <= 0:
            return text
        left = total // 2
        right = total - left
        return f"{' ' * left}{text}{' ' * right}"

    def render(self) -> str:
        style = line_styles[self._style_name]

        inner_width = self._inner_width()
        top = f"{style['┌']}{style['─'] * inner_width}{style['┐']}"
        mid = f"{style['├']}{style['─'] * inner_width}{style['┤']}"
        bot = f"{style['└']}{style['─'] * inner_width}{style['┘']}"

        lines: List[str] = [top]

        # Title line(s) (left border only, no right-side │)
        if self._title and self._title.row != "":
            for seg in self._fit_lines(self._title.row, inner_width):
                lines.append(f"{style['│']}{self._pad_center(seg, inner_width)}")
            lines.append(mid)

        # Content rows (left border only, no right-side │)
        for r in self._rows:
            segs = self._fit_lines(r.row, inner_width)
            for seg in segs:
                lines.append(f"{style['│']}{self._pad_left(seg, inner_width)}")

        lines.append(bot)
        return "\n".join(lines)


__all__ = ["TableRow", "TableFormatter", "line_styles"]
