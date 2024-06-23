from pathlib import Path

ENCODINGS_FOLDER = Path(__file__).parent / "encodings"
CHECK = Path(ENCODINGS_FOLDER, "check_trace.lp").as_posix()
SOLVE_STATIC = Path(ENCODINGS_FOLDER, "solve_static.lp").as_posix()
SOLVE_INCREMENTAL = Path(ENCODINGS_FOLDER, "solve_incremental.lp").as_posix()
REYNOLDS = Path(ENCODINGS_FOLDER, "reynolds.lp").as_posix()
