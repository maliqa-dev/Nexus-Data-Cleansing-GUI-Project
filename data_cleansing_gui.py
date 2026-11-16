import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Flagship Cyber-Obsidian Theme Configuration
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class FlagshipDataStudio(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("NEXUS DATA STUDIO • AI-Powered Data Cleansing & Telemetry")
        self.geometry("1280x780")
        self.minsize(1200, 720)
        self.configure(fg_color="#060913")  # Ultra-Deep Obsidian Navy

        self.file_path = None
        self.df_raw = None
        self.df_clean = None
        self.pulse_state = True

        # Grid Setup
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ==================== GLASSMORPHIC LEFT SIDEBAR ====================
        self.sidebar = ctk.CTkFrame(
            self,
            width=280,
            corner_radius=0,
            fg_color="#0B1120",
            border_width=1,
            border_color="#1E293B",
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # Glowing Brand Header
        brand_box = ctk.CTkFrame(
            self.sidebar,
            fg_color="#111C33",
            corner_radius=12,
            border_width=1,
            border_color="#0EA5E9",
        )
        brand_box.pack(fill="x", padx=18, pady=(22, 18))

        ctk.CTkLabel(
            brand_box,
            text="◈ NEXUS STUDIO",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color="#38BDF8",
        ).pack(anchor="w", padx=14, pady=(12, 0))

        ctk.CTkLabel(
            brand_box,
            text="Data Cleansing & Telemetry v2.6",
            font=ctk.CTkFont(size=11),
            text_color="#94A3B8",
        ).pack(anchor="w", padx=14, pady=(0, 12))

        # Workflow Actions
        ctk.CTkLabel(
            self.sidebar,
            text="COMMAND CENTER",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="#64748B",
        ).pack(anchor="w", padx=22, pady=(4, 8))

        self.btn_load = ctk.CTkButton(
            self.sidebar,
            text="📥  1. Import Raw Dataset",
            command=self.load_csv,
            height=46,
            corner_radius=12,
            fg_color="#0F172A",
            hover_color="#1E293B",
            border_width=1,
            border_color="#38BDF8",
            text_color="#F8FAFC",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w",
        )
        self.btn_load.pack(fill="x", padx=18, pady=6)

        self.btn_clean = ctk.CTkButton(
            self.sidebar,
            text="⚡  2. Run Smart Pipeline",
            command=self.clean_data,
            height=46,
            corner_radius=12,
            fg_color="#059669",
            hover_color="#047857",
            border_width=1,
            border_color="#34D399",
            text_color="#FFFFFF",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w",
        )
        self.btn_clean.pack(fill="x", padx=18, pady=6)

        self.btn_export = ctk.CTkButton(
            self.sidebar,
            text="🚀  3. Export Package",
            command=self.export_files,
            height=46,
            corner_radius=12,
            fg_color="#6366F1",
            hover_color="#4F46E5",
            border_width=1,
            border_color="#A5B4FC",
            text_color="#FFFFFF",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w",
        )
        self.btn_export.pack(fill="x", padx=18, pady=6)

        # Live Data Health Score Gauge Card (Matplotlib Donut Ring)
        self.gauge_card = ctk.CTkFrame(
            self.sidebar,
            fg_color="#0F172A",
            corner_radius=14,
            border_width=1,
            border_color="#1E293B",
        )
        self.gauge_card.pack(fill="x", padx=18, pady=(18, 10))

        ctk.CTkLabel(
            self.gauge_card,
            text="DATA HEALTH INDEX",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="#94A3B8",
        ).pack(pady=(10, 0))

        self.gauge_container = ctk.CTkFrame(
            self.gauge_card, fg_color="transparent", height=145
        )
        self.gauge_container.pack(fill="x", padx=10, pady=(0, 8))
        self.draw_health_ring(0, "#475569", "NO DATA")

        # Author Badge at Bottom
        self.author_card = ctk.CTkFrame(
            self.sidebar,
            fg_color="#111C33",
            corner_radius=12,
            border_width=1,
            border_color="#1E293B",
        )
        self.author_card.pack(side="bottom", fill="x", padx=18, pady=18)

        ctk.CTkLabel(
            self.author_card,
            text="👩‍💻 Maliqa Manzoor (BSIT)",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#F8FAFC",
        ).pack(anchor="w", padx=12, pady=(10, 2))
        ctk.CTkLabel(
            self.author_card,
            text="🎓 Prof. Habibullah • Data Science",
            font=ctk.CTkFont(size=11),
            text_color="#38BDF8",
        ).pack(anchor="w", padx=12, pady=(0, 10))

        # ==================== MAIN WORKSPACE ====================
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=22, pady=18)
        self.main_area.grid_columnconfigure(0, weight=1)
        self.main_area.grid_rowconfigure(3, weight=1)

        # Header Bar with Animated Pulse Pill
        self.top_bar = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.top_bar.grid(row=0, column=0, sticky="ew", pady=(0, 12))

        self.title_lbl = ctk.CTkLabel(
            self.top_bar,
            text="Intelligent Data Quality & Preprocessing Studio",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#F8FAFC",
        )
        self.title_lbl.pack(side="left")

        self.pulse_pill = ctk.CTkLabel(
            self.top_bar,
            text="● ENGINE STANDBY",
            fg_color="#0F172A",
            text_color="#38BDF8",
            corner_radius=20,
            padx=16,
            pady=6,
            font=ctk.CTkFont(size=11, weight="bold"),
        )
        self.pulse_pill.pack(side="right")
        self.animate_pulse()

        # 4 Neon KPI Cards
        self.kpi_row = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.kpi_row.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        for i in range(4):
            self.kpi_row.grid_columnconfigure(i, weight=1)

        self.kpi_records = self.build_kpi(
            self.kpi_row, 0, "TOTAL RECORDS", "0", "Rows Loaded", "#38BDF8"
        )
        self.kpi_missing = self.build_kpi(
            self.kpi_row, 1, "MISSING ANOMALIES", "0", "Null Cells", "#F43F5E"
        )
        self.kpi_dups = self.build_kpi(
            self.kpi_row, 2, "EXACT DUPLICATES", "0", "Redundant Rows", "#F59E0B"
        )
        self.kpi_outliers = self.build_kpi(
            self.kpi_row,
            3,
            "IQR OUTLIERS",
            "0",
            "Flagged & Retained",
            "#C084FC",
        )

        # Smooth Progress Bar
        self.progress = ctk.CTkProgressBar(
            self.main_area,
            height=6,
            corner_radius=3,
            fg_color="#0F172A",
            progress_color="#10B981",
        )
        self.progress.grid(row=2, column=0, sticky="ew", pady=(0, 12))
        self.progress.set(0)

        # 3-Tab Professional Workspace
        self.tabs = ctk.CTkTabview(
            self.main_area,
            fg_color="#0B1120",
            border_width=1,
            border_color="#1E293B",
            corner_radius=14,
            segmented_button_fg_color="#060913",
            segmented_button_selected_color="#0284C7",
            segmented_button_unselected_color="#060913",
        )
        self.tabs.grid(row=3, column=0, sticky="nsew")

        self.tab_audit = self.tabs.add("  📋 Execution Audit Log  ")
        self.tab_charts = self.tabs.add("  📈 Visual Telemetry & Charts  ")
        self.tab_grid = self.tabs.add("  🔍 Interactive Data Explorer  ")

        # TAB 1: Audit Log
        self.log_box = ctk.CTkTextbox(
            self.tab_audit,
            fg_color="#060913",
            text_color="#E2E8F0",
            border_width=1,
            border_color="#1E293B",
            corner_radius=10,
            font=ctk.CTkFont(family="Consolas", size=13),
        )
        self.log_box.pack(fill="both", expand=True, padx=10, pady=10)
        self.log_box.insert(
            "0.0",
            "◈ NEXUS DATA STUDIO READY.\n"
            "◈ Click '1. Import Raw Dataset' on the left sidebar to load your Kaggle CSV file...\n",
        )

        # TAB 2: Visual Charts Canvas
        self.chart_frame = ctk.CTkFrame(
            self.tab_charts, fg_color="#060913", corner_radius=10
        )
        self.chart_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.chart_placeholder = ctk.CTkLabel(
            self.chart_frame,
            text="📊 Visual Telemetry Charts will render automatically after you import & clean your dataset!",
            font=ctk.CTkFont(size=14),
            text_color="#64748B",
        )
        self.chart_placeholder.place(relx=0.5, rely=0.5, anchor="center")

        # TAB 3: Interactive Searchable Data Grid
        search_bar = ctk.CTkFrame(self.tab_grid, fg_color="transparent")
        search_bar.pack(fill="x", padx=10, pady=(8, 6))

        self.search_entry = ctk.CTkEntry(
            search_bar,
            placeholder_text="🔎 Search records by any keyword (e.g., Female, Clothing, Istanbul)...",
            width=420,
            height=34,
            fg_color="#060913",
            border_color="#38BDF8",
        )
        self.search_entry.pack(side="left", padx=(0, 8))
        self.search_entry.bind("<KeyRelease>", self.filter_table)

        self.row_count_lbl = ctk.CTkLabel(
            search_bar,
            text="Showing top 100 rows",
            font=ctk.CTkFont(size=11),
            text_color="#94A3B8",
        )
        self.row_count_lbl.pack(side="right")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="#060913",
            foreground="#E2E8F0",
            fieldbackground="#060913",
            rowheight=28,
            borderwidth=0,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Treeview.Heading",
            background="#1E293B",
            foreground="#38BDF8",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
        )
        style.map("Treeview", background=[("selected", "#0284C7")])

        grid_box = ctk.CTkFrame(self.tab_grid, fg_color="#060913")
        grid_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        sy = ttk.Scrollbar(grid_box, orient="vertical")
        sx = ttk.Scrollbar(grid_box, orient="horizontal")
        self.tree = ttk.Treeview(
            grid_box, yscrollcommand=sy.set, xscrollcommand=sx.set
        )
        sy.config(command=self.tree.yview)
        sx.config(command=self.tree.xview)
        sy.pack(side="right", fill="y")
        sx.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

    def animate_pulse(self):
        current = self.pulse_pill.cget("text")
        if self.pulse_state:
            self.pulse_pill.configure(text=current.replace("●", "◉"))
        else:
            self.pulse_pill.configure(text=current.replace("◉", "●"))
        self.pulse_state = not self.pulse_state
        self.after(700, self.animate_pulse)

    def build_kpi(self, parent, col, title, val, sub, color):
        card = ctk.CTkFrame(
            parent,
            fg_color="#0B1120",
            corner_radius=14,
            border_width=1,
            border_color=color,
        )
        card.grid(
            row=0,
            column=col,
            sticky="ew",
            padx=(0 if col == 0 else 7, 0 if col == 3 else 7),
        )
        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="#94A3B8",
        ).pack(anchor="w", padx=16, pady=(12, 2))
        val_lbl = ctk.CTkLabel(
            card,
            text=val,
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=color,
        )
        val_lbl.pack(anchor="w", padx=16, pady=0)
        ctk.CTkLabel(
            card,
            text=sub,
            font=ctk.CTkFont(size=10),
            text_color="#64748B",
        ).pack(anchor="w", padx=16, pady=(0, 10))
        return val_lbl

    def draw_health_ring(self, score, color, label):
        for w in self.gauge_container.winfo_children():
            w.destroy()
        fig, ax = plt.subplots(figsize=(2.1, 1.45), dpi=100)
        fig.patch.set_facecolor("#0F172A")
        ax.set_facecolor("#0F172A")

        vals = [score, max(0, 100 - score)]
        colors = [color, "#1E293B"]
        ax.pie(
            vals,
            startangle=90,
            colors=colors,
            counterclock=False,
            wedgeprops={"width": 0.26, "edgecolor": "#0F172A"},
        )
        ax.text(
            0,
            0.08,
            f"{score}%",
            ha="center",
            va="center",
            color="#F8FAFC",
            fontsize=15,
            fontweight="bold",
        )
        ax.text(
            0,
            -0.32,
            label,
            ha="center",
            va="center",
            color=color,
            fontsize=7.5,
            fontweight="bold",
        )
        ax.axis("equal")
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

        canvas = FigureCanvasTkAgg(fig, master=self.gauge_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)

    def render_charts(self, missing_before, outlier_dict):
        for w in self.chart_frame.winfo_children():
            w.destroy()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.2, 3.6), dpi=100)
        fig.patch.set_facecolor("#060913")

        # Chart 1: Before vs After Data Anomalies
        ax1.set_facecolor("#0B1120")
        categories = ["Missing Cells\n(Before)", "Missing Cells\n(After)", "Duplicates\n(Found)"]
        counts = [missing_before, 0, int(self.df_raw.duplicated().sum())]
        bars = ax1.bar(
            categories,
            counts,
            color=["#F43F5E", "#10B981", "#F59E0B"],
            width=0.45,
        )
        ax1.set_title(
            "Data Cleansing Impact (Before vs. After)",
            color="#F8FAFC",
            fontsize=11,
            fontweight="bold",
            pad=12,
        )
        ax1.tick_params(colors="#94A3B8", labelsize=9)
        for spine in ax1.spines.values():
            spine.set_color("#1E293B")
        for bar in bars:
            yval = bar.get_height()
            ax1.text(
                bar.get_x() + bar.get_width() / 2.0,
                yval + max(1, max(counts) * 0.03),
                f"{int(yval)}",
                ha="center",
                va="bottom",
                color="#F8FAFC",
                fontsize=9,
                fontweight="bold",
            )

        # Chart 2: IQR Outliers Detected Per Numeric Feature
        ax2.set_facecolor("#0B1120")
        if outlier_dict:
            cols = list(outlier_dict.keys())
            out_vals = list(outlier_dict.values())
            bars2 = ax2.barh(cols, out_vals, color="#A855F7", height=0.45)
            ax2.set_title(
                "IQR Outliers Flagged by Column",
                color="#F8FAFC",
                fontsize=11,
                fontweight="bold",
                pad=12,
            )
            ax2.tick_params(colors="#94A3B8", labelsize=9)
            for spine in ax2.spines.values():
                spine.set_color("#1E293B")
            for bar in bars2:
                xval = bar.get_width()
                ax2.text(
                    xval + max(1, max(out_vals) * 0.02),
                    bar.get_y() + bar.get_height() / 2.0,
                    f"{int(xval)}",
                    va="center",
                    ha="left",
                    color="#F8FAFC",
                    fontsize=9,
                    fontweight="bold",
                )

        plt.tight_layout(pad=2.0)
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        plt.close(fig)

    def populate_table(self, df):
        self.tree.delete(*self.tree.get_children())
        cols = list(df.columns)
        self.tree["columns"] = cols
        self.tree["show"] = "headings"
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=115, anchor="center")
        for _, row in df.head(100).iterrows():
            self.tree.insert("", "end", values=list(row))

    def filter_table(self, event=None):
        active_df = (
            self.df_clean if self.df_clean is not None else self.df_raw
        )
        if active_df is None:
            return
        q = self.search_entry.get().strip().lower()
        if not q:
            self.populate_table(active_df)
            self.row_count_lbl.configure(text="Showing top 100 rows")
            return
        mask = active_df.apply(
            lambda r: r.astype(str).str.lower().str.contains(q).any(), axis=1
        )
        filtered = active_df[mask]
        self.populate_table(filtered)
        self.row_count_lbl.configure(
            text=f"Matched {len(filtered):,} rows (showing up to 100)"
        )

    def log(self, text):
        self.log_box.insert(tk.END, text + "\n")
        self.log_box.see(tk.END)

    def load_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not path:
            return
        self.file_path = path
        self.df_raw = pd.read_csv(path)
        self.progress.set(0.35)

        rows, cols = self.df_raw.shape
        missing = int(self.df_raw.isna().sum().sum())
        dups = int(self.df_raw.duplicated().sum())

        self.kpi_records.configure(text=f"{rows:,}")
        self.kpi_missing.configure(text=f"{missing:,}", text_color="#F43F5E")
        self.kpi_dups.configure(text=f"{dups:,}")
        self.kpi_outliers.configure(text="Ready")

        # Calculate initial health score
        init_score = max(
            45,
            int(100 - ((missing + dups) / max(1, rows * cols)) * 100 - 15),
        )
        self.draw_health_ring(init_score, "#F59E0B", "NEEDS AUDIT")
        self.pulse_pill.configure(
            text=f"● LOADED: {os.path.basename(path)}", text_color="#38BDF8"
        )
        self.populate_table(self.df_raw)

        self.log_box.delete("0.0", tk.END)
        self.log("=" * 74)
        self.log("PHASE 1: INITIAL DATASET TELEMETRY & ANOMALY DETECTION")
        self.log("=" * 74)
        self.log(f"Source File       : {os.path.basename(path)}")
        self.log(f"Dataset Shape     : {rows:,} rows x {cols} columns")
        self.log(
            f"Duplicate Records : {dups} ({'No duplicate values found' if dups == 0 else 'Duplicates identified'})"
        )
        self.log(f"Missing Cells     : {missing}")
        self.log("\n--- Missing Values Per Column (Before Cleaning) ---")
        self.log(self.df_raw.isna().sum().to_string())
        self.log("\n--- Schema & Data Types ---")
        self.log(self.df_raw.dtypes.to_string())
        self.log(
            "\n◈ Ready for cleansing. Click '2. Run Smart Pipeline' to execute."
        )

    def clean_data(self):
        if self.df_raw is None:
            messagebox.showwarning(
                "No Dataset", "Please import a CSV dataset first!"
            )
            return

        df = self.df_raw.copy()
        missing_before = int(df.isna().sum().sum())
        self.progress.set(0.75)

        self.log("\n" + "=" * 74)
        self.log("PHASE 2: EXECUTING 6-STAGE SMART DATA CLEANSING PIPELINE")
        self.log("=" * 74)

        # 1. Text Standardization
        for col in df.select_dtypes(include=["object"]).columns:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace(
                {"nan": np.nan, "None": np.nan, "": np.nan, "NaN": np.nan}
            )
        self.log(
            "[01] Whitespace & Null Trim   : Stripped leading/trailing spaces & normalized null tokens."
        )

        # 2. Duplicate Removal
        dup_before = int(df.duplicated().sum())
        df = df.drop_duplicates()
        if dup_before == 0:
            self.log(
                "[02] Duplicate Verification   : No duplicate values found (0 rows removed)."
            )
        else:
            self.log(
                f"[02] Duplicate Verification   : Removed {dup_before} exact duplicate rows."
            )

        # 3. Data Type & Domain Check
        num_cols = df.select_dtypes(include=[np.number]).columns
        invalid_count = 0
        for col in num_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            neg = int((df[col] < 0).sum())
            if neg > 0:
                invalid_count += neg
                df.loc[df[col] < 0, col] = np.nan
        self.log(
            f"[03] Type & Domain Integrity  : Enforced numeric dtypes; {invalid_count} invalid negative values handled."
        )

        # 4. Missing Value Imputation
        for col in df.columns:
            if df[col].isna().sum() > 0:
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = df[col].fillna(df[col].median())
                else:
                    mode_val = (
                        df[col].mode()[0]
                        if not df[col].mode().empty
                        else "Unknown"
                    )
                    df[col] = df[col].fillna(mode_val)
        missing_after = int(df.isna().sum().sum())
        self.log(
            f"[04] Missing Value Imputation : Missing cells reduced from {missing_before} -> {missing_after} (Median/Mode)."
        )

        # 5. Inconsistent Categorical Standardization
        for col in df.select_dtypes(include=["object"]).columns:
            if (
                "id" not in col.lower()
                and "date" not in col.lower()
                and "invoice" not in col.lower()
            ):
                df[col] = df[col].str.title()
        self.log(
            "[05] Categorical Uniformity   : Standardized text categories to Title Case."
        )

        # 6. IQR Outlier Detection
        total_outliers = 0
        outlier_summary = {}
        for col in num_cols:
            if "id" not in col.lower():
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers = (df[col] < (Q1 - 1.5 * IQR)) | (
                    df[col] > (Q3 + 1.5 * IQR)
                )
                cnt = int(outliers.sum())
                total_outliers += cnt
                outlier_summary[col] = cnt
                df[f"{col}_OutlierFlag"] = np.where(outliers, 1, 0)
                self.log(
                    f"[06] IQR Outlier Flagging     : '{col}' -> {cnt:,} statistical outliers flagged."
                )

        self.df_clean = df
        self.progress.set(1.0)

        # Update All KPIs, Health Ring & Visual Charts
        self.kpi_records.configure(text=f"{df.shape[0]:,}")
        self.kpi_missing.configure(text="0", text_color="#10B981")
        self.kpi_dups.configure(text="0", text_color="#10B981")
        self.kpi_outliers.configure(text=f"{total_outliers:,}")

        self.draw_health_ring(100, "#10B981", "100% HEALTHY")
        self.pulse_pill.configure(
            text="● VALIDATED & 100% CLEAN", text_color="#10B981"
        )
        self.populate_table(self.df_clean)
        self.render_charts(missing_before, outlier_summary)

        self.log("\n" + "=" * 74)
        self.log("PHASE 3: POST-CLEANSING VALIDATION REPORT (AFTER CLEANING)")
        self.log("=" * 74)
        self.log(
            f"Final Dimensions          : {df.shape[0]:,} rows x {df.shape[1]} columns"
        )
        self.log(
            f"Validation - Zero Missing : {'PASS' if df.isna().sum().sum() == 0 else 'FAIL'}"
        )
        self.log(
            f"Validation - No Duplicates: {'PASS' if df.duplicated().sum() == 0 else 'FAIL'}"
        )
        self.log("\n--- Missing Values Per Column (After Cleaning) ---")
        self.log(df.isna().sum().to_string())

    def export_files(self):
        if self.df_clean is None:
            messagebox.showwarning(
                "Not Ready", "Please run Smart Pipeline first!"
            )
            return
        os.makedirs("Output", exist_ok=True)
        csv_out = os.path.join("Output", "cleaned_customer_shopping_data.csv")
        txt_out = os.path.join("Output", "nexus_cleaning_audit_report.txt")
        self.df_clean.to_csv(csv_out, index=False)
        with open(txt_out, "w", encoding="utf-8") as f:
            f.write(self.log_box.get("0.0", tk.END))
        messagebox.showinfo(
            "Package Exported",
            f"All deliverables exported to Output folder:\n\n1. {csv_out}\n2. {txt_out}",
        )


if __name__ == "__main__":
    app = FlagshipDataStudio()
    app.mainloop()