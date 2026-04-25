import threading

import customtkinter as ctk
from tkinter import filedialog, messagebox

from ai_service import (
    generate_topic_proposals,
    stream_article_text,
)
from history_service import save_article, load_history, delete_article
from usage_service import can_use_ai, get_usage_status, register_ai_use
from word_service import get_default_docx_filename, save_to_word


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Generator artykułów")
        self.geometry("980x760")
        self.minsize(900, 700)
        self.configure(fg_color="#FFFFFF")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.usage_status_text = ctk.StringVar(value="")
        self.selected_topic = ctk.StringVar(value="")
        self.proposals_status_text = ctk.StringVar(value="")
        self.article_status_text = ctk.StringVar(value="")
        self.content_type_var = ctk.StringVar(value="Blog")

        self.history_entries = []
        self.history_selected_id = None

        self._build_header()
        self._build_tabs()

        self._build_section_topic()
        self._build_section_proposals()
        self._build_section_article()
        self._build_history_tab()

        self.show_proposals_button.configure(command=self.generate_topics)
        self.generate_article_button.configure(command=self.choose_topic)
        self.save_word_button.configure(command=self.handle_save_to_word)

        self.refresh_usage_label()
        self._load_history_tab()

    def _build_header(self):
        self.header_frame = ctk.CTkFrame(self, fg_color="#FFFFFF")
        self.header_frame.grid(row=0, column=0, padx=24, pady=(24, 12), sticky="ew")
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.header_label = ctk.CTkLabel(
            self.header_frame,
            text="Generator artykułów AI",
            text_color="#54595F",
            font=ctk.CTkFont(size=28, weight="bold"),
        )
        self.header_label.grid(row=0, column=0)

        self.subtitle_label = ctk.CTkLabel(
            self.header_frame,
            text="Wygodnie twórz i zapisuj gotowe artykuły w kilku krokach.",
            text_color="#7A7A7A",
            font=ctk.CTkFont(size=14),
        )
        self.subtitle_label.grid(row=1, column=0, pady=(4, 0))

    def _build_tabs(self):
        self.tab_view = ctk.CTkTabview(
            self,
            corner_radius=16,
            fg_color="#FFFFFF",
            segmented_button_fg_color="#F8FAFC",
            segmented_button_selected_color="#2A95CF",
            segmented_button_selected_hover_color="#5AB3DC",
            segmented_button_unselected_color="#F8FAFC",
            segmented_button_unselected_hover_color="#E2E8F0",
            text_color="#54595F",
            text_color_disabled="#9CA3AF",
        )
        self.tab_view.grid(row=1, column=0, padx=24, pady=(0, 24), sticky="nsew")

        self.tab_view.add("Generator")
        self.tab_view.add("Historia")

        self.generator_tab = self.tab_view.tab("Generator")
        self.history_tab = self.tab_view.tab("Historia")

        self.generator_tab.grid_columnconfigure(0, weight=1)
        self.generator_tab.grid_rowconfigure(0, weight=1)

        self.history_tab.grid_columnconfigure(0, weight=1)
        self.history_tab.grid_rowconfigure(1, weight=1)
        self.history_tab.grid_rowconfigure(2, weight=1)

        self.main_container = ctk.CTkFrame(self.generator_tab, corner_radius=16, fg_color="#FFFFFF")
        self.main_container.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=0, minsize=280)
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        self.sidebar_wrapper = ctk.CTkFrame(self.main_container, corner_radius=12, fg_color="#F8FAFC")
        self.sidebar_wrapper.grid(row=0, column=0, padx=(16, 8), pady=16, sticky="nsew")
        self.sidebar_wrapper.grid_propagate(False)
        self.sidebar_wrapper.configure(width=280)
        self.sidebar_wrapper.grid_columnconfigure(0, weight=1)
        self.sidebar_wrapper.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self.sidebar_wrapper, corner_radius=12, fg_color="#F8FAFC")
        self.sidebar_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.sidebar_frame.grid_propagate(False)
        self.sidebar_frame.configure(width=280)
        self.sidebar_frame.grid_columnconfigure(0, weight=1)
        self.sidebar_frame.grid_rowconfigure(3, weight=1)

        self.sidebar_right_border = ctk.CTkFrame(self.sidebar_wrapper, corner_radius=0, fg_color="#E2E8F0", width=1)
        self.sidebar_right_border.place(relx=1.0, rely=0, relheight=1, anchor="ne")

        self.article_area = ctk.CTkFrame(self.main_container, corner_radius=12, fg_color="#FFFFFF")
        self.article_area.grid(row=0, column=1, padx=(8, 16), pady=16, sticky="nsew")
        self.article_area.grid_columnconfigure(0, weight=1)
        self.article_area.grid_rowconfigure(0, weight=1)

    def _build_section_topic(self):
        self.section_topic = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.section_topic.grid(row=0, column=0, padx=14, pady=(14, 10), sticky="ew")
        self.section_topic.grid_columnconfigure(0, weight=1)

        self.content_type_label = ctk.CTkLabel(
            self.section_topic,
            text="Typ treści",
            text_color="#54595F",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.content_type_label.grid(row=0, column=0, pady=(0, 4), sticky="w")

        self.content_type_dropdown = ctk.CTkOptionMenu(
            self.section_topic,
            variable=self.content_type_var,
            values=["Blog", "Facebook", "LinkedIn"],
            fg_color="#FFFFFF",
            button_color="#2A95CF",
            button_hover_color="#5AB3DC",
            text_color="#54595F",
            dropdown_fg_color="#FFFFFF",
            dropdown_text_color="#54595F",
        )
        self.content_type_dropdown.grid(row=1, column=0, pady=(0, 12), sticky="ew")

        self.topic_entry = ctk.CTkEntry(
            self.section_topic,
            placeholder_text="Np. Jak skutecznie promować firmę lokalnie",
            fg_color="#FFFFFF",
            border_color="#E2E8F0",
            border_width=1,
            text_color="#54595F",
            placeholder_text_color="#9CA3AF",
            height=40,
            corner_radius=6,
            justify="left",
        )
        self.topic_entry.grid(row=2, column=0, pady=(0, 12), sticky="ew")

        self.show_proposals_button = ctk.CTkButton(
            self.section_topic,
            text="Pokaż propozycje",
            fg_color="#2A95CF",
            hover_color="#5AB3DC",
            text_color="#FFFFFF",
            height=40,
            corner_radius=8,
            border_width=0,
            text_color_disabled="#9CA3AF",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        self.show_proposals_button.grid(row=3, column=0, pady=(0, 0), sticky="ew")

    def _build_section_proposals(self):
        self.sidebar_separator = ctk.CTkFrame(self.sidebar_frame, height=1, corner_radius=0, fg_color="#E2E8F0")
        self.sidebar_separator.grid(row=1, column=0, padx=14, pady=(0, 10), sticky="ew")

        self.section_proposals = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.section_proposals.grid(row=2, column=0, padx=14, pady=(0, 8), sticky="nsew")
        self.section_proposals.grid_columnconfigure(0, weight=1)
        self.section_proposals.grid_rowconfigure(1, weight=1)

        self.proposals_status_label = ctk.CTkLabel(
            self.section_proposals,
            textvariable=self.proposals_status_text,
            text_color="#7A7A7A",
            font=ctk.CTkFont(size=14),
        )
        self.proposals_status_label.grid(row=0, column=0, pady=(0, 8), sticky="w")

        self.options_frame = ctk.CTkScrollableFrame(
            self.section_proposals,
            corner_radius=10,
            fg_color="#FFFFFF",
            border_color="#E2E8F0",
            border_width=1,
        )
        self.options_frame.grid(row=1, column=0, pady=(0, 10), sticky="nsew")
        self.options_frame.grid_columnconfigure(0, weight=1)

        self.action_buttons_row = ctk.CTkFrame(self.section_proposals, fg_color="transparent")
        self.action_buttons_row.grid(row=2, column=0, pady=(0, 0), sticky="ew")
        self.action_buttons_row.grid_columnconfigure(0, weight=1)

        self.generate_article_button = ctk.CTkButton(
            self.action_buttons_row,
            text="Generuj artykuł",
            fg_color="#2A95CF",
            hover_color="#5AB3DC",
            text_color="#FFFFFF",
            height=40,
            corner_radius=8,
            border_width=0,
            text_color_disabled="#9CA3AF",
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        self.generate_article_button.grid(row=0, column=0, sticky="ew")

        self.usage_status_label = ctk.CTkLabel(
            self.sidebar_frame,
            textvariable=self.usage_status_text,
            text_color="#7A7A7A",
            font=ctk.CTkFont(size=13),
            justify="left",
            anchor="w",
        )
        self.usage_status_label.grid(row=4, column=0, padx=14, pady=(8, 14), sticky="ew")

    def _build_section_article(self):
        self.section_article = ctk.CTkFrame(self.article_area, corner_radius=12, fg_color="#FFFFFF")
        self.section_article.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.section_article.grid_columnconfigure(0, weight=1)
        self.section_article.grid_rowconfigure(1, weight=1)

        self.article_header_row = ctk.CTkFrame(self.section_article, fg_color="transparent", height=60)
        self.article_header_row.grid(row=0, column=0, padx=16, pady=(12, 6), sticky="ew")
        self.article_header_row.grid_columnconfigure(0, weight=0)
        self.article_header_row.grid_columnconfigure(1, weight=1)

        self.section_article_title = ctk.CTkLabel(
            self.article_header_row,
            text="Wygenerowany artykuł",
            text_color="#54595F",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.section_article_title.grid(row=0, column=0, sticky="w")

        self.article_status_label = ctk.CTkLabel(
            self.article_header_row,
            textvariable=self.article_status_text,
            text_color="#7A7A7A",
            font=ctk.CTkFont(size=14),
        )
        self.article_status_label.grid(row=0, column=1, padx=(12, 0), sticky="w")

        self.article_textbox = ctk.CTkTextbox(
            self.section_article,
            corner_radius=6,
            wrap="word",
            fg_color="#FFFFFF",
            border_color="#E2E8F0",
            border_width=1,
            text_color="#54595F",
        )
        self.article_textbox.grid(row=1, column=0, padx=16, pady=(0, 12), sticky="nsew")

        self.save_word_button = ctk.CTkButton(
            self.section_article,
            text="Zapisz do Worda",
            fg_color="#2A95CF",
            hover_color="#5AB3DC",
            text_color="#FFFFFF",
            height=40,
            corner_radius=8,
            border_width=0,
            text_color_disabled="#9CA3AF",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        self.save_word_button.grid(row=2, column=0, padx=16, pady=(0, 14), sticky="e")

    def _build_history_tab(self):
        self.history_controls = ctk.CTkFrame(self.history_tab, fg_color="transparent")
        self.history_controls.grid(row=0, column=0, padx=16, pady=(14, 8), sticky="ew")
        self.history_controls.grid_columnconfigure(0, weight=1)

        self.refresh_history_button = ctk.CTkButton(
            self.history_controls,
            text="Odśwież",
            fg_color="#2A95CF",
            hover_color="#5AB3DC",
            text_color="#FFFFFF",
            height=40,
            corner_radius=8,
            border_width=0,
            text_color_disabled="#9CA3AF",
            command=self._load_history_tab,
        )
        self.refresh_history_button.grid(row=0, column=0, sticky="w")

        self.history_list_frame = ctk.CTkScrollableFrame(self.history_tab, corner_radius=12)
        self.history_list_frame.grid(row=1, column=0, padx=16, pady=(0, 10), sticky="nsew")
        self.history_list_frame.grid_columnconfigure(0, weight=1)

        self.history_preview = ctk.CTkTextbox(self.history_tab, corner_radius=12, wrap="word")
        self.history_preview.grid(row=2, column=0, padx=16, pady=(0, 14), sticky="nsew")

    def _truncate_topic(self, topic):
        topic = topic.strip()
        if len(topic) <= 60:
            return topic
        return topic[:60].rstrip() + "..."

    def _select_history_entry(self, entry):
        self.history_selected_id = entry["id"]
        self.history_preview.delete("1.0", "end")
        self.history_preview.insert("1.0", entry.get("text", ""))

    def _delete_history_entry(self, article_id):
        delete_article(article_id)

        if self.history_selected_id == article_id:
            self.history_selected_id = None
            self.history_preview.delete("1.0", "end")

        self._load_history_tab()

    def _load_history_tab(self):
        self.history_entries = load_history()

        for widget in self.history_list_frame.winfo_children():
            widget.destroy()

        if not self.history_entries:
            self.history_selected_id = None
            self.history_preview.delete("1.0", "end")
            empty_label = ctk.CTkLabel(self.history_list_frame, text="Brak zapisanych artykułów.")
            empty_label.grid(row=0, column=0, padx=8, pady=8, sticky="w")
            return

        for idx, entry in enumerate(self.history_entries):
            row = ctk.CTkFrame(self.history_list_frame, corner_radius=10)
            row.grid(row=idx, column=0, padx=4, pady=4, sticky="ew")
            row.grid_columnconfigure(0, weight=1)

            summary = f"{entry.get('date', '')} | {entry.get('content_type', '')} | {self._truncate_topic(entry.get('topic', ''))}"
            row_label = ctk.CTkLabel(row, text=summary, anchor="w")
            row_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

            delete_button = ctk.CTkButton(
                row,
                text="Usuń",
                width=90,
                command=lambda article_id=entry["id"]: self._delete_history_entry(article_id),
            )
            delete_button.grid(row=0, column=1, padx=10, pady=8)

            row.bind("<Button-1>", lambda _event, item=entry: self._select_history_entry(item))
            row_label.bind("<Button-1>", lambda _event, item=entry: self._select_history_entry(item))

    def set_action_buttons_enabled(self, enabled):
        state = "normal" if enabled else "disabled"
        self.show_proposals_button.configure(state=state)
        self.generate_article_button.configure(state=state)
        self.save_word_button.configure(state=state)

    def refresh_usage_label(self):
        status = get_usage_status()
        self.usage_status_text.set(f"Pozostało użyć AI: {status['remaining']} / {status['limit']}")

    def on_topics_success(self, proposals):
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        self.selected_topic.set("")

        options_label = ctk.CTkLabel(self.options_frame, text="Wybierz jeden z tematów:")
        options_label.pack(anchor="w")

        for proposal in proposals:
            radio = ctk.CTkRadioButton(
                self.options_frame,
                text=proposal,
                variable=self.selected_topic,
                value=proposal,
            )
            radio.pack(anchor="w", pady=5)

        self.proposals_status_text.set("Gotowe")
        self.set_action_buttons_enabled(True)

    def on_topics_error(self, error_text):
        messagebox.showerror("Błąd", f"Błąd generowania propozycji: {error_text}")
        self.proposals_status_text.set("")
        self.set_action_buttons_enabled(True)

    def on_article_success(self, article):
        if not article:
            self.article_status_text.set("")
            self.set_action_buttons_enabled(True)
            return

        self.article_textbox.delete("1.0", "end")
        self.article_textbox.insert("1.0", article)
        self.article_status_text.set("Gotowe")
        self.set_action_buttons_enabled(True)

    def on_article_error(self):
        messagebox.showerror("Błąd", "Błąd generowania artykułu")
        self.article_status_text.set("")
        self.set_action_buttons_enabled(True)

    def on_article_stream_done(self):
        self.article_status_text.set("Gotowe")
        save_article(
            self.selected_topic.get(),
            self.content_type_var.get(),
            self.article_textbox.get("1.0", "end").strip(),
        )
        self._load_history_tab()
        self.set_action_buttons_enabled(True)

    def generate_topics(self):
        topic = self.topic_entry.get().strip()
        content_type = self.content_type_var.get().strip()

        if not topic:
            self.proposals_status_text.set("")
            messagebox.showwarning("Uwaga", "Wpisz temat artykułu")
            return

        if not can_use_ai():
            messagebox.showwarning("Limit AI", "Osiągnięto dzienny limit użyć AI")
            self.refresh_usage_label()
            return

        self.proposals_status_text.set("Generowanie propozycji...")
        self.set_action_buttons_enabled(False)

        def worker():
            try:
                proposals = generate_topic_proposals(topic, content_type)
                register_ai_use()
                self.after(0, self.refresh_usage_label)
                self.after(0, lambda: self.on_topics_success(proposals))
            except Exception as e:
                error_text = str(e)
                print(f"Błąd generowania propozycji: {error_text}")
                self.after(0, lambda: self.on_topics_error(error_text))

        threading.Thread(target=worker, daemon=True).start()

    def choose_topic(self):
        chosen = self.selected_topic.get().strip()
        content_type = self.content_type_var.get().strip()

        if not chosen:
            self.article_status_text.set("")
            messagebox.showwarning("Uwaga", "Wybierz jedną propozycję")
            return

        if not can_use_ai():
            messagebox.showwarning("Limit AI", "Osiągnięto dzienny limit użyć AI")
            self.refresh_usage_label()
            return

        self.article_textbox.delete("1.0", "end")
        self.article_status_text.set("Tworzenie artykułu...")
        self.set_action_buttons_enabled(False)

        def worker():
            try:
                for chunk in stream_article_text(chosen, content_type):
                    self.after(0, lambda c=chunk: self.article_textbox.insert("end", c))
                register_ai_use()
                self.after(0, self.refresh_usage_label)
                self.after(0, self.on_article_stream_done)
            except Exception as e:
                error_text = str(e)
                print(f"Błąd generowania artykułu: {error_text}")
                self.after(0, self.on_article_error)

        threading.Thread(target=worker, daemon=True).start()

    def handle_save_to_word(self):
        article = self.article_textbox.get("1.0", "end").strip()
        topic_for_name = self.selected_topic.get().strip()

        if not article:
            messagebox.showwarning("Uwaga", "Najpierw wygeneruj artykuł")
            return

        default_file_name = get_default_docx_filename(topic_for_name)
        file_path = filedialog.asksaveasfilename(
            title="Zapisz artykuł do Worda",
            defaultextension=".docx",
            filetypes=[("Dokumenty Word", "*.docx")],
            initialfile=default_file_name,
        )

        if not file_path:
            return

        save_to_word(article, file_path)


if __name__ == "__main__":
    app = App()
    app.mainloop()
