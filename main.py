import tkinter as tk
from tkinter import ttk, messagebox
import itertools

class LogicGate:
    """Класс для представления логического вентиля"""
    def __init__(self, gate_type, name, position=(0, 0)):
        self.gate_type = gate_type  # 'AND', 'OR', 'NOT', 'NAND', 'NOR', 'XOR'
        self.name = name
        self.position = position
        self.inputs = []  # Имена входных вентилей
        self.output = None
        self.input_values = {}  # Текущие значения входов
        
    def compute(self):
        """Вычисление выхода вентиля на основе входов"""
        if not self.inputs:
            return None
            
        if self.gate_type == 'AND':
            result = all(self.input_values.values())
        elif self.gate_type == 'OR':
            result = any(self.input_values.values())
        elif self.gate_type == 'NOT':
            # Для NOT берем первый вход
            if self.inputs:
                result = not self.input_values.get(self.inputs[0], False)
            else:
                result = None
        elif self.gate_type == 'NAND':
            result = not all(self.input_values.values())
        elif self.gate_type == 'NOR':
            result = not any(self.input_values.values())
        elif self.gate_type == 'XOR':
            values = list(self.input_values.values())
            result = values[0] != values[1] if len(values) == 2 else False
        else:
            result = None
            
        self.output = result
        return result

class CircuitSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Симулятор логических элементов")
        self.root.geometry("1200x700")
        
        # Серо-белая цветовая палитра
        self.colors = {
            'bg_main': '#FFFFFF',
            'bg_sidebar': '#F5F5F5',
            'bg_header': '#2C3E50',
            'btn_normal': '#E0E0E0',
            'btn_hover': '#BDBDBD',
            'btn_active': '#9E9E9E',
            'btn_text': '#212121',
            'btn_special': '#607D8B',
            'btn_special_hover': '#455A64',
            'btn_special_text': '#FFFFFF',
            'canvas_bg': '#FFFFFF',
            'gate_and': '#E8EAF6',
            'gate_or': '#E3F2FD',
            'gate_not': '#F3E5F5',
            'gate_nand': '#E8F5E8',
            'gate_nor': '#FFF3E0',
            'gate_xor': '#FCE4EC',
            'gate_input': '#F5F5F5',
            'gate_output': '#EEEEEE',
            'text': '#37474F',
            'text_light': '#78909C',
            'text_dark': '#263238',
            'connection': '#546E7A',
            'selected': '#2196F3',
            'input_dot': '#757575',
            'output_dot': '#424242',
            'border': '#CFD8DC',
            'highlight': '#ECEFF1',
        }
        
        # Настройка стилей
        self.setup_styles()
        
        # Хранение компонентов схемы
        self.gates = {}
        self.connections = []
        self.input_gates = {}
        self.output_gates = {}
        
        # Создание интерфейса
        self.create_widgets()
        
    def setup_styles(self):
        """Настройка стилей для кнопок и виджетов"""
        self.root.configure(bg=self.colors['bg_main'])
        
        # Стиль для кнопок
        style = ttk.Style()
        style.theme_use('clam')
        
        # Обычные кнопки
        style.configure('Gray.TButton',
                       background=self.colors['btn_normal'],
                       foreground=self.colors['btn_text'],
                       font=('Segoe UI', 10),
                       borderwidth=1,
                       relief='flat',
                       padding=10)
        
        style.map('Gray.TButton',
                 background=[('active', self.colors['btn_hover']),
                            ('pressed', self.colors['btn_active'])],
                 relief=[('pressed', 'sunken')])
        
        # Специальные кнопки
        style.configure('Special.TButton',
                       background=self.colors['btn_special'],
                       foreground=self.colors['btn_special_text'],
                       font=('Segoe UI', 10, 'bold'),
                       borderwidth=1,
                       relief='flat',
                       padding=10)
        
        style.map('Special.TButton',
                 background=[('active', self.colors['btn_special_hover']),
                            ('pressed', self.colors['btn_active'])])
        
    def create_widgets(self):
        # Верхняя панель с названием
        header_frame = tk.Frame(self.root, height=80, bg=self.colors['bg_header'])
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Название по центру
        title_label = tk.Label(header_frame, 
                              text="СИМУЛЯТОР ЛОГИЧЕСКИХ ЭЛЕМЕНТОВ",
                              font=('Segoe UI', 24, 'bold'),
                              bg=self.colors['bg_header'],
                              fg='white')
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(header_frame,
                                 text="Конструктор цифровых схем с таблицей истинности",
                                 font=('Segoe UI', 11),
                                 bg=self.colors['bg_header'],
                                 fg='#B0BEC5')
        subtitle_label.pack(pady=(0, 10))
        
        # Основной контейнер
        main_container = tk.Frame(self.root, bg=self.colors['bg_main'])
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Панель инструментов слева
        left_frame = tk.Frame(main_container, width=250, bg=self.colors['bg_sidebar'])
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        left_frame.pack_propagate(False)
        
        # Разделы панели инструментов
        sections = [
            ("ЛОГИЧЕСКИЕ ЭЛЕМЕНТЫ", ['AND', 'OR', 'NOT', 'NAND', 'NOR', 'XOR']),
            ("ИНТЕРФЕЙСНЫЕ ЭЛЕМЕНТЫ", ['INPUT', 'OUTPUT']),
            ("УПРАВЛЕНИЕ", ['Соединить', 'Удалить', 'Проверить схему', 'Таблица истинности', 'Очистить схему'])
        ]
        
        for section_title, items in sections:
            # Заголовок раздела
            section_frame = tk.Frame(left_frame, bg=self.colors['bg_sidebar'])
            section_frame.pack(fill=tk.X, padx=15, pady=(15, 5))
            
            tk.Label(section_frame, text=section_title,
                    font=('Segoe UI', 9, 'bold'),
                    bg=self.colors['bg_sidebar'],
                    fg=self.colors['text_dark'],
                    anchor='w').pack(fill=tk.X)
            
            # Разделитель
            ttk.Separator(section_frame, orient='horizontal').pack(fill=tk.X, pady=3)
            
            # Кнопки раздела
            for item in items:
                if item in ['INPUT', 'OUTPUT', 'AND', 'OR', 'NOT', 'NAND', 'NOR', 'XOR']:
                    # Кнопки элементов
                    btn = tk.Button(section_frame, text=item,
                                  font=('Segoe UI', 10),
                                  bg=self.colors['btn_normal'],
                                  fg=self.colors['btn_text'],
                                  activebackground=self.colors['btn_hover'],
                                  activeforeground=self.colors['btn_text'],
                                  relief='flat',
                                  borderwidth=1,
                                  height=1,
                                  cursor='hand2',
                                  command=lambda i=item: self.add_gate(i))
                    btn.pack(fill=tk.X, pady=2, padx=5)
                    
                    # Эффект при наведении
                    btn.bind('<Enter>', lambda e, b=btn: b.configure(
                        bg=self.colors['btn_hover']))
                    btn.bind('<Leave>', lambda e, b=btn: b.configure(
                        bg=self.colors['btn_normal']))
                else:
                    # Кнопки управления
                    special_commands = {
                        'Соединить': self.start_connection,
                        'Удалить': self.delete_selected,
                        'Проверить схему': self.check_circuit,
                        'Таблица истинности': self.show_truth_table,
                        'Очистить схему': self.clear_circuit
                    }
                    
                    btn = tk.Button(section_frame, text=item,
                                  font=('Segoe UI', 10, 'bold'),
                                  bg=self.colors['btn_special'],
                                  fg=self.colors['btn_special_text'],
                                  activebackground=self.colors['btn_special_hover'],
                                  activeforeground='white',
                                  relief='flat',
                                  borderwidth=0,
                                  height=1,
                                  cursor='hand2',
                                  command=special_commands[item])
                    btn.pack(fill=tk.X, pady=3, padx=5)
                    
                    # Эффект при наведении
                    btn.bind('<Enter>', lambda e, b=btn: b.configure(
                        bg=self.colors['btn_special_hover']))
                    btn.bind('<Leave>', lambda e, b=btn: b.configure(
                        bg=self.colors['btn_special']))
        
        # Статусная панель внизу
        status_frame = tk.Frame(left_frame, bg=self.colors['bg_sidebar'], height=120)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=15)
        status_frame.pack_propagate(False)
        
        tk.Label(status_frame, text="Статус схемы:",
                font=('Segoe UI', 9, 'bold'),
                bg=self.colors['bg_sidebar'],
                fg=self.colors['text_dark'],
                anchor='w').pack(fill=tk.X, pady=(0, 5))
        
        self.status_label = tk.Label(status_frame, text="Готов к работе",
                                    font=('Segoe UI', 9),
                                    bg=self.colors['bg_sidebar'],
                                    fg=self.colors['text_light'],
                                    anchor='w',
                                    justify=tk.LEFT,
                                    wraplength=220)
        self.status_label.pack(fill=tk.X)
        
        # Информация о схеме
        info_frame = tk.Frame(status_frame, bg=self.colors['bg_sidebar'])
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.info_label = tk.Label(info_frame, text="Элементов: 0\nСоединений: 0",
                                  font=('Segoe UI', 8),
                                  bg=self.colors['bg_sidebar'],
                                  fg=self.colors['text_light'],
                                  anchor='w',
                                  justify=tk.LEFT)
        self.info_label.pack(fill=tk.X)
        
        # Область рисования схемы
        self.canvas = tk.Canvas(main_container, bg=self.colors['canvas_bg'], 
                               highlightthickness=1,
                               highlightbackground=self.colors['border'])
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Сетка на холсте
        self.draw_grid()
        
        # Привязка событий мыши
        self.canvas.bind("<Button-1>", self.canvas_click)
        self.canvas.bind("<B1-Motion>", self.drag_gate)
        self.canvas.bind("<ButtonRelease-1>", self.canvas_release)
        
        # Выделенный элемент
        self.selected_gate = None
        self.connecting = False
        self.connection_start = None
        
        # Счетчик для имен
        self.gate_counter = {'AND': 1, 'OR': 1, 'NOT': 1, 'NAND': 1,
                            'NOR': 1, 'XOR': 1, 'INPUT': 1, 'OUTPUT': 1}
    
    def draw_grid(self):
        """Отрисовка сетки на холсте"""
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width > 1 and height > 1:
            self.canvas.delete('grid')
            
            # Рисуем вертикальные линии
            for x in range(0, width, 20):
                self.canvas.create_line(x, 0, x, height, 
                                       fill=self.colors['highlight'], 
                                       tags='grid', width=0.5)
            
            # Рисуем горизонтальные линии
            for y in range(0, height, 20):
                self.canvas.create_line(0, y, width, y, 
                                       fill=self.colors['highlight'], 
                                       tags='grid', width=0.5)
    
    def add_gate(self, gate_type):
        """Добавление нового вентиля на схему"""
        name = f"{gate_type}{self.gate_counter[gate_type]}"
        self.gate_counter[gate_type] += 1
        
        gate = LogicGate(gate_type, name, (200, 200))
        self.gates[name] = gate
        
        if gate_type == 'INPUT':
            self.input_gates[name] = gate
            gate.input_values = {'input': False}
        elif gate_type == 'OUTPUT':
            self.output_gates[name] = gate
        
        self.draw_gate(gate)
        self.update_status(f"Добавлен элемент: {name}")
        self.update_info()
    
    def draw_gate(self, gate):
        """Отрисовка вентиля на холсте"""
        x, y = gate.position
        
        # Цвета для разных вентилей
        gate_colors = {
            'AND': self.colors['gate_and'],
            'OR': self.colors['gate_or'],
            'NOT': self.colors['gate_not'],
            'NAND': self.colors['gate_nand'],
            'NOR': self.colors['gate_nor'],
            'XOR': self.colors['gate_xor'],
            'INPUT': self.colors['gate_input'],
            'OUTPUT': self.colors['gate_output']
        }
        
        color = gate_colors.get(gate.gate_type, self.colors['btn_normal'])
        
        # Рисуем прямоугольник для вентиля с тенью
        gate.rect = self.canvas.create_rectangle(x-45, y-25, x+45, y+25,
                                                fill=color, 
                                                outline=self.colors['border'],
                                                width=1, 
                                                tags=('gate', gate.name))
        
        # Подписываем вентиль
        self.canvas.create_text(x, y, text=gate.name, 
                               font=('Segoe UI', 9, 'bold'),
                               fill=self.colors['text_dark'],
                               tags=('gate', gate.name))
        
        # Рисуем входы и выходы только для INPUT и OUTPUT
        if gate.gate_type == 'INPUT':
            # Только выход для входного вентиля (справа)
            gate.output_point = self.canvas.create_oval(x+35, y-5, x+45, y+5,
                                                       fill=self.colors['output_dot'], 
                                                       outline=self.colors['border'],
                                                       width=1,
                                                       tags=('gate', gate.name, 'output_point'))
        elif gate.gate_type == 'OUTPUT':
            # Только вход для выходного вентиля (слева)
            gate.input_point = self.canvas.create_oval(x-45, y-5, x-35, y+5,
                                                      fill=self.colors['input_dot'], 
                                                      outline=self.colors['border'],
                                                      width=1,
                                                      tags=('gate', gate.name, 'input_point'))
    
    def get_connection_point(self, gate, is_output=False):
        """Получение точки соединения для вентиля"""
        x, y = gate.position
        if is_output:
            # Точка выхода - правая сторона
            return (x + 45, y)
        else:
            # Точка входа - левая сторона
            return (x - 45, y)
    
    def canvas_click(self, event):
        """Обработка клика на холсте"""
        items = self.canvas.find_withtag('current')
        
        if items:
            tags = self.canvas.gettags(items[0])
            
            # Игнорируем клик по сетке
            if 'grid' in tags:
                return
            
            # Находим вентиль по тегу
            clicked_gate = None
            for tag in tags:
                if tag in self.gates:
                    clicked_gate = self.gates[tag]
                    break
            
            if clicked_gate:
                # Снимаем выделение с предыдущего
                if self.selected_gate and self.selected_gate != clicked_gate:
                    self.canvas.itemconfig(self.selected_gate.rect, 
                                         outline=self.colors['border'])
                
                self.selected_gate = clicked_gate
                
                # Выделяем новый
                self.canvas.itemconfig(self.selected_gate.rect, 
                                     outline=self.colors['selected'],
                                     width=2)
                
                if self.connecting:
                    if self.connection_start:
                        # Завершаем соединение
                        self.create_connection(self.connection_start, self.selected_gate)
                        self.connecting = False
                        self.connection_start = None
                        self.update_status("Готово")
                    else:
                        # Начинаем соединение
                        self.connection_start = self.selected_gate
                        self.update_status(f"Выберите второй элемент для соединения с {self.selected_gate.name}")
                else:
                    self.update_status(f"Выбран элемент: {self.selected_gate.name}")
    
    def create_connection(self, gate_from, gate_to):
        """Создание соединения между вентилями"""
        # Проверяем возможность соединения
        if gate_from == gate_to:
            messagebox.showerror("Ошибка", "Нельзя соединять элемент с самим собой!")
            return
        
        # Проверяем, не существует ли уже такое соединение
        for conn in self.connections:
            if conn['from'] == gate_from.name and conn['to'] == gate_to.name:
                messagebox.showwarning("Предупреждение", "Такое соединение уже существует!")
                return
        
        # Добавляем соединение
        connection = {
            'from': gate_from.name,
            'to': gate_to.name,
            'from_gate': gate_from.gate_type,
            'to_gate': gate_to.gate_type
        }
        
        self.connections.append(connection)
        gate_to.inputs.append(gate_from.name)
        
        # Получаем точки соединения
        from_point = self.get_connection_point(gate_from, is_output=True)
        to_point = self.get_connection_point(gate_to, is_output=False)
        
        # Рисуем соединение
        line = self.canvas.create_line(from_point[0], from_point[1],
                                     to_point[0], to_point[1],
                                     fill=self.colors['connection'], 
                                     width=2,
                                     arrow=tk.LAST,
                                     arrowshape=(8, 10, 3),
                                     tags=('connection',
                                           f"{gate_from.name}-{gate_to.name}"))
        connection['line_id'] = line
        
        self.update_status(f"Создано соединение: {gate_from.name} → {gate_to.name}")
        self.update_info()
    
    def start_connection(self):
        """Начало процесса соединения"""
        self.connecting = True
        self.update_status("Выберите первый элемент для соединения")
    
    def drag_gate(self, event):
        """Перетаскивание вентиля"""
        if self.selected_gate and not self.connecting:
            dx = event.x - self.selected_gate.position[0]
            dy = event.y - self.selected_gate.position[1]
            
            self.selected_gate.position = (event.x, event.y)
            self.canvas.move(self.selected_gate.name, dx, dy)
            
            # Обновляем соединения
            self.update_connections(self.selected_gate)
    
    def update_connections(self, gate):
        """Обновление позиций соединений при перемещении вентиля"""
        for conn in self.connections:
            if conn['from'] == gate.name or conn['to'] == gate.name:
                from_gate = self.gates[conn['from']]
                to_gate = self.gates[conn['to']]
                
                from_point = self.get_connection_point(from_gate, is_output=True)
                to_point = self.get_connection_point(to_gate, is_output=False)
                
                self.canvas.coords(conn['line_id'],
                                 from_point[0], from_point[1],
                                 to_point[0], to_point[1])
    
    def canvas_release(self, event):
        """Обработка отпускания кнопки мыши"""
        self.selected_gate = None
    
    def delete_selected(self):
        """Удаление выбранного элемента"""
        if self.selected_gate:
            # Удаляем все соединения с этим вентилем
            connections_to_remove = []
            for conn in self.connections:
                if conn['from'] == self.selected_gate.name or conn['to'] == self.selected_gate.name:
                    connections_to_remove.append(conn)
                    
            for conn in connections_to_remove:
                self.canvas.delete(conn['line_id'])
                self.connections.remove(conn)
                
                # Удаляем из списков входов
                for gate in self.gates.values():
                    if self.selected_gate.name in gate.inputs:
                        gate.inputs.remove(self.selected_gate.name)
            
            # Удаляем вентиль
            self.canvas.delete(self.selected_gate.name)
            
            # Удаляем из словарей
            if self.selected_gate.name in self.input_gates:
                del self.input_gates[self.selected_gate.name]
            if self.selected_gate.name in self.output_gates:
                del self.output_gates[self.selected_gate.name]
            
            del self.gates[self.selected_gate.name]
            self.selected_gate = None
            self.update_status("Элемент удален")
            self.update_info()
    
    def clear_circuit(self):
        """Очистка всей схемы"""
        if messagebox.askyesno("Очистка схемы", "Удалить всю схему?"):
            self.canvas.delete('all')
            self.draw_grid()  # Перерисовываем сетку
            self.gates.clear()
            self.connections.clear()
            self.input_gates.clear()
            self.output_gates.clear()
            self.selected_gate = None
            self.connecting = False
            self.connection_start = None
            self.gate_counter = {'AND': 1, 'OR': 1, 'NOT': 1, 'NAND': 1,
                               'NOR': 1, 'XOR': 1, 'INPUT': 1, 'OUTPUT': 1}
            self.update_status("Схема очищена")
            self.update_info()
    
    def check_circuit(self):
        """Проверка схемы на корректность"""
        info = []
        
        # Проверяем INPUT вентили
        if not self.input_gates:
            info.append("⚠️ Нет входных элементов (INPUT)")
        else:
            info.append(f"✓ Входные элементы: {len(self.input_gates)}")
            
            # Проверяем соединения INPUT
            for input_name, input_gate in self.input_gates.items():
                has_output = False
                for conn in self.connections:
                    if conn['from'] == input_name:
                        has_output = True
                        break
                if not has_output:
                    info.append(f"  ⚠️ {input_name} не подключен")
        
        # Проверяем OUTPUT вентили
        if not self.output_gates:
            info.append("⚠️ Нет выходных элементов (OUTPUT)")
        else:
            info.append(f"✓ Выходные элементы: {len(self.output_gates)}")
            
            # Проверяем соединения OUTPUT
            for output_name, output_gate in self.output_gates.items():
                has_input = False
                for conn in self.connections:
                    if conn['to'] == output_name:
                        has_input = True
                        break
                if not has_input:
                    info.append(f"  ⚠️ {output_name} не подключен")
        
        # Проверяем соединения
        if not self.connections:
            info.append("⚠️ Нет соединений между элементами")
        else:
            info.append(f"✓ Соединений: {len(self.connections)}")
        
        # Показываем информацию
        message = "\n".join(info)
        messagebox.showinfo("Проверка схемы", message)
        self.update_status("Проверка схемы завершена")
    
    def update_status(self, message):
        """Обновление статусного сообщения"""
        self.status_label.config(text=message)
    
    def update_info(self):
        """Обновление информации о схеме"""
        elements_count = len(self.gates)
        connections_count = len(self.connections)
        inputs_count = len(self.input_gates)
        outputs_count = len(self.output_gates)
        
        info_text = f"Элементов: {elements_count}\n"
        info_text += f"Соединений: {connections_count}\n"
        info_text += f"Входов: {inputs_count}\n"
        info_text += f"Выходов: {outputs_count}"
        
        self.info_label.config(text=info_text)
    
    def simulate_circuit(self, input_values):
        """Моделирование схемы для заданных входных значений"""
        # Сбрасываем все выходы
        for gate in self.gates.values():
            gate.output = None
            gate.input_values = {}
        
        # 1. Устанавливаем значения входных вентилей
        input_list = list(self.input_gates.items())
        for i, (input_name, input_gate) in enumerate(input_list):
            if i < len(input_values):
                input_gate.output = input_values[i]
            else:
                input_gate.output = False
        
        # 2. Топологическая сортировка для правильного порядка вычислений
        def get_sorted_gates():
            """Получаем вентили в порядке вычислений"""
            visited = set()
            result = []
            
            def visit(gate_name):
                if gate_name in visited:
                    return
                visited.add(gate_name)
                
                gate = self.gates[gate_name]
                # Сначала посещаем все входы
                for input_name in gate.inputs:
                    if input_name in self.gates:
                        visit(input_name)
                
                # Затем добавляем текущий вентиль
                result.append(gate)
            
            # Начинаем с выходных вентилей
            for output_name in self.output_gates:
                visit(output_name)
            
            return result
        
        # 3. Вычисляем вентили в правильном порядке
        sorted_gates = get_sorted_gates()
        
        for gate in sorted_gates:
            if gate.gate_type != 'INPUT':
                # Собираем значения входов
                all_inputs_known = True
                for input_name in gate.inputs:
                    input_gate = self.gates.get(input_name)
                    if input_gate and input_gate.output is not None:
                        gate.input_values[input_name] = input_gate.output
                    else:
                        all_inputs_known = False
                        break
                
                if all_inputs_known and gate.output is None:
                    gate.compute()
        
        # 4. Собираем выходные значения
        outputs = []
        for output_name, output_gate in self.output_gates.items():
            if output_gate.output is not None:
                outputs.append(output_gate.output)
            else:
                # Ищем значение от последнего входного вентиля
                last_value = False
                for input_name in output_gate.inputs:
                    input_gate = self.gates.get(input_name)
                    if input_gate and input_gate.output is not None:
                        last_value = input_gate.output
                        break
                outputs.append(last_value)
        
        return outputs
    
    def show_truth_table(self):
        """Отображение таблицы истинности"""
        # Сначала проверяем схему
        self.check_circuit()
        
        if not self.input_gates:
            messagebox.showerror("Ошибка", "Добавьте входные элементы (INPUT)!")
            return
            
        if not self.output_gates:
            messagebox.showerror("Ошибка", "Добавьте выходные элементы (OUTPUT)!")
            return
        
        if not self.connections:
            messagebox.showwarning("Внимание", "Соедините элементы между собой!")
            return
        
        # Создаем окно для таблицы
        table_window = tk.Toplevel(self.root)
        table_window.title("Таблица истинности")
        table_window.geometry("1000x600")
        table_window.configure(bg=self.colors['bg_main'])
        
        # Заголовок
        header = tk.Frame(table_window, bg=self.colors['bg_header'])
        header.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(header, text="ТАБЛИЦА ИСТИННОСТИ", 
                font=('Segoe UI', 18, 'bold'),
                bg=self.colors['bg_header'],
                fg='white',
                pady=15).pack()
        
        # Информация о схеме
        info_frame = tk.Frame(table_window, bg=self.colors['bg_main'])
        info_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        input_count = len(self.input_gates)
        output_count = len(self.output_gates)
        
        tk.Label(info_frame, text=f"Схема содержит {input_count} входов и {output_count} выходов", 
                font=('Segoe UI', 11),
                bg=self.colors['bg_main'],
                fg=self.colors['text_dark']).pack(anchor='w')
        
        tk.Label(info_frame, text=f"Всего комбинаций: {2**input_count}", 
                font=('Segoe UI', 10),
                bg=self.colors['bg_main'],
                fg=self.colors['text_light']).pack(anchor='w', pady=(2, 0))
        
        # Создаем фрейм для таблицы с прокруткой
        table_frame = tk.Frame(table_window, bg=self.colors['bg_main'])
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Создаем таблицу
        input_names = list(self.input_gates.keys())
        output_names = list(self.output_gates.keys())
        all_names = input_names + output_names
        
        # Создаем Treeview с пользовательским стилем
        style = ttk.Style(table_window)
        style.configure("Custom.Treeview",
                       background=self.colors['bg_main'],
                       foreground=self.colors['text_dark'],
                       fieldbackground=self.colors['bg_main'],
                       borderwidth=0,
                       font=('Segoe UI', 10))
        
        style.configure("Custom.Treeview.Heading",
                       background=self.colors['btn_special'],
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'),
                       borderwidth=0,
                       relief='flat')
        
        tree = ttk.Treeview(table_frame, columns=all_names, show='headings', 
                           height=20, style="Custom.Treeview")
        
        # Настраиваем заголовки
        for name in input_names:
            tree.heading(name, text=f"Вход\n{name}", anchor='center')
            tree.column(name, width=80, anchor='center', minwidth=80)
            
        for name in output_names:
            tree.heading(name, text=f"Выход\n{name}", anchor='center')
            tree.column(name, width=80, anchor='center', minwidth=80)
        
        # Генерируем все комбинации входов
        all_combinations = list(itertools.product([False, True], repeat=input_count))
        
        # Заполняем таблицу
        for combo_idx, combo in enumerate(all_combinations):
            outputs = self.simulate_circuit(combo)
            
            # Форматируем значения
            row_values = []
            for val in combo:
                row_values.append('1' if val else '0')
            for val in outputs:
                row_values.append('1' if val else '0')
            
            # Вставляем строку
            tree.insert('', 'end', values=tuple(row_values))
            
            # Подсвечиваем каждую 2-ю строку для читаемости
            if combo_idx % 2 == 1:
                tree.tag_configure('oddrow', background=self.colors['highlight'])
                tree.item(tree.get_children()[-1], tags=('oddrow',))
        
        # Добавляем полосы прокрутки
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Размещаем элементы
        tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        # Настраиваем расширение
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Кнопка закрытия
        close_btn = tk.Button(table_window, text="ЗАКРЫТЬ",
                            font=('Segoe UI', 10, 'bold'),
                            bg=self.colors['btn_special'],
                            fg='white',
                            activebackground=self.colors['btn_special_hover'],
                            activeforeground='white',
                            relief='flat',
                            borderwidth=0,
                            cursor='hand2',
                            command=table_window.destroy)
        close_btn.pack(pady=(0, 20))

def main():
    root = tk.Tk()
    app = CircuitSimulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()