import tkinter as tk
from tkinter import messagebox
import math

# ---------- Clase Grafo ----------
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
                self.adj_list[user2].append(user1)

    def get_friends(self, user):
        return self.adj_list.get(user, [])

# ---------- Función BFS ----------
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
    level_2_friends -= set(graph.get_friends(start_user))  # Excluir amigos directos
    return list(level_2_friends)

# ---------- Interfaz Gráfica ----------
class SocialApp:
    def __init__(self, root):
        self.graph = Graph()
        self.root = root
        self.root.title("Red Social - Grafo")
        self.positions = {}
        self.radius = 200

        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack()

        self.entry = tk.Entry(root)
        self.entry.pack()

        self.btn_add_user = tk.Button(root, text="Agregar Usuario", command=self.add_user)
        self.btn_add_user.pack()

        self.btn_connect = tk.Button(root, text="Conectar Amigos", command=self.connect_users)
        self.btn_connect.pack()

        self.btn_show_friends = tk.Button(root, text="Ver Amigos", command=self.show_friends)
        self.btn_show_friends.pack()

        self.btn_suggest = tk.Button(root, text="Sugerencias", command=self.suggest_friends)
        self.btn_suggest.pack()

        self.canvas.bind("<Button-1>", self.select_user)
        self.selected_users = []

    def draw_node(self, user):
        angle = len(self.positions) * (2 * math.pi / 20)
        x = 400 + self.radius * math.cos(angle)
        y = 300 + self.radius * math.sin(angle)
        self.positions[user] = (x, y)

        self.canvas.create_oval(x-20, y-20, x+20, y+20, fill="skyblue", tags=("node", user))
        self.canvas.create_text(x, y, text=user, tags=("text", user))

    def draw_edge(self, u1, u2):
        x1, y1 = self.positions[u1]
        x2, y2 = self.positions[u2]
        self.canvas.create_line(x1, y1, x2, y2, fill="black")

    def add_user(self):
        user = self.entry.get().strip()
        if not user:
            messagebox.showwarning("Entrada inválida", "Ingresa un nombre de usuario.")
            return
        if user in self.graph.adj_list:
            messagebox.showwarning("Duplicado", f"{user} ya existe.")
            return
        self.graph.add_user(user)
        self.draw_node(user)
        messagebox.showinfo("Usuario agregado", f"{user} fue agregado.")

    def connect_users(self):
        if len(self.selected_users) == 2:
            u1, u2 = self.selected_users
            if u1 == u2:
                messagebox.showwarning("Conexión inválida", "No puedes conectar un usuario consigo mismo.")
                return
            self.graph.add_friendship(u1, u2)
            self.draw_edge(u1, u2)
            messagebox.showinfo("Conexión", f"{u1} y {u2} ahora son amigos.")
            self.selected_users = []
        else:
            messagebox.showwarning("Conexión", "Haz clic en dos usuarios para conectarlos.")

    def show_friends(self):
        user = self.entry.get().strip()
        if not user:
            messagebox.showwarning("Entrada inválida", "Ingresa un nombre de usuario.")
            return
        friends = self.graph.get_friends(user)
        if friends:
            messagebox.showinfo("Amigos", f"Amigos de {user}: {', '.join(friends)}")
        else:
            messagebox.showinfo("Amigos", f"{user} no tiene amigos aún.")

    def suggest_friends(self):
        user = self.entry.get().strip()
        if not user:
            messagebox.showwarning("Entrada inválida", "Ingresa un nombre de usuario.")
            return
        if user not in self.graph.adj_list:
            messagebox.showwarning("No encontrado", f"{user} no existe en la red.")
            return
        suggestions = bfs_suggestions(self.graph, user)
        if suggestions:
            messagebox.showinfo("Sugerencias", f"Sugerencias de amistad para {user}: {', '.join(suggestions)}")
        else:
            messagebox.showinfo("Sugerencias", f"No hay sugerencias disponibles para {user}.")

    def select_user(self, event):
        clicked = self.canvas.find_closest(event.x, event.y)
        tags = self.canvas.gettags(clicked)
        if len(tags) > 1:
            user = tags[1]
            if user not in self.selected_users:
                self.selected_users.append(user)
                if len(self.selected_users) > 2:
                    self.selected_users = self.selected_users[-2:]

# ---------- Ejecutar aplicación ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = SocialApp(root)
    root.mainloop()
