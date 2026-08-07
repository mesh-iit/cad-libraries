"""
ProductionDocExporter - main.py

Generates a Creo auto_trail.txt from a missing.txt/list of codes.

Workflow:
1. Ask whether to use the default ProductionDocCollector missing.txt.
2. Otherwise let the user select any .txt file.
3. Let the user select the CAD source root folder.
4. Clean/create: C:\\Users\\<user>\\Documents\\ProductionDocExporter_Output
5. Parse codes from the input text.
6. Search recursively for source files with Creo version suffix .1:
   CODE.prt.1, CODE.asm.1, CODE.drw.1
7. Warn, but do not stop, if versions > .1 are found.
8. Generate auto_trail.txt and report.txt.

The generated trail is meant to be launched manually from Creo.
"""

from __future__ import annotations

import datetime as _dt
import re
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import tkinter as tk
from tkinter import filedialog, messagebox


# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

APP_NAME = "ProductionDocExporter"
COLLECTOR_OUTPUT_DIRNAME = "ProductionDocCollector_Output"
EXPORTER_OUTPUT_DIRNAME = "ProductionDocExporter_Output"
DEFAULT_MISSING_FILENAME = "missing.txt"
TRAIL_FILENAME = "auto_trail.txt"
REPORT_FILENAME = "report.txt"

# Creo file type IDs observed from the validated trail/mapkeys.
CREO_TYPE_STEP = "db_539"
CREO_TYPE_STL = "db_549"
CREO_TYPE_PDF = "db_617"

# General-purpose STL settings selected by Lorenzo.
STL_CHORD_HEIGHT = "0.03"
STL_ANGLE_CONTROL = "0.85"

# Object code pattern examples:
#   IC_099_P_004_REV_0
#   IC_033_P_001_REV_A2
#   ECUB_003_P_048_REV_B1
#   IC_099_P_004
CODE_PATTERN = re.compile(
    r"\b(?P<base>[A-Z][A-Z0-9]*_\d{3}_[A-Z]_\d{3})(?:_REV_(?P<rev>[A-Z0-9]+))?\b",
    re.IGNORECASE,
)

# Creo versioned source file:
#   ic_033_p_001.prt.1
#   ic_033_p_001.asm.2
#   ic_033_p_001.drw.3
SOURCE_FILE_PATTERN = re.compile(
    r"^(?P<base>[a-z0-9]+_\d{3}_[a-z]_\d{3})\.(?P<ext>prt|asm|drw)\.(?P<ver>\d+)$",
    re.IGNORECASE,
)


# -----------------------------------------------------------------------------
# Data models
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class RequestedCode:
    base: str
    revision: Optional[str] = None

    @property
    def output_stem(self) -> str:
        if self.revision:
            return f"{self.base}_REV_{self.revision}"
        return self.base

    @property
    def has_revision(self) -> bool:
        return bool(self.revision)


@dataclass
class FoundSources:
    model_path: Optional[Path] = None
    model_kind: Optional[str] = None  # "prt" or "asm"
    drawing_path: Optional[Path] = None
    purge_warnings: List[str] = field(default_factory=list)
    source_warnings: List[str] = field(default_factory=list)


@dataclass
class ExportPlanItem:
    code: RequestedCode
    sources: FoundSources


# -----------------------------------------------------------------------------
# Small helpers
# -----------------------------------------------------------------------------


def documents_dir() -> Path:
    return Path.home() / "Documents"


def default_missing_path() -> Path:
    return documents_dir() / COLLECTOR_OUTPUT_DIRNAME / DEFAULT_MISSING_FILENAME


def exporter_output_dir() -> Path:
    return documents_dir() / EXPORTER_OUTPUT_DIRNAME


def creo_path(path: Path) -> str:
    """Return a path formatted for Creo trail commands."""
    return str(path).replace("\\", "\\\\")


def clean_output_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def read_text_file(path: Path) -> str:
    """Read text robustly enough for common Windows-generated TXT files."""
    encodings = ("utf-8-sig", "utf-8", "cp1252", "latin-1")
    last_exc: Optional[Exception] = None
    for enc in encodings:
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError as exc:
            last_exc = exc
    raise RuntimeError(f"Could not read text file: {path}\nLast error: {last_exc}")


# -----------------------------------------------------------------------------
# Input parsing
# -----------------------------------------------------------------------------


def parse_requested_codes(text: str) -> List[RequestedCode]:
    """
    Extract all object codes from arbitrary text.

    This intentionally ignores headers, paths, blank lines, separators, etc.
    Duplicates are removed while preserving first occurrence.
    """
    seen: set[str] = set()
    codes: List[RequestedCode] = []

    for match in CODE_PATTERN.finditer(text.upper()):
        base = match.group("base").upper()
        rev = match.group("rev")
        key = f"{base}_REV_{rev}" if rev else base
        if key in seen:
            continue
        seen.add(key)
        codes.append(RequestedCode(base=base, revision=rev.upper() if rev else None))

    return codes


# -----------------------------------------------------------------------------
# Source indexing and search
# -----------------------------------------------------------------------------


def build_source_index(root: Path) -> Dict[str, List[Path]]:
    """Index files under root by lower-case filename."""
    index: Dict[str, List[Path]] = {}
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        name = path.name.lower()
        if SOURCE_FILE_PATTERN.match(name):
            index.setdefault(name, []).append(path)
    for paths in index.values():
        paths.sort(key=lambda p: str(p).lower())
    return index


def choose_one(paths: List[Path]) -> Optional[Path]:
    return paths[0] if paths else None


def is_probably_assembly_code(base: str) -> bool:
    """
    Legacy rule observed in the old script:
    _A_, _G_, _R_ codes are searched as assemblies first.
    Everything else is searched as part first.
    """
    upper = base.upper()
    return any(token in upper for token in ("_A_", "_G_", "_R_"))


def find_sources_for_code(code: RequestedCode, index: Dict[str, List[Path]]) -> FoundSources:
    base_l = code.base.lower()
    result = FoundSources()

    prt_name = f"{base_l}.prt.1"
    asm_name = f"{base_l}.asm.1"
    drw_name = f"{base_l}.drw.1"

    prt_paths = index.get(prt_name, [])
    asm_paths = index.get(asm_name, [])
    drw_paths = index.get(drw_name, [])

    # Select model according to expected object class, but still tolerate the
    # other kind as fallback.
    if is_probably_assembly_code(code.base):
        if asm_paths:
            result.model_path = choose_one(asm_paths)
            result.model_kind = "asm"
        elif prt_paths:
            result.model_path = choose_one(prt_paths)
            result.model_kind = "prt"
            result.source_warnings.append("Expected ASM by code class, but only PRT was found.")
    else:
        if prt_paths:
            result.model_path = choose_one(prt_paths)
            result.model_kind = "prt"
        elif asm_paths:
            result.model_path = choose_one(asm_paths)
            result.model_kind = "asm"
            result.source_warnings.append("Expected PRT by code class, but only ASM was found.")

    if prt_paths and asm_paths:
        result.source_warnings.append("Both PRT.1 and ASM.1 were found; exported the expected-priority model only.")

    if len(prt_paths) > 1:
        result.source_warnings.append(f"Multiple PRT.1 files found; using: {prt_paths[0]}")
    if len(asm_paths) > 1:
        result.source_warnings.append(f"Multiple ASM.1 files found; using: {asm_paths[0]}")
    if len(drw_paths) > 1:
        result.source_warnings.append(f"Multiple DRW.1 files found; using: {drw_paths[0]}")

    result.drawing_path = choose_one(drw_paths)

    # Purge warnings: versions > .1 exist. Export continues using .1.
    prefix = f"{base_l}."
    for filename, paths in index.items():
        if not filename.startswith(prefix):
            continue
        m = SOURCE_FILE_PATTERN.match(filename)
        if not m:
            continue
        if m.group("base").lower() != base_l:
            continue
        ver = int(m.group("ver"))
        if ver > 1:
            for p in paths:
                result.purge_warnings.append(str(p))

    result.purge_warnings.sort(key=str.lower)
    return result


# -----------------------------------------------------------------------------
# Trail generation
# -----------------------------------------------------------------------------


def trail_header() -> List[str]:
    return [
        "!trail file version No. 1600",
        f"!automatically generated by {APP_NAME}",
        f"!generated at {_dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    ]


def trail_open_file(source_path: Path) -> List[str]:
    return [
        "~ Activate `main_dlg_cur` `main_dlg_cur`",
        "~ Command `ProCmdModelOpen`",
        f"~ Update `file_open` `Inputname` `{creo_path(source_path)}`",
        "~ Activate `file_open` `Inputname`",
    ]


def trail_close_and_erase() -> List[str]:
    return [
        "~ Command `ProCmdWinCloseGroup`",
        "~ Command `ProCmdModelEraseNotDisp`",
        "~ Activate `file_erase_nd` `ok_pb`",
    ]


def trail_export_step(target_stem: Path) -> List[str]:
    return [
        "~ Command `ProCmdModelSaveAs`",
        "~ Open `file_saveas` `type_option`",
        f"~ Select `file_saveas` `type_option` 1 `{CREO_TYPE_STEP}`",
        f"~ Update `file_saveas` `Inputname` `{creo_path(target_stem)}`",
        "~ Activate `file_saveas` `Inputname`",
        "~ Activate `intf_export` `OkPushBtn`",
    ]


def trail_export_stl(target_stem: Path) -> List[str]:
    return [
        "~ Command `ProCmdModelSaveAs`",
        "~ Open `file_saveas` `type_option`",
        f"~ Select `file_saveas` `type_option` 1 `{CREO_TYPE_STL}`",
        f"~ Update `file_saveas` `Inputname` `{creo_path(target_stem)}`",
        "~ Activate `file_saveas` `Inputname`",
        f"~ Update `export_slice` `ChordHeightPanel` `{STL_CHORD_HEIGHT}`",
        "~ FocusOut `export_slice` `ChordHeightPanel`",
        f"~ Update `export_slice` `AngleControlPanel` `{STL_ANGLE_CONTROL}`",
        "~ FocusOut `export_slice` `AngleControlPanel`",
        "~ Activate `export_slice` `OK`",
    ]


def trail_export_pdf(target_stem: Path) -> List[str]:
    return [
        "~ Command `ProCmdModelSaveAs`",
        "~ Open `file_saveas` `type_option`",
        f"~ Select `file_saveas` `type_option` 1 `{CREO_TYPE_PDF}`",
        "~ Activate `file_saveas` `file_saveas`",
        f"~ Update `file_saveas` `Inputname` `{creo_path(target_stem)}`",
        "~ Activate `file_saveas` `Inputname`",
        "~ Open `intf_profile` `pdf_export.pdf_raster_dpi`",
        "~ Select `intf_profile` `pdf_export.pdf_raster_dpi` 1 `600`",
        "~ Activate `intf_profile` `pdf_export.pdf_launch_viewer` 0",
        "~ Activate `intf_profile` `OkPshBtn`",
    ]


def generate_trail(plan: List[ExportPlanItem], output_dir: Path) -> str:
    lines: List[str] = trail_header()

    for item in plan:
        target_stem = output_dir / item.code.output_stem

        if item.sources.model_path:
            lines.extend(trail_open_file(item.sources.model_path))
            lines.extend(trail_export_step(target_stem))
            lines.extend(trail_export_stl(target_stem))
            lines.extend(trail_close_and_erase())

        if item.sources.drawing_path:
            lines.extend(trail_open_file(item.sources.drawing_path))
            lines.extend(trail_export_pdf(target_stem))
            lines.extend(trail_close_and_erase())

    return "\n".join(lines) + "\n"


# -----------------------------------------------------------------------------
# Report generation
# -----------------------------------------------------------------------------


def generate_report(
    input_file: Path,
    cad_root: Path,
    output_dir: Path,
    requested_codes: List[RequestedCode],
    plan: List[ExportPlanItem],
) -> str:
    now = _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    model_jobs = sum(1 for item in plan if item.sources.model_path)
    drawing_jobs = sum(1 for item in plan if item.sources.drawing_path)
    no_rev = [item.code for item in plan if not item.code.has_revision]
    missing_model = [item for item in plan if not item.sources.model_path]
    missing_drw = [item for item in plan if not item.sources.drawing_path]
    purge_items = [item for item in plan if item.sources.purge_warnings]
    source_warning_items = [item for item in plan if item.sources.source_warnings]

    lines: List[str] = []
    add = lines.append

    add("=" * 72)
    add(f"{APP_NAME} report")
    add("=" * 72)
    add(f"Generated at: {now}")
    add(f"Input file:   {input_file}")
    add(f"CAD root:     {cad_root}")
    add(f"Output dir:   {output_dir}")
    add("")

    add("SUMMARY")
    add("-" * 72)
    add(f"Requested codes:       {len(requested_codes)}")
    add(f"Model export jobs:     {model_jobs}  (STEP + STL)")
    add(f"Drawing export jobs:   {drawing_jobs}  (PDF)")
    add(f"Codes without REV:     {len(no_rev)}")
    add(f"Missing model sources: {len(missing_model)}")
    add(f"Missing drawings:      {len(missing_drw)}")
    add(f"Purge warnings:        {len(purge_items)}")
    add("")

    add("REQUESTED CODES")
    add("-" * 72)
    for code in requested_codes:
        if code.revision:
            add(f"{code.base}_REV_{code.revision}")
        else:
            add(f"{code.base}    [WARNING: no revision specified]")
    add("")

    add("EXPORT PLAN")
    add("-" * 72)
    for item in plan:
        code = item.code
        add(f"{code.output_stem}")
        if item.sources.model_path:
            add(f"  MODEL ({item.sources.model_kind}): {item.sources.model_path}")
            add(f"  WILL EXPORT: {code.output_stem}.stp")
            add(f"  WILL EXPORT: {code.output_stem}.stl")
        else:
            add("  MODEL: NOT FOUND")
        if item.sources.drawing_path:
            add(f"  DRAWING: {item.sources.drawing_path}")
            add(f"  WILL EXPORT: {code.output_stem}.pdf")
        else:
            add("  DRAWING: NOT FOUND")
        if not code.has_revision:
            add("  WARNING: No revision specified; output name will not contain REV.")
        for warn in item.sources.source_warnings:
            add(f"  WARNING: {warn}")
        add("")

    add("PURGE WARNINGS")
    add("-" * 72)
    if not purge_items:
        add("None")
    else:
        add("WARNING: Purge not done properly. Files with version > .1 were found.")
        add("Export trail still uses .1 sources only.")
        add("")
        for item in purge_items:
            add(item.code.output_stem)
            for p in item.sources.purge_warnings:
                add(f"  found: {p}")
            add("")
    add("")

    add("MISSING SOURCES")
    add("-" * 72)
    if not missing_model and not missing_drw:
        add("None")
    else:
        for item in plan:
            missing_bits = []
            if not item.sources.model_path:
                missing_bits.append("model source (.prt.1/.asm.1)")
            if not item.sources.drawing_path:
                missing_bits.append("drawing source (.drw.1)")
            if missing_bits:
                add(f"{item.code.output_stem}: missing {', '.join(missing_bits)}")
    add("")

    add("HOW TO RUN")
    add("-" * 72)
    add("1. Open Creo from the official company shortcut.")
    add("2. In Creo, launch the generated trail file:")
    add(f"   {output_dir / TRAIL_FILENAME}")
    add("3. When Creo finishes, generated PDF/STP/STL files should be in:")
    add(f"   {output_dir}")
    add("")

    return "\n".join(lines) + "\n"


# -----------------------------------------------------------------------------
# GUI flow
# -----------------------------------------------------------------------------


def ask_input_file(root: tk.Tk) -> Optional[Path]:
    default_path = default_missing_path()

    use_default = messagebox.askyesno(
        APP_NAME,
        "Should I use the default path for the missing.txt file?\n\n"
        f"{default_path}",
        parent=root,
    )

    if use_default:
        if default_path.exists():
            return default_path
        messagebox.showwarning(
            APP_NAME,
            "Default missing.txt not found.\n\nPlease select a TXT file manually.",
            parent=root,
        )

    selected = filedialog.askopenfilename(
        title="Select input TXT file",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        parent=root,
    )
    if not selected:
        return None
    return Path(selected)


def ask_cad_root(root: tk.Tk) -> Optional[Path]:
    selected = filedialog.askdirectory(
        title="Select CAD source root folder",
        parent=root,
    )
    if not selected:
        return None
    return Path(selected)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def run() -> int:
    root = tk.Tk()
    root.withdraw()

    try:
        input_file = ask_input_file(root)
        if not input_file:
            return 1

        cad_root = ask_cad_root(root)
        if not cad_root:
            return 1
        if not cad_root.exists() or not cad_root.is_dir():
            messagebox.showerror(APP_NAME, f"Invalid CAD root folder:\n{cad_root}", parent=root)
            return 1

        input_text = read_text_file(input_file)
        requested_codes = parse_requested_codes(input_text)
        if not requested_codes:
            messagebox.showerror(
                APP_NAME,
                "No valid object codes were found in the selected TXT file.",
                parent=root,
            )
            return 1

        out_dir = exporter_output_dir()
        clean_output_dir(out_dir)

        index = build_source_index(cad_root)
        plan = [ExportPlanItem(code=c, sources=find_sources_for_code(c, index)) for c in requested_codes]

        trail_text = generate_trail(plan, out_dir)
        report_text = generate_report(input_file, cad_root, out_dir, requested_codes, plan)

        trail_path = out_dir / TRAIL_FILENAME
        report_path = out_dir / REPORT_FILENAME
        trail_path.write_text(trail_text, encoding="utf-8")
        report_path.write_text(report_text, encoding="utf-8")

        purge_count = sum(1 for item in plan if item.sources.purge_warnings)
        no_rev_count = sum(1 for item in plan if not item.code.has_revision)
        missing_model_count = sum(1 for item in plan if not item.sources.model_path)
        missing_drw_count = sum(1 for item in plan if not item.sources.drawing_path)

        msg_lines = [
            "Trail generated successfully.",
            "",
            f"Codes parsed: {len(requested_codes)}",
            f"Output folder:",
            f"{out_dir}",
            "",
            f"Trail:",
            f"{trail_path}",
            "",
            f"Report:",
            f"{report_path}",
        ]

        warnings = []
        if purge_count:
            warnings.append(f"Purge warnings: {purge_count}")
        if no_rev_count:
            warnings.append(f"Codes without REV: {no_rev_count}")
        if missing_model_count:
            warnings.append(f"Missing model sources: {missing_model_count}")
        if missing_drw_count:
            warnings.append(f"Missing drawings: {missing_drw_count}")

        if warnings:
            msg_lines.extend(["", "Warnings:"])
            msg_lines.extend(f"- {w}" for w in warnings)
            msg_lines.append("")
            msg_lines.append("See report.txt for details.")
            messagebox.showwarning(APP_NAME, "\n".join(msg_lines), parent=root)
        else:
            messagebox.showinfo(APP_NAME, "\n".join(msg_lines), parent=root)

        return 0

    except Exception as exc:
        messagebox.showerror(APP_NAME, f"Unexpected error:\n\n{exc}", parent=root)
        return 1
    finally:
        root.destroy()


if __name__ == "__main__":
    sys.exit(run())
