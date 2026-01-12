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
        self.root.title("Симулятор логических схем")
        self.root.geometry("1200x700")
        
        # Розовая цветовая палитра
        self.colors = {
            'bg_main': '#FFF0F5',
            'bg_sidebar': '#FFE4E1',
            'btn_normal': '#FFB6C1',
            'btn_hover': '#FF69B4',
            'btn_text': '#8B008B',
            'canvas_bg': '#FFFFFF',
            'gate_and': '#FFC0CB',
            'gate_or': '#FFB7C5',
            'gate_not': '#FFA7BA',
            'gate_nand': '#FF9EB5',
            'gate_nor': '#FF8DA1',
            'gate_xor': '#FF7F93',
            'gate_input': '#FFE4EC',
            'gate_output': '#FFD9E6',
            'text': '#C71585',
            'connection': '#DB7093',
            'selected': '#FF1493',
            'input_dot': '#8B008B',
            'output_dot': '#FF1493',
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
        
        style.configure('Pink.TButton',
                       background=self.colors['btn_normal'],
                       foreground=self.colors['btn_text'],
                       font=('Arial', 10, 'bold'),
                       borderwidth=2,
                       relief='raised',
                       padding=8)
        
        style.map('Pink.TButton',
                 background=[('active', self.colors['btn_hover'])],
                 relief=[('pressed', 'sunken')])
        
    def create_widgets(self):
        # Панель инструментов слева
        left_frame = tk.Frame(self.root, width=220, bg=self.colors['bg_sidebar'])
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        left_frame.pack_propagate(False)
        
        # Заголовок
        title_frame = tk.Frame(left_frame, bg=self.colors['bg_sidebar'])
        title_frame.pack(fill=tk.X, pady=(15, 10))
        
        tk.Label(title_frame, text="ЛОГИЧЕСКИЕ ВЕНТИЛИ", 
                font=('Arial', 14, 'bold'), 
                bg=self.colors['bg_sidebar'],
                fg=self.colors['text']).pack()
        
        # Разделитель
        ttk.Separator(left_frame, orient='horizontal').pack(fill=tk.X, padx=10, pady=5)
        
        # Кнопки для добавления вентилей
        gates_frame = tk.Frame(left_frame, bg=self.colors['bg_sidebar'])
        gates_frame.pack(pady=10)
        
        gates = ['AND', 'OR', 'NOT', 'NAND', 'NOR', 'XOR', 'INPUT', 'OUTPUT']
        
        for gate in gates:
            btn = tk.Button(gates_frame, text=gate,
                          font=('Arial', 10, 'bold'),
                          bg=self.colors['btn_normal'],
                          fg=self.colors['btn_text'],
                          activebackground=self.colors['btn_hover'],
                          activeforeground='white',
                          relief='raised',
                          borderwidth=2,
                          width=18,
                          height=1,
                          cursor='hand2',
                          command=lambda g=gate: self.add_gate(g))
            btn.pack(pady=3)
            
            # Эффект при наведении
            btn.bind('<Enter>', lambda e, b=btn: b.configure(
                bg=self.colors['btn_hover']))
            btn.bind('<Leave>', lambda e, b=btn: b.configure(
                bg=self.colors['btn_normal']))
        
        # Разделитель
        ttk.Separator(left_frame, orient='horizontal').pack(fill=tk.X, padx=10, pady=10)
        
        # Панель управления
        control_frame = tk.Frame(left_frame, bg=self.colors['bg_sidebar'])
        control_frame.pack(pady=10)
        
        controls = [
            ('Соединить', self.start_connection),
            ('Удалить', self.delete_selected),
            ('Таблица истинности', self.show_truth_table),
            ('Очистить схему', self.clear_circuit),
            ('Проверить схему', self.check_circuit)  # Добавлена кнопка проверки
        ]
        
        for text, command in controls:
            btn = tk.Button(control_frame, text=text,
                          font=('Arial', 10, 'bold'),
                          bg=self.colors['btn_normal'],
                          fg=self.colors['btn_text'],
                          activebackground=self.colors['btn_hover'],
                          activeforeground='white',
                          relief='raised',
                          borderwidth=2,
                          width=18,
                          height=1,
                          cursor='hand2',
                          command=command)
            btn.pack(pady=3)
            
            # Эффект при наведении
            btn.bind('<Enter>', lambda e, b=btn: b.configure(
                bg=self.colors['btn_hover']))
            btn.bind('<Leave>', lambda e, b=btn: b.configure(
                bg=self.colors['btn_normal']))
        
        # Информационная панель
        info_frame = tk.Frame(left_frame, bg=self.colors['bg_sidebar'])
        info_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        tk.Label(info_frame, text="Инструкция:", 
                font=('Arial', 10, 'bold'),
                bg=self.colors['bg_sidebar'],
                fg=self.colors['text']).pack(anchor='w', padx=10, pady=(0, 5))
        
        instructions = [
            "1. Добавьте вентили",
            "2. Соедините их",
            "3. Нажмите 'Таблица истинности'"
        ]
        
        for instr in instructions:
            tk.Label(info_frame, text=instr,
                    font=('Arial', 9),
                    bg=self.colors['bg_sidebar'],
                    fg=self.colors['text']).pack(anchor='w', padx=20)
        
        # Область рисования схемы
        self.canvas = tk.Canvas(self.root, bg=self.colors['canvas_bg'], 
                               highlightthickness=2,
                               highlightbackground=self.colors['text'])
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
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
    
    def add_gate(self, gate_type):
        """Добавление нового вентиля на схему"""
        name = f"{gate_type}{self.gate_counter[gate_type]}"
        self.gate_counter[gate_type] += 1
        
        gate = LogicGate(gate_type, name, (100, 100))
        self.gates[name] = gate
        
        if gate_type == 'INPUT':
            self.input_gates[name] = gate
            gate.input_values = {'input': False}
        elif gate_type == 'OUTPUT':
            self.output_gates[name] = gate
        
        self.draw_gate(gate)
    
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
        
        # Рисуем прямоугольник для вентиля
        gate.rect = self.canvas.create_rectangle(x-45, y-25, x+45, y+25,
                                                fill=color, 
                                                outline=self.colors['text'],
                                                width=2, 
                                                tags=('gate', gate.name))
        
        # Подписываем вентиль
        self.canvas.create_text(x, y, text=gate.name, 
                               font=('Arial', 10, 'bold'),
                               fill=self.colors['text'],
                               tags=('gate', gate.name))
        
        # Рисуем входы и выходы только для INPUT и OUTPUT
        if gate.gate_type == 'INPUT':
            # Только выход для входного вентиля (справа)
            gate.output_point = self.canvas.create_oval(x+35, y-5, x+45, y+5,
                                                       fill=self.colors['output_dot'], 
                                                       tags=('gate', gate.name, 'output_point'))
        elif gate.gate_type == 'OUTPUT':
            # Только вход для выходного вентиля (слева)
            gate.input_point = self.canvas.create_oval(x-45, y-5, x-35, y+5,
                                                      fill=self.colors['input_dot'], 
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
                                         outline=self.colors['text'])
                
                self.selected_gate = clicked_gate
                
                # Выделяем новый
                self.canvas.itemconfig(self.selected_gate.rect, 
                                     outline=self.colors['selected'],
                                     width=3)
                
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
                        self.update_status(f"Выберите второй вентиль для соединения с {self.selected_gate.name}")
    
    def create_connection(self, gate_from, gate_to):
        """Создание соединения между вентилями"""
        # Проверяем возможность соединения
        if gate_from == gate_to:
            messagebox.showerror("Ошибка", "Нельзя соединять вентиль с самим собой!")
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
                                     tags=('connection',
                                           f"{gate_from.name}-{gate_to.name}"))
        connection['line_id'] = line
        
        self.update_status(f"Соединение создано: {gate_from.name} → {gate_to.name}")
    
    def start_connection(self):
        """Начало процесса соединения"""
        self.connecting = True
        self.update_status("Выберите первый вентиль для соединения")
    
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
            self.update_status("Вентиль удален")
    
    def clear_circuit(self):
        """Очистка всей схемы"""
        if messagebox.askyesno("Очистка", "Удалить всю схему?"):
            self.canvas.delete('all')
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
    
    def check_circuit(self):
        """Проверка схемы на корректность"""
        info = []
        
        # Проверяем INPUT вентили
        if not self.input_gates:
            info.append("❌ Нет входных вентилей (INPUT)")
        else:
            info.append(f"✅ Входные вентили: {len(self.input_gates)}")
            
            # Проверяем соединения INPUT
            for input_name, input_gate in self.input_gates.items():
                has_output = False
                for conn in self.connections:
                    if conn['from'] == input_name:
                        has_output = True
                        break
                if not has_output:
                    info.append(f"⚠️ {input_name} никуда не подключен")
        
        # Проверяем OUTPUT вентили
        if not self.output_gates:
            info.append("❌ Нет выходных вентилей (OUTPUT)")
        else:
            info.append(f"✅ Выходные вентили: {len(self.output_gates)}")
            
            # Проверяем соединения OUTPUT
            for output_name, output_gate in self.output_gates.items():
                has_input = False
                for conn in self.connections:
                    if conn['to'] == output_name:
                        has_input = True
                        break
                if not has_input:
                    info.append(f"⚠️ {output_name} ни к чему не подключен")
        
        # Проверяем соединения
        if not self.connections:
            info.append("❌ Нет соединений между вентилями")
        else:
            info.append(f"✅ Соединений: {len(self.connections)}")
        
        # Проверяем логические вентили
        logic_gates = [g for g in self.gates.values() if g.gate_type not in ['INPUT', 'OUTPUT']]
        if logic_gates:
            info.append(f"✅ Логические вентили: {len(logic_gates)}")
            
            # Проверяем соединения логических вентилей
            for gate in logic_gates:
                # Проверяем входы
                if not gate.inputs:
                    info.append(f"⚠️ {gate.name} не имеет входов")
                else:
                    info.append(f"✅ {gate.name} имеет {len(gate.inputs)} вход(ов)")
                
                # Проверяем выходы
                has_output = False
                for conn in self.connections:
                    if conn['from'] == gate.name:
                        has_output = True
                        break
                if not has_output and gate.gate_type != 'NOT':  # NOT может быть без выхода
                    info.append(f"⚠️ {gate.name} не имеет выходов")
        
        # Показываем информацию
        message = "\n".join(info)
        messagebox.showinfo("Проверка схемы", message)
    
    def update_status(self, message):
        """Обновление статусного сообщения"""
        self.root.title(f"Симулятор логических схем - {message}")
    
    def simulate_circuit(self, input_values):
        """Моделирование схемы для заданных входных значений"""
        # Отладочная информация
        print(f"\n=== Начало симуляции с входными значениями: {input_values} ===")
        
        # Сбрасываем все выходы
        for gate in self.gates.values():
            gate.output = None
            gate.input_values = {}
        
        # 1. Устанавливаем значения входных вентилей
        input_list = list(self.input_gates.items())
        for i, (input_name, input_gate) in enumerate(input_list):
            if i < len(input_values):
                input_gate.output = input_values[i]
                print(f"  INPUT {input_name} = {input_gate.output}")
            else:
                input_gate.output = False
                print(f"  INPUT {input_name} = {input_gate.output} (по умолчанию)")
        
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
                    old_output = gate.output
                    gate.compute()
                    print(f"  {gate.name} ({gate.gate_type}) входы={gate.input_values} выход={gate.output}")
                    if gate.output != old_output:
                        pass
        
        # 4. Собираем выходные значения
        outputs = []
        for output_name, output_gate in self.output_gates.items():
            if output_gate.output is not None:
                outputs.append(output_gate.output)
                print(f"  OUTPUT {output_name} = {output_gate.output} (из самого вентиля)")
            else:
                # Ищем значение от последнего входного вентиля
                last_value = False
                for input_name in output_gate.inputs:
                    input_gate = self.gates.get(input_name)
                    if input_gate and input_gate.output is not None:
                        last_value = input_gate.output
                        break
                outputs.append(last_value)
                print(f"  OUTPUT {output_name} = {last_value} (от входного вентиля)")
        
        print(f"=== Конец симуляции. Выходы: {outputs} ===\n")
        return outputs
    
    def show_truth_table(self):
        """Отображение таблицы истинности"""
        # Сначала проверяем схему
        self.check_circuit()
        
        if not self.input_gates:
            messagebox.showerror("Ошибка", "Добавьте входные вентили (INPUT)!")
            return
            
        if not self.output_gates:
            messagebox.showerror("Ошибка", "Добавьте выходные вентили (OUTPUT)!")
            return
        
        if not self.connections:
            messagebox.showwarning("Внимание", "Соедините вентили между собой!")
            return
        
        # Создаем окно для таблицы
        table_window = tk.Toplevel(self.root)
        table_window.title("Таблица истинности")
        table_window.geometry("900x500")
        table_window.configure(bg=self.colors['bg_main'])
        
        # Заголовок
        header = tk.Frame(table_window, bg=self.colors['bg_main'])
        header.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        input_count = len(self.input_gates)
        output_count = len(self.output_gates)
        tk.Label(header, text=f"Таблица истинности: {input_count} входов, {output_count} выходов", 
                font=('Arial', 12, 'bold'),
                bg=self.colors['bg_main'],
                fg=self.colors['text']).pack()
        
        # Информация о схеме
        info_text = f"Схема: {len(self.gates)} вентилей, {len(self.connections)} соединений"
        tk.Label(header, text=info_text,
                font=('Arial', 10),
                bg=self.colors['bg_main'],
                fg=self.colors['text']).pack()
        
        # Создаем фрейм для таблицы с прокруткой
        table_frame = tk.Frame(table_window)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Создаем таблицу
        input_names = list(self.input_gates.keys())
        output_names = list(self.output_gates.keys())
        all_names = input_names + output_names
        
        # Создаем Treeview
        tree = ttk.Treeview(table_frame, columns=all_names, show='headings', height=20)
        
        # Настраиваем заголовки
        for name in input_names:
            tree.heading(name, text=f"Вход:\n{name}", anchor='center')
            tree.column(name, width=80, anchor='center')
            
        for name in output_names:
            tree.heading(name, text=f"Выход:\n{name}", anchor='center')
            tree.column(name, width=80, anchor='center')
        
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
                tree.tag_configure('oddrow', background='#FFF0F5')
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
        close_btn = tk.Button(table_window, text="Закрыть таблицу",
                            font=('Arial', 10, 'bold'),
                            bg=self.colors['btn_normal'],
                            fg=self.colors['btn_text'],
                            activebackground=self.colors['btn_hover'],
                            activeforeground='white',
                            relief='raised',
                            borderwidth=2,
                            command=table_window.destroy)
        close_btn.pack(pady=10)

def main():
    root = tk.Tk()
    app = CircuitSimulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()