import tkinter as tk
from tkinter import messagebox
import math

# Clase Grafo dirigido usando listas de adyacencia
class Graph:
    def __init__(self):
        self.adj_list = {}

    def add_user(self, user):
        if user not in self.adj_list:
            self.adj_list[user] = []

    def add_friendship(self, user1, user2):
        if user1 in self.adj_list and user2 in self.adj_list:
            if user2 not in self.adj_list[user1]:
                self.adj_list[user1].append(user2)

    def get_friends(self, user):
        return self.adj_list.get(user, [])

# BFS para sugerencias de amistad a nivel 2
def bfs_suggestions(graph, start_user):
    visited = set()
    queue = [(start_user, 0)]
    level_2_friends = set()

    while queue:
        current, level = queue.pop(0)
        if current not in visited:
            visited.add(current)
            if level == 2:
                level_2_friends.add(current)
            elif level < 2:
                for neighbor in graph.get_friends(current):
                    queue.append((neighbor, level + 1))

    level_2_friends.discard(start_user)
    level_2_friends -= set(graph.get_friends(start_user))
    return list(level_2_friends)

# Aplicación con Tkinter
class SocialApp:
    def __init__(self, root):
        self.graph = Graph()
        self.root = root
        self.root.title("Red Social")
        self.positions = {}

        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack()

        control_frame = tk.Frame(root)
        control_frame.pack(pady=10)

        self.entry_user = tk.Entry(control_frame)
        self.entry_user.grid(row=0, column=0, padx=5)
        tk.Button(control_frame, text="Agregar Usuario", command=self.add_user).grid(row=0, column=1, padx=5)
        tk.Button(control_frame, text="Conectar Amigos", command=self.connect_users).grid(row=0, column=2, padx=5)

        self.results = tk.Text(root, height=6, state='disabled')
        self.results.pack(fill='x', padx=10, pady=5)

        self.selected_users = []
        self.moving_node = None
        self.canvas.bind("<Button-1>", self.select_user)
        self.canvas.bind("<B1-Motion>", self.drag_user)
        self.canvas.bind("<ButtonRelease-1>", self.release_user)

    def draw_node(self, user):
        x, y = 100 + len(self.positions) * 100, 100
        self.positions[user] = (x, y)

        self.canvas.create_oval(x-20, y-20, x+20, y+20, fill="skyblue", tags=("node", user))
        self.canvas.create_text(x, y, text=user, tags=("text", user))

    def draw_edges(self):
        self.canvas.delete("edge")
        for u in self.graph.adj_list:
            for v in self.graph.get_friends(u):
                if u in self.positions and v in self.positions:
                    x1, y1 = self.positions[u]
                    x2, y2 = self.positions[v]
                    self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, tags="edge")

    def add_user(self):
        user = self.entry_user.get().strip()
        if not user:
            messagebox.showwarning("Entrada inválida", "Ingresa un nombre de usuario.")
            return
        if user in self.graph.adj_list:
            messagebox.showwarning("Duplicado", f"{user} ya existe.")
            return
        self.graph.add_user(user)
        self.draw_node(user)
        self.entry_user.delete(0, tk.END)

    def connect_users(self):
        if len(self.selected_users) == 2:
            u1, u2 = self.selected_users
            if u1 == u2:
                messagebox.showwarning("Conexión inválida", "No puedes conectar un usuario consigo mismo.")
                return
            self.graph.add_friendship(u1, u2)
            self.draw_edges()
            self.selected_users = []
            self.show_results(u1)
            self.show_results(u2)
        else:
            messagebox.showinfo("Conectar", "Selecciona dos usuarios haciendo clic para conectarlos.")

    def show_results(self, user):
        friends = self.graph.get_friends(user)
        suggestions = bfs_suggestions(self.graph, user)
        self.results.config(state='normal')
        self.results.delete(1.0, tk.END)
        self.results.insert(tk.END, f"Usuario seleccionado: {user}\n")
        self.results.insert(tk.END, f"Amigos directos: {', '.join(friends) if friends else 'Ninguno'}\n")
        self.results.insert(tk.END, f"Sugerencias de amistad: {', '.join(suggestions) if suggestions else 'Ninguna'}\n")
        self.results.config(state='disabled')

    def select_user(self, event):
        clicked = self.canvas.find_closest(event.x, event.y)
        tags = self.canvas.gettags(clicked)
        if len(tags) > 1:
            user = tags[1]
            if user not in self.selected_users:
                self.selected_users.append(user)
                if len(self.selected_users) > 2:
                    self.selected_users = self.selected_users[-2:]
            self.show_results(user)
            self.moving_node = user

    def drag_user(self, event):
        if self.moving_node:
            x, y = event.x, event.y
            self.positions[self.moving_node] = (x, y)
            self.redraw()

    def release_user(self, event):
        self.moving_node = None

    def redraw(self):
        self.canvas.delete("all")
        for user in self.positions:
            x, y = self.positions[user]
            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill="skyblue", tags=("node", user))
            self.canvas.create_text(x, y, text=user, tags=("text", user))
        self.draw_edges()

if __name__ == "__main__":
    root = tk.Tk()
    app = SocialApp(root)
    root.mainloop()
