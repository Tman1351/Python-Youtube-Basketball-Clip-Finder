import tkinter as tk
from tkinter import ttk, messagebox
import threading
import webbrowser
import os
from dotenv import load_dotenv
from datetime import datetime
from typing import List, Dict, Any
from googleapiclient.discovery import build

load_dotenv()  # Load .env variables

class APIKeys:
    def __init__(self):
        self.youtube_key = os.getenv('YOUTUBE_API_KEY')

        # Debug log to check loaded environment variables
        print("[DEBUG] Loaded Environment Variables:")
        print(f"  YOUTUBE_API_KEY: {'set' if self.youtube_key else 'missing'}")

class HighlightSearcher:
    def __init__(self):
        self.api_keys = APIKeys()
        self.clients = {}
        self.last_error = None
        self._initialize_clients()

    def _initialize_clients(self):
        try:
            self.clients['youtube'] = build(
                'youtube', 'v3',
                developerKey=self.api_keys.youtube_key,
                cache_discovery=False
            )
            print("[DEBUG] YouTube client initialized")
        except Exception as e:
            print(f"[ERROR] Failed to initialize YouTube client: {e}")

    def search(self, query: str, max_results: int = 5, order: str = "relevance") -> List[Dict[str, Any]]:
        results = []
        self.last_error = None

        print(f"[DEBUG] Starting YouTube search for query: '{query}' with order: '{order}'")

        if 'youtube' in self.clients:
            try:
                response = self.clients['youtube'].search().list(
                    q=f"{query} basketball highlights",
                    part='snippet',
                    type='video',
                    maxResults=max_results,
                    order=order
                ).execute()

                for item in response.get('items', []):
                    results.append({
                        "platform": "YouTube",
                        "title": item['snippet']['title'],
                        "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                        "upload_date": item['snippet']['publishedAt'],
                        "score": 0
                    })
                print(f"[DEBUG] YouTube: Found {len(results)} videos")

            except Exception as e:
                self.last_error = f"YouTube API error: {e}"
                print(f"[ERROR] {self.last_error}")

        if not results:
            self.last_error = "No highlights found. Try different keywords."
            print("[DEBUG] No results found.")

        return results


class HighlightApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Basketball Highlights Aggregator")
        self.geometry("900x600")
        self.searcher = HighlightSearcher()
        self._create_widgets()

    def _create_widgets(self):
        frame = ttk.Frame(self, padding="5")
        frame.pack(fill=tk.X)

        self.search_entry = ttk.Entry(frame, width=50)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.search_entry.bind("<Return>", lambda e: self.start_search())

        self.search_button = ttk.Button(frame, text="Search", command=self.start_search)
        self.search_button.pack(side=tk.LEFT)

        ttk.Label(frame, text="Sort by:").pack(side=tk.LEFT, padx=(10, 2))

        self.order_var = tk.StringVar(value="relevance")
        self.order_combo = ttk.Combobox(
            frame,
            textvariable=self.order_var,
            state="readonly",
            values=["relevance", "date", "viewCount", "rating", "title"],
            width=12
        )
        self.order_combo.pack(side=tk.LEFT)

        self.status_label = ttk.Label(frame, text="Ready")
        self.status_label.pack(side=tk.RIGHT)

        self.tree = ttk.Treeview(self, columns=("Platform", "Title", "Date", "URL"), show="headings")
        for col, width in [("Platform", 100), ("Title", 400), ("Date", 150), ("URL", 300)]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.tree.bind("<Double-1>", self.open_url)

    def start_search(self):
        query = self.search_entry.get().strip()
        if not query:
            messagebox.showwarning("Input Required", "Please enter search keywords.")
            return

        order = self.order_var.get()

        self.search_button.config(state='disabled')
        self.status_label.config(text="Searching...")
        self.tree.delete(*self.tree.get_children())
        threading.Thread(target=self._run_search, args=(query, order), daemon=True).start()

    def _run_search(self, query, order):
        results = self.searcher.search(query, order=order)
        if not results:
            self.after(0, lambda: messagebox.showinfo("No Results", str(self.searcher.last_error)))
        else:
            self.after(0, self.update_results, results)
        self.after(0, lambda: self.search_button.config(state='normal'))
        self.after(0, lambda: self.status_label.config(text="Ready"))

    def update_results(self, results):
        for res in results:
            self.tree.insert("", "end", values=(
                res["platform"],
                res["title"],
                res["upload_date"],
                res["url"]
            ))

    def open_url(self, event):
        selected = self.tree.selection()
        if selected:
            url = self.tree.item(selected[0])["values"][3]
            webbrowser.open_new_tab(url)


def main():
    app = HighlightApp()
    app.mainloop()


if __name__ == "__main__":
    main()
