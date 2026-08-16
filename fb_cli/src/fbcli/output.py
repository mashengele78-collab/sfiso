from __future__ import annotations

import csv
import io
import json
from typing import Any

from rich.console import Console
from rich.table import Table

console = Console()
err_console = Console(stderr=True)

FORMATS = ("table", "json", "csv")


def _flat(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def _truncate(text: str, width: int) -> str:
    return text if len(text) <= width else text[: width - 1] + "…"


def emit(
    rows: list[dict[str, Any]],
    *,
    fmt: str = "table",
    columns: list[str] | None = None,
    title: str | None = None,
    empty: str = "No results.",
    max_width: int = 60,
) -> None:
    """Render a list of records as a table, JSON or CSV."""
    if fmt == "json":
        console.print_json(json.dumps(rows, ensure_ascii=False, default=str))
        return

    if not rows:
        if fmt == "csv":
            return
        console.print(f"[yellow]{empty}[/yellow]")
        return

    cols = columns or list(dict.fromkeys(k for row in rows for k in row))

    if fmt == "csv":
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=cols, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({c: _flat(row.get(c)) for c in cols})
        console.print(buf.getvalue().rstrip("\n"), highlight=False, markup=False)
        return

    table = Table(title=title, header_style="bold cyan", show_lines=False)
    for col in cols:
        table.add_column(col, overflow="fold")
    for row in rows:
        table.add_row(*[_truncate(_flat(row.get(c)), max_width) for c in cols])
    console.print(table)


def emit_object(obj: dict[str, Any], *, fmt: str = "table", title: str | None = None) -> None:
    """Render a single object as key/value pairs (or raw JSON/CSV)."""
    if fmt == "json":
        console.print_json(json.dumps(obj, ensure_ascii=False, default=str))
        return
    if fmt == "csv":
        emit([obj], fmt="csv")
        return
    table = Table(title=title, header_style="bold cyan", show_header=False, box=None)
    table.add_column("field", style="bold")
    table.add_column("value", overflow="fold")
    for key, value in obj.items():
        table.add_row(key, _flat(value))
    console.print(table)


def success(message: str) -> None:
    console.print(f"[green]✓[/green] {message}")


def warn(message: str) -> None:
    console.print(f"[yellow]![/yellow] {message}")


def info(message: str) -> None:
    console.print(f"[dim]{message}[/dim]")
