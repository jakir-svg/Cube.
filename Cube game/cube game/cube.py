# Example corrected code
# Assumes you have a Cube class from a cube library or your own implementation

class Cube:
    """A minimal 3x3 cube model supporting U, D, L, R, F, and B turns."""

    _NORMALS = {
        "U": (0, 1, 0),
        "D": (0, -1, 0),
        "L": (-1, 0, 0),
        "R": (1, 0, 0),
        "F": (0, 0, 1),
        "B": (0, 0, -1),
    }

    def __init__(self):
        self._solved = {}
        for face, normal in self._NORMALS.items():
            for row in range(-1, 2):
                for column in range(-1, 2):
                    if face in "UD":
                        position = (column, normal[1], row)
                    elif face in "LR":
                        position = (normal[0], row, column)
                    else:
                        position = (column, row, normal[2])
                    self._solved[(position, normal)] = face
        self.state = self._solved.copy()

    @staticmethod
    def _rotate(vector, axis, quarter_turns):
        result = vector
        for _ in range(quarter_turns % 4):
            dot = sum(a * b for a, b in zip(result, axis))
            cross = (
                axis[1] * result[2] - axis[2] * result[1],
                axis[2] * result[0] - axis[0] * result[2],
                axis[0] * result[1] - axis[1] * result[0],
            )
            result = tuple(dot * a - c for a, c in zip(axis, cross))
        return result

    def turn(self, move):
        """Apply a face turn such as R, U', or F2."""
        if not move or move[0] not in self._NORMALS or move[1:] not in ("", "'", "2"):
            raise ValueError(f"Invalid move: {move!r}")

        face = move[0]
        axis = self._NORMALS[face]
        quarter_turns = {"": 1, "'": 3, "2": 2}[move[1:]]
        next_state = self.state.copy()

        for (position, normal), sticker in self.state.items():
            if sum(a * b for a, b in zip(position, axis)) == 1:
                rotated_position = self._rotate(position, axis, quarter_turns)
                rotated_normal = self._rotate(normal, axis, quarter_turns)
                next_state[(rotated_position, rotated_normal)] = sticker

        self.state = next_state

    def solved(self):
        return self.state == self._solved


def count_until_solved(seq):
    """
    Apply moves repeatedly until the cube is solved.
    seq: string of moves separated by spaces (e.g., 'R U R\' U\'')
    Returns: number of repetitions needed to solve
    """
    cube = Cube()
    n = 0

    while True:
        for m in seq.split():
            cube.turn(m)
        n += 1
        if cube.solved():
            return n


def launch_graphics():
    import tkinter as tk
    from tkinter import messagebox

    cube = Cube()
    history = []
    colors = {
        "U": "#f5f4e9",
        "D": "#ffd447",
        "L": "#ff8a3d",
        "R": "#e74c4c",
        "F": "#25b978",
        "B": "#4387e8",
    }

    root = tk.Tk()
    root.title("Rubik Cube")
    root.geometry("900x700")
    root.minsize(700, 600)
    root.configure(bg="#171b20")

    header = tk.Frame(root, bg="#171b20", padx=24, pady=16)
    header.pack(fill="x")
    tk.Label(
        header,
        text="RUBIK CUBE  /  3x3",
        font=("Segoe UI", 18, "bold"),
        fg="#f4f1e8",
        bg="#171b20",
    ).pack(side="left")
    status = tk.Label(
        header,
        text="SOLVED",
        font=("Segoe UI", 10, "bold"),
        fg="#25b978",
        bg="#171b20",
    )
    status.pack(side="right")

    canvas = tk.Canvas(root, bg="#20262d", highlightthickness=0)
    canvas.pack(fill="both", expand=True, padx=24)

    def project(point, center_x, center_y, scale):
        x, y, z = point
        return (
            center_x + scale * 0.866 * (x - z),
            center_y + scale * (0.5 * (x + z) - y),
        )

    def draw_cube(_event=None):
        canvas.delete("all")
        width = max(canvas.winfo_width(), 1)
        height = max(canvas.winfo_height(), 1)
        scale = min(width * 0.22, height * 0.30, 105)
        center_x = width / 2
        center_y = height / 2 + scale * 0.12

        for visible_face in ("U", "R", "F"):
            for (position, normal), sticker in cube.state.items():
                if normal != Cube._NORMALS[visible_face]:
                    continue

                tangent_axes = [index for index, value in enumerate(normal) if value == 0]
                corners = []
                for first, second in ((-0.48, -0.48), (-0.48, 0.48), (0.48, 0.48), (0.48, -0.48)):
                    point = list(position)
                    point[tangent_axes[0]] += first
                    point[tangent_axes[1]] += second
                    corners.extend(project(point, center_x, center_y, scale))

                canvas.create_polygon(
                    corners,
                    fill=colors[sticker],
                    outline="#11161a",
                    width=3,
                    joinstyle="round",
                )

        status.configure(
            text="SOLVED" if cube.solved() else "MIXED",
            fg="#25b978" if cube.solved() else "#ffd447",
        )

    canvas.bind("<Configure>", draw_cube)

    def apply_moves(moves):
        trial = Cube()
        trial.state = cube.state.copy()
        try:
            for move in moves:
                trial.turn(move)
        except ValueError as error:
            messagebox.showerror("Invalid move", str(error), parent=root)
            return

        if moves:
            history.append(cube.state.copy())
            cube.state = trial.state
            draw_cube()

    controls = tk.Frame(root, bg="#171b20", padx=24, pady=16)
    controls.pack(fill="x")

    sequence_row = tk.Frame(controls, bg="#171b20")
    sequence_row.pack(fill="x", pady=(0, 12))
    tk.Label(
        sequence_row,
        text="MOVES",
        font=("Segoe UI", 9, "bold"),
        fg="#aab3ba",
        bg="#171b20",
    ).pack(side="left", padx=(0, 12))
    sequence_entry = tk.Entry(
        sequence_row,
        font=("Consolas", 12),
        bg="#2b333b",
        fg="#f4f1e8",
        insertbackground="#f4f1e8",
        relief="flat",
    )
    sequence_entry.pack(side="left", fill="x", expand=True, ipady=8)
    sequence_entry.insert(0, "R U R' U'")
    tk.Button(
        sequence_row,
        text="Apply",
        command=lambda: apply_moves(sequence_entry.get().split()),
        font=("Segoe UI", 10, "bold"),
        bg="#25b978",
        fg="#10251c",
        activebackground="#38d18d",
        relief="flat",
        padx=18,
        pady=7,
    ).pack(side="left", padx=(10, 0))
    sequence_entry.bind("<Return>", lambda _event: apply_moves(sequence_entry.get().split()))

    move_row = tk.Frame(controls, bg="#171b20")
    move_row.pack(fill="x")
    for index, move in enumerate(
        move for face in "UDLRFB" for move in (face, face + "'", face + "2")
    ):
        tk.Button(
            move_row,
            text=move,
            command=lambda selected=move: apply_moves([selected]),
            font=("Segoe UI", 10, "bold"),
            bg="#343d46",
            fg="#f4f1e8",
            activebackground="#4b5965",
            activeforeground="#ffffff",
            relief="flat",
            padx=10,
            pady=8,
        ).grid(row=index // 9, column=index % 9, padx=3, pady=3, sticky="ew")
    for column in range(9):
        move_row.grid_columnconfigure(column, weight=1)

    action_row = tk.Frame(controls, bg="#171b20")
    action_row.pack(fill="x", pady=(12, 0))

    def undo():
        if history:
            cube.state = history.pop()
            draw_cube()

    def reset():
        history.clear()
        cube.state = cube._solved.copy()
        draw_cube()

    tk.Button(
        action_row,
        text="Undo",
        command=undo,
        font=("Segoe UI", 10),
        bg="#343d46",
        fg="#f4f1e8",
        relief="flat",
        padx=14,
        pady=7,
    ).pack(side="left")
    tk.Button(
        action_row,
        text="Reset cube",
        command=reset,
        font=("Segoe UI", 10),
        bg="#343d46",
        fg="#f4f1e8",
        relief="flat",
        padx=14,
        pady=7,
    ).pack(side="left", padx=8)

    draw_cube()
    root.mainloop()


# Example usage:
if __name__ == "__main__":
    launch_graphics()

