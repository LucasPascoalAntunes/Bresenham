import tkinter as tk
from tkinter import ttk, messagebox

CELL_SIZE = 22
BASE_UNITS_X = 16
BASE_UNITS_Y = 10
MAX_UNITS_X = 30
MAX_UNITS_Y = 20
MAX_CANVAS_WIDTH = 600
MAX_CANVAS_HEIGHT = 400

UNITS_X = BASE_UNITS_X
UNITS_Y = BASE_UNITS_Y

CANVAS_WIDTH = CELL_SIZE * UNITS_X
CANVAS_HEIGHT = CELL_SIZE * UNITS_Y

WORLD_X_MIN = -UNITS_X // 2
WORLD_Y_MIN = -UNITS_Y // 2
WORLD_X_MAX_EDGE = WORLD_X_MIN + UNITS_X
WORLD_Y_MAX_EDGE = WORLD_Y_MIN + UNITS_Y

BG_COLOR = "#F8F9FA"
INPUT_FRAME_BG_COLOR = "#FFFFFF"
CANVAS_OUTER_FRAME_BG_COLOR = "#E9ECEF"
INPUT_BG_COLOR = "#FFFFFF"
BUTTON_FG_COLOR = "#FFFFFF"
BUTTON_BG_COLOR = "#007BFF"
BUTTON_ACTIVE_BG_COLOR = "#0056B3"
TEXT_COLOR_PRIMARY = "#212529"
TEXT_COLOR_SECONDARY = "#6C757D"
GRID_COLOR = "#DEE2E6"
AXIS_COLOR = "#495057"
PIXEL_COLOR_DDA = "#007BFF"
IDEAL_LINE_COLOR = "#DC3545"
CANVAS_BG_COLOR = "#FFFFFF"
CELL_NUMBER_COLOR = "#ADB5BD"
CELL_NUMBER_AXIS_COLOR = "#495057"

FONT_FAMILY_PRIMARY = "Segoe UI"
FONT_FAMILY_FALLBACK = "Calibri"
FONT_SIZE_NORMAL = 9
FONT_SIZE_LABEL_FRAME = 10
FONT_SIZE_GRID_LABEL = 7
FONT_SIZE_CELL_NUMBER = 5


class DDAGraphicalTest:
    def __init__(self, master):
        self.master = master
        self.current_units_x = BASE_UNITS_X
        self.current_units_y = BASE_UNITS_Y
        self.scroll_x = None
        self.scroll_y = None
        self._update_grid_dimensions()
        self._initialize_application()

    def _initialize_application(self):
        self._setup_window()
        self._setup_styles()
        self._create_interface()
        self._draw_initial_grid()

    def _setup_window(self):
        self.master.title("🎯 Visualizador Bresenham - Interface Aprimorada")
        self.master.configure(bg=BG_COLOR)
        self.master.resizable(False, False)

    def _setup_styles(self):
        self.style = ttk.Style()
        try:
            self.style.theme_use('clam')
        except tk.TclError:
            self.style.theme_use('default')

        self._setup_fonts()
        self._configure_styles()

    def _setup_fonts(self):
        try:
            self.primary_font = (FONT_FAMILY_PRIMARY, FONT_SIZE_NORMAL)
            self.labelframe_font = (FONT_FAMILY_PRIMARY, FONT_SIZE_LABEL_FRAME, "bold")
            self.grid_label_font = (FONT_FAMILY_PRIMARY, FONT_SIZE_GRID_LABEL)
            self.cell_number_font = (FONT_FAMILY_PRIMARY, FONT_SIZE_CELL_NUMBER)
            self.button_font = (FONT_FAMILY_PRIMARY, FONT_SIZE_NORMAL, "bold")
        except tk.TclError:
            self.primary_font = (FONT_FAMILY_FALLBACK, FONT_SIZE_NORMAL)
            self.labelframe_font = (FONT_FAMILY_FALLBACK, FONT_SIZE_LABEL_FRAME, "bold")
            self.grid_label_font = (FONT_FAMILY_FALLBACK, FONT_SIZE_GRID_LABEL)
            self.cell_number_font = (FONT_FAMILY_FALLBACK, FONT_SIZE_CELL_NUMBER)
            self.button_font = (FONT_FAMILY_FALLBACK, FONT_SIZE_NORMAL, "bold")

    def _configure_styles(self):
        self.style.configure('.', font=self.primary_font, background=BG_COLOR, foreground=TEXT_COLOR_PRIMARY)
        
        self.style.configure('Input.TLabel', foreground=TEXT_COLOR_PRIMARY, background=INPUT_FRAME_BG_COLOR)
        self.style.configure('Outer.TLabel', foreground=TEXT_COLOR_SECONDARY, background=BG_COLOR)
        
        self.style.configure('TButton', font=self.button_font, foreground=BUTTON_FG_COLOR,
                             background=BUTTON_BG_COLOR, padding=(15, 10))
        self.style.map('TButton', background=[('active', BUTTON_ACTIVE_BG_COLOR), ('pressed', BUTTON_ACTIVE_BG_COLOR)])
        
        self.style.configure('TEntry', font=self.primary_font, fieldbackground=INPUT_BG_COLOR,
                             foreground=TEXT_COLOR_PRIMARY, padding=(8,8))
        
        self.style.configure('TLabelframe', labelmargins=(15, 5), background=INPUT_FRAME_BG_COLOR,
                             borderwidth=2, relief="solid")
        self.style.configure('TLabelframe.Label', font=self.labelframe_font, foreground=TEXT_COLOR_PRIMARY,
                             background=INPUT_FRAME_BG_COLOR)
        
        self.style.configure('CanvasOuter.TFrame', background=CANVAS_OUTER_FRAME_BG_COLOR)

    def _create_interface(self):
        self._create_header()
        self._create_input_section()
        self._create_action_button()
        self._create_visualization_area()
        self._create_information_footer()

    def _create_header(self):
        header_frame = ttk.Frame(self.master, style='TFrame')
        header_frame.pack(pady=(10, 3), padx=15, fill="x")
        
        title_label = ttk.Label(header_frame, text="Algoritmo Bresenham - Rasterização de Linha",
                               style='Outer.TLabel', font=(FONT_FAMILY_PRIMARY, 12, "bold"))
        title_label.pack()

    def _create_input_section(self):
        input_labelframe = ttk.LabelFrame(self.master, text="🎯 Coordenadas da Linha", 
                                         padding=(15, 10), style='TLabelframe')
        input_labelframe.pack(pady=8, padx=15, fill="x")

        self._setup_grid_weights(input_labelframe)
        self._create_coordinate_inputs(input_labelframe)

    def _setup_grid_weights(self, parent):
        for i in range(4):
            parent.grid_columnconfigure(i, weight=1 if i % 2 == 1 else 0)

    def _create_coordinate_inputs(self, parent):
        coordinates = [
            ("Ponto Inicial X:", "x0_entry", "-3", 0, 0),
            ("Ponto Inicial Y:", "y0_entry", "-2", 0, 2),
            ("Ponto Final X:", "x1_entry", "3", 1, 0),
            ("Ponto Final Y:", "y1_entry", "2", 1, 2)
        ]

        for label_text, attr_name, default_value, row, col in coordinates:
            ttk.Label(parent, text=label_text, style='Input.TLabel').grid(
                row=row, column=col, padx=(12 if col==2 else 0, 5), pady=6, sticky="w")
            
            entry = ttk.Entry(parent, width=6)
            entry.grid(row=row, column=col+1, pady=6, sticky="ew")
            entry.insert(0, default_value)
            setattr(self, attr_name, entry)

    def _create_action_button(self):
        button_frame = ttk.Frame(self.master, style='TFrame')
        button_frame.pack(pady=6, padx=15, fill="x")
        
        self.draw_button = ttk.Button(button_frame, text="🎨 Executar Algoritmo Bresenham", 
                                     command=self._execute_bresenham_algorithm)
        self.draw_button.pack(fill="x")

    def _create_visualization_area(self):
        viz_frame = ttk.Frame(self.master, style='TFrame')
        viz_frame.pack(pady=(6, 3), padx=15, fill="both", expand=True)
        
        viz_label = ttk.Label(viz_frame, text="📊 Visualização da Grade", 
                             style='Outer.TLabel', font=self.labelframe_font)
        viz_label.pack(pady=(0, 6))

        self.canvas_outer_frame = ttk.Frame(viz_frame, style='CanvasOuter.TFrame', padding=8)
        self.canvas_outer_frame.pack(fill="both", expand=True)

        self._create_canvas_widget()

    def _create_canvas_widget(self):
        canvas_frame = ttk.Frame(self.canvas_outer_frame)
        canvas_frame.pack(fill="both", expand=True)
        
        actual_width = min(CANVAS_WIDTH, MAX_CANVAS_WIDTH)
        actual_height = min(CANVAS_HEIGHT, MAX_CANVAS_HEIGHT)
        
        self.canvas = tk.Canvas(canvas_frame, width=actual_width, height=actual_height,
                               bg=CANVAS_BG_COLOR, highlightthickness=2, 
                               highlightbackground=AXIS_COLOR, relief="solid",
                               scrollregion=(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT))
        
        if CANVAS_WIDTH > MAX_CANVAS_WIDTH:
            self.scroll_x = ttk.Scrollbar(canvas_frame, orient="horizontal", command=self.canvas.xview)
            self.canvas.configure(xscrollcommand=self.scroll_x.set)
            self.scroll_x.pack(side="bottom", fill="x")
        
        if CANVAS_HEIGHT > MAX_CANVAS_HEIGHT:
            self.scroll_y = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
            self.canvas.configure(yscrollcommand=self.scroll_y.set)
            self.scroll_y.pack(side="right", fill="y")
        
        self.canvas.pack(side="left", fill="both", expand=True)

    def _update_canvas_size(self):
        actual_width = min(CANVAS_WIDTH, MAX_CANVAS_WIDTH)
        actual_height = min(CANVAS_HEIGHT, MAX_CANVAS_HEIGHT)
        
        self.canvas.configure(width=actual_width, height=actual_height,
                             scrollregion=(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT))
        
        if hasattr(self, 'scroll_x') and self.scroll_x:
            self.scroll_x.destroy()
            self.scroll_x = None
        if hasattr(self, 'scroll_y') and self.scroll_y:
            self.scroll_y.destroy()
            self.scroll_y = None
        
        canvas_frame = self.canvas.master
        
        if CANVAS_WIDTH > MAX_CANVAS_WIDTH:
            self.scroll_x = ttk.Scrollbar(canvas_frame, orient="horizontal", command=self.canvas.xview)
            self.canvas.configure(xscrollcommand=self.scroll_x.set)
            self.scroll_x.pack(side="bottom", fill="x")
        
        if CANVAS_HEIGHT > MAX_CANVAS_HEIGHT:
            self.scroll_y = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
            self.canvas.configure(yscrollcommand=self.scroll_y.set)
            self.scroll_y.pack(side="right", fill="y")

    def _create_information_footer(self):
        info_text = (f"💡 Grade: [{WORLD_X_MIN},{WORLD_X_MAX_EDGE-1}] × [{WORLD_Y_MIN},{WORLD_Y_MAX_EDGE-1}] "
                    f"| 🔵 Pixels Bresenham | 🔴 Linha Ideal")
        
        self.info_label = ttk.Label(self.master, style='Outer.TLabel', text=info_text,
                                   font=(self.primary_font[0], FONT_SIZE_NORMAL-2),
                                   justify="center")
        self.info_label.pack(pady=(3, 10), padx=15)

    def _update_info_footer(self):
        info_text = (f"💡 Grade: [{WORLD_X_MIN},{WORLD_X_MAX_EDGE-1}] × [{WORLD_Y_MIN},{WORLD_Y_MAX_EDGE-1}] "
                    f"| 🔵 Pixels Bresenham | 🔴 Linha Ideal")
        self.info_label.configure(text=info_text)

    def _world_to_canvas_cell_coords(self, wx, wy):
        cx0 = (wx - WORLD_X_MIN) * CELL_SIZE
        cy0 = CANVAS_HEIGHT - ((wy + 1) - WORLD_Y_MIN) * CELL_SIZE
        cx1 = ((wx + 1) - WORLD_X_MIN) * CELL_SIZE
        cy1 = CANVAS_HEIGHT - (wy - WORLD_Y_MIN) * CELL_SIZE
        return cx0, cy0, cx1, cy1

    def _world_to_canvas_line_endpoint_coords(self, wx, wy):
        cx = (wx + 0.5 - WORLD_X_MIN) * CELL_SIZE
        cy = CANVAS_HEIGHT - (wy + 0.5 - WORLD_Y_MIN) * CELL_SIZE
        return cx, cy

    def _draw_initial_grid(self):
        self._clear_canvas()
        self._draw_grid_structure()
        self._draw_coordinates()
        self._draw_axis_markings()

    def _clear_canvas(self):
        self.canvas.delete("all")

    def _draw_grid_structure(self):
        self._draw_vertical_grid_lines()
        self._draw_horizontal_grid_lines()

    def _draw_vertical_grid_lines(self):
        for i in range(UNITS_X + 1):
            x_pos = i * CELL_SIZE
            world_x = WORLD_X_MIN + i
            is_main_axis = (world_x == 0)
            
            line_color = AXIS_COLOR if is_main_axis else GRID_COLOR
            line_width = 2 if is_main_axis else 1
            
            self.canvas.create_line(x_pos, 0, x_pos, CANVAS_HEIGHT, 
                                   fill=line_color, width=line_width, tags="grid_structure")

    def _draw_horizontal_grid_lines(self):
        for i in range(UNITS_Y + 1):
            y_pos = i * CELL_SIZE
            world_y = WORLD_Y_MIN + (UNITS_Y - i)
            is_main_axis = (world_y == 0)
            
            line_color = AXIS_COLOR if is_main_axis else GRID_COLOR
            line_width = 2 if is_main_axis else 1
            
            self.canvas.create_line(0, y_pos, CANVAS_WIDTH, y_pos,
                                   fill=line_color, width=line_width, tags="grid_structure")

    def _draw_coordinates(self):
        for world_x in range(WORLD_X_MIN, WORLD_X_MAX_EDGE):
            for world_y in range(WORLD_Y_MIN, WORLD_Y_MAX_EDGE):
                self._draw_cell_coordinate(world_x, world_y)

    def _draw_cell_coordinate(self, wx, wy):
        cx0, cy0, cx1, cy1 = self._world_to_canvas_cell_coords(wx, wy)
        center_x, center_y = (cx0 + cx1) / 2, (cy0 + cy1) / 2
        
        is_axis_cell = (wx == 0 or wy == 0)
        text_color = CELL_NUMBER_AXIS_COLOR if is_axis_cell else CELL_NUMBER_COLOR
        
        self.canvas.create_text(center_x, center_y, text=f"({wx},{wy})",
                               fill=text_color, font=self.cell_number_font,
                               tags="coordinates")

    def _draw_axis_markings(self):
        self._draw_x_axis_labels()
        self._draw_y_axis_labels()

    def _draw_x_axis_labels(self):
        for i in range(UNITS_X + 1):
            x_pos = i * CELL_SIZE
            world_x = WORLD_X_MIN + i
            
            if self._should_show_axis_label(world_x):
                self.canvas.create_text(x_pos, CANVAS_HEIGHT + 8, text=str(world_x),
                                       anchor="n", fill=TEXT_COLOR_PRIMARY, 
                                       font=self.grid_label_font, tags="axis_labels")

    def _draw_y_axis_labels(self):
        for i in range(UNITS_Y + 1):
            y_pos = i * CELL_SIZE
            world_y = WORLD_Y_MIN + (UNITS_Y - i)
            
            if self._should_show_axis_label(world_y):
                self.canvas.create_text(-8, y_pos, text=str(world_y),
                                       anchor="e", fill=TEXT_COLOR_PRIMARY,
                                       font=self.grid_label_font, tags="axis_labels")

    def _should_show_axis_label(self, value):
        return value % 2 == 0 or value == 0

    def bresenham_algorithm(self, x0, y0, x1, y1):
        pixels = []
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        
        x_step = 1 if x0 < x1 else -1
        y_step = 1 if y0 < y1 else -1
        
        x, y = x0, y0
        
        if dx > dy:
            error = dx / 2
            while True:
                pixels.append((x, y))
                if x == x1:
                    break
                error -= dy
                if error < 0:
                    y += y_step
                    error += dx
                x += x_step
        else:
            error = dy / 2
            while True:
                pixels.append((x, y))
                if y == y1:
                    break
                error -= dx
                if error < 0:
                    x += x_step
                    error += dy
                y += y_step
        
        return pixels

    def _calculate_required_grid_size(self, x0, y0, x1, y1):
        coords = [x0, y0, x1, y1]
        max_coord = max(abs(coord) for coord in coords)
        
        padding = 3
        required_size = (max_coord + padding) * 2
        
        min_size_x = max(BASE_UNITS_X, required_size)
        min_size_y = max(BASE_UNITS_Y, required_size)
        
        self.current_units_x = min(MAX_UNITS_X, min_size_x if min_size_x % 2 == 0 else min_size_x + 1)
        self.current_units_y = min(MAX_UNITS_Y, min_size_y if min_size_y % 2 == 0 else min_size_y + 1)

    def _execute_bresenham_algorithm(self):
        coordinates = self._get_input_coordinates()
        if coordinates is None:
            return

        x0, y0, x1, y1 = coordinates
        
        max_coord = max(abs(coord) for coord in coordinates)
        if max_coord > 15:
            response = messagebox.askyesno("Grade Grande", 
                                         f"As coordenadas são grandes (máximo: {max_coord}). "
                                         f"Isso criará uma grade maior com barras de rolagem. Continuar?", 
                                         parent=self.master)
            if not response:
                return
        
        old_units_x, old_units_y = self.current_units_x, self.current_units_y
        self._calculate_required_grid_size(x0, y0, x1, y1)
        
        if (self.current_units_x != old_units_x or self.current_units_y != old_units_y):
            self._update_grid_dimensions()
            self._update_canvas_size()
            self._update_info_footer()
            self._draw_initial_grid()
        
        self._clear_previous_results()
        bresenham_pixels = self.bresenham_algorithm(x0, y0, x1, y1)
        self._visualize_results(bresenham_pixels, x0, y0, x1, y1)

    def _get_input_coordinates(self):
        try:
            return [int(entry.get()) for entry in [self.x0_entry, self.y0_entry, 
                                                  self.x1_entry, self.y1_entry]]
        except ValueError:
            messagebox.showerror("❌ Entrada Inválida", 
                               "Insira apenas números inteiros válidos.", 
                               parent=self.master)
            return None

    def _update_grid_dimensions(self):
        global UNITS_X, UNITS_Y, CANVAS_WIDTH, CANVAS_HEIGHT
        global WORLD_X_MIN, WORLD_Y_MIN, WORLD_X_MAX_EDGE, WORLD_Y_MAX_EDGE
        
        UNITS_X = self.current_units_x
        UNITS_Y = self.current_units_y
        CANVAS_WIDTH = CELL_SIZE * UNITS_X
        CANVAS_HEIGHT = CELL_SIZE * UNITS_Y
        WORLD_X_MIN = -UNITS_X // 2
        WORLD_Y_MIN = -UNITS_Y // 2
        WORLD_X_MAX_EDGE = WORLD_X_MIN + UNITS_X
        WORLD_Y_MAX_EDGE = WORLD_Y_MIN + UNITS_Y

    def _clear_previous_results(self):
        self.canvas.delete("bresenham_results", "ideal_line")

    def _visualize_results(self, pixels, x0, y0, x1, y1):
        self._highlight_bresenham_pixels(pixels)
        self._draw_ideal_reference_line(x0, y0, x1, y1)

    def _highlight_bresenham_pixels(self, pixels):
        for wx, wy in pixels:
            if self._is_within_bounds(wx, wy):
                self._draw_highlighted_pixel(wx, wy)

    def _is_within_bounds(self, wx, wy):
        return (WORLD_X_MIN <= wx < WORLD_X_MAX_EDGE and 
                WORLD_Y_MIN <= wy < WORLD_Y_MAX_EDGE)

    def _draw_highlighted_pixel(self, wx, wy):
        cx0, cy0, cx1, cy1 = self._world_to_canvas_cell_coords(wx, wy)
        
        self.canvas.create_rectangle(cx0+2, cy0+2, cx1-2, cy1-2, 
                                   fill=PIXEL_COLOR_DDA, outline=PIXEL_COLOR_DDA,
                                   tags="bresenham_results")
        
        center_x, center_y = (cx0 + cx1) / 2, (cy0 + cy1) / 2
        self.canvas.create_text(center_x, center_y, text=f"({wx},{wy})",
                               fill="white", font=(self.cell_number_font[0], 
                               self.cell_number_font[1], "bold"),
                               tags="bresenham_results")

    def _draw_ideal_reference_line(self, x0, y0, x1, y1):
        start_x, start_y = self._world_to_canvas_line_endpoint_coords(x0, y0)
        end_x, end_y = self._world_to_canvas_line_endpoint_coords(x1, y1)
        
        self.canvas.create_line(start_x, start_y, end_x, end_y,
                               fill=IDEAL_LINE_COLOR, width=3, dash=(10, 5), 
                               tags="ideal_line")


if __name__ == '__main__':
    root = tk.Tk()
    app = DDAGraphicalTest(root)
    root.mainloop()
