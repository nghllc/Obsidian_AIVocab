import sys
import os
import json
import requests
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton, QFileDialog,
    QComboBox, QProgressBar, QMessageBox, QListWidget, QListWidgetItem,
    QSplitter, QFrame, QRadioButton, QButtonGroup, QStackedWidget
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QIcon, QFont, QPalette, QColor

# ==================== HELPER FUNCTION FOR ICON RESOURCE ====================
# This function ensures the icon can be found whether running from source or as a bundled app
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# ==================== DEFAULT SETTINGS INTEGRATED IN CODE ====================
DEFAULT_SETTINGS = {
    "api_key": "",
    "model": "gemini",
    "prompt": "Bạn là chuyên gia ngôn ngữ học với kinh nghiệm xây dựng hệ thống từ vựng và phương pháp ghi nhớ hiệu quả. Hãy tạo thẻ từ vựng chi tiết, trực quan và đầy đủ thông tin cho quá trình học tiếng Anh.\n\nNếu động từ không ở dạng nguyên gốc hãy đưa về dạng nguyên gốc.\n\nHãy tạo một thẻ từ vựng chi tiết cho từ vựng được cung cấp theo tiêu chuẩn học thuật và ngôn ngữ học, với đầy đủ thông tin từ phát âm, định nghĩa đến ngữ cảnh sử dụng và mối liên hệ với các từ khác.\n\n---\nword: [từ vựng]\npronunciation: '/phiên_âm_quốc_tế/'\npos:\n  - [noun/adverb/...]\nlevel:\n  - [A1/A2/B1/B2/C1/C2]\ntopics:\n  - [business/technology/academic/...]\n  - [topic2]\n  - [topic3]\nsynonyms:\n  - [word1]\n  - [word2]\n  - [word3]\nantonyms:\n  - [word1]\n  - [word2]\ncreated: [yyyy-mm-dd]\ncompleted: [true/false]\naliases:\n  - [infinitive form]\n  - [past tense form]\n  - [present/past participle forms]\n  - [noun form]\n  - [adjective form]\n  - [etc]\n---\n# {{từ vựng}}\n## Định nghĩa\n> [!info] 📚 Định nghĩa\n> - Nghĩa tiếng Việt: [Cung cấp định nghĩa rõ ràng, đầy đủ bằng tiếng Việt]\n> - Nghĩa tiếng Anh: [Cung cấp định nghĩa rõ ràng, đầy đủ bằng tiếng Anh]\n\n## Phát âm\n> [!note] 🔊 Lưu ý phát âm\n> Các điểm cần lưu ý khi phát âm từ này, bao gồm: trọng âm, cách phát âm các âm khó, sự khác biệt giữa phát âm của từ này trong các biến thể tiếng Anh (Anh, Mỹ, Úc...) nếu có.\n>Audio: ![[{từ vựng}.mp3]] \n\n## Ví dụ\n> [!example] 📝 Ví dụ\n> 1. [Câu ví dụ 1 - một câu hoàn chỉnh sử dụng từ vựng trong ngữ cảnh tự nhiên]\n> 2. [Câu ví dụ 2 - một câu hoàn chỉnh sử dụng từ vựng trong ngữ cảnh khác]\n> 3. [Câu ví dụ 3 - nếu từ có nhiều cách sử dụng khác nhau]\n\n## Collocations (Cụm từ thông dụng)\n> [!tip] 🔄 Cụm từ thông dụng\n> - [Cụm từ 1] - [giải thích ngắn gọn nếu cần]\n> - [Cụm từ 2] - [giải thích ngắn gọn nếu cần]\n> - [Cụm từ 3] - [giải thích ngắn gọn nếu cần]\n\n## Phrases & Idioms (Thành ngữ, tục ngữ)\n> [!quote] 💬 Thành ngữ, tục ngữ\n> - [[Thành ngữ/tục ngữ 1]]: [Giải thích ý nghĩa chi tiết và cách sử dụng]\n> - [[Thành ngữ/tục ngữ 2]]: [Giải thích ý nghĩa chi tiết và cách sử dụng]\n\n## Ngữ cảnh sử dụng\n> [!abstract] 🌐 Ngữ cảnh sử dụng\n> - 🏛️ Ngữ cảnh trang trọng: [Cách sử dụng từ này trong ngữ cảnh trang trọng, học thuật hoặc công việc]\n> - 🏙️ Ngữ cảnh thông thường: [Cách sử dụng từ này trong giao tiếp hàng ngày]\n> - 🏠 Ngữ cảnh không trang trọng: [Cách sử dụng từ này trong giao tiếp thân mật, không trang trọng]\n\n## Từ đồng âm (nếu có)\n> [!warning] 🔄 Từ đồng âm\n> - [[từ đồng âm 1]]: [giải thích sự khác biệt về ý nghĩa và cách sử dụng]\n> - [[từ đồng âm 2]]: [giải thích sự khác biệt về ý nghĩa và cách sử dụng]\n\n## Từ liên quan\n> [!link] 🔗 Từ liên quan\n> - [[từ liên quan 1]]: [mối liên hệ với từ gốc]\n> - [[từ liên quan 2]]: [mối liên hệ với từ gốc]\n\n## Gốc từ / Từ nguyên\n> [!cite] 📜 Gốc từ / Từ nguyên\n> [Gốc từ, nguồn gốc và lịch sử của từ, bao gồm ngôn ngữ gốc, thay đổi nghĩa theo thời gian nếu có]\n\n## Ghi chú cá nhân\n> [!question] 💡 Ghi chú cá nhân\n> - [Các ghi chú, mẹo nhớ từ cá nhân, liên kết đến kiến thức hoặc trải nghiệm cá nhân để nhớ từ dễ hơn]\n> - [Các mẹo ghi nhớ nghĩa, cách dùng hoặc phát âm]\n\n## Ảnh minh họa\n> [!image] 🖼️ Ảnh minh họa\n> ![[ảnh minh họa từ vựng.jpg]]\n\n## Các dạng liên quan (Aliases)\n### {{alias 1}}\n> [!important] 🔄 [[alias 1]]\n> - **Loại từ**: [noun/verb/adjective/...]\n> - **Định nghĩa ngắn gọn**: [Đưa ra định nghĩa ngắn gọn hoặc mô tả mối quan hệ với từ gốc]\n> - **Ví dụ**: [Câu ví dụ sử dụng alias này trong ngữ cảnh tự nhiên]\n> - **Lưu ý sử dụng**: [Các lưu ý đặc biệt về cách sử dụng, nếu có]\n\n## Nội dung cho Anki\n```\nSTART\nEN-Words\nVocabulary: {từ vựng}\nPronunciation: {phát âm quốc tế}\nDefinition: {định nghĩa tiếng Việt ngắn gọn}\nAudio: ![[{từ vựng}.mp3]]\nExample: {câu ví dụ đầu tiên}\nExample Translation: {bản dịch của câu ví dụ}\nImage: {mô tả hoặc liên kết đến hình ảnh}\nNotes: {ghi chú quan trọng về cách sử dụng}\nPart of Speech: {loại từ}\nSynonyms: {từ đồng nghĩa, phân cách bằng dấu phẩy}\nAntonyms: {từ trái nghĩa, phân cách bằng dấu phẩy}\nTags: {cấp độ, chủ đề, loại từ, lĩnh vực sử dụng, trạng thái học tập (new/review/mastered)}\nLinks: {liên kết đến các từ liên quan}\nID: {cấp độ}_{ngày tạo yyyymmdd}_{hash 4 số của từ vựng}\nEND\n```",
    "input_folder": "",
    "output_folder": "",
    "single_word": ""
}

class AIProcessorThread(QThread):
    progress = Signal(int)
    status = Signal(str)
    finished = Signal()
    error = Signal(str)

    def __init__(self, items, mode, prompt, api_key, model, output_folder, parent=None):
        super().__init__(parent)
        self.items = items
        self.mode = mode
        self.prompt = prompt
        self.api_key = api_key
        self.model = model
        self.output_folder = output_folder
        self.is_paused = False
        self.should_stop = False

    def run(self):
        try:
            total_items = len(self.items)
            for i, item in enumerate(self.items):
                if self.should_stop:
                    break
                while self.is_paused:
                    self.msleep(100)
                    if self.should_stop:
                        break

                self.status.emit(f"Processing ({i+1}/{total_items}): {os.path.basename(item)}")
                
                content_to_process = ""
                output_filename = ""

                if self.mode == 'markdown':
                    with open(item, 'r', encoding='utf-8') as f:
                        content_to_process = f"[{os.path.basename(item)}]\n\n{f.read()}"
                    output_path = item # Overwrite original file
                else: # TXT file or Single Word mode
                    word = item
                    content_to_process = f"Từ vựng: {word}"
                    safe_word = "".join(c for c in word if c.isalnum() or c in (' ', '-', '_')).strip()
                    output_filename = f"{safe_word}.md"
                    output_path = os.path.join(self.output_folder, output_filename)
                    count = 1
                    base, ext = os.path.splitext(output_path)
                    while os.path.exists(output_path):
                        output_path = f"{base}_{count}{ext}"
                        count += 1
                
                full_prompt = f"{self.prompt}\n\n{content_to_process}"
                processed_content = self.process_with_ai(full_prompt)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(processed_content)
                
                self.progress.emit(int((i + 1) / total_items * 100))

            if self.should_stop:
                self.status.emit("Processing stopped by user.")
            else:
                self.status.emit("Processing complete!")
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))
    
    def process_with_ai(self, content):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={self.api_key}"
        headers = {'Content-Type': 'application/json'}
        data = {"contents": [{"parts": [{"text": content}]}]}
        try:
            response = requests.post(url, headers=headers, json=data, timeout=120)
            response.raise_for_status()
            result = response.json()
            return result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
        except requests.exceptions.RequestException as e:
            raise Exception(f"API Request Error: {e}")

    def pause(self):
        self.is_paused = True

    def resume(self):
        self.is_paused = False

    def stop(self):
        self.should_stop = True

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AIVocab")
        self.setMinimumSize(800, 600)
        self.setWindowIcon(QIcon(resource_path("app_icon.ico")))
        self.settings_file = 'settings.json'
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # --- Warning Note ---
        warning_label = QLabel("Note: The free API tier is limited to about 60 words per minute.")
        warning_label.setAlignment(Qt.AlignCenter)
        palette = warning_label.palette()
        palette.setColor(QPalette.WindowText, QColor("orange"))
        warning_label.setPalette(palette)
        main_layout.addWidget(warning_label)
        
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # --- Processing Mode ---
        mode_group_box = QFrame()
        mode_group_box.setFrameShape(QFrame.StyledPanel)
        mode_layout = QVBoxLayout(mode_group_box)
        mode_layout.addWidget(QLabel("Processing Mode:"))
        self.mode_group = QButtonGroup(self)
        
        self.md_radio = QRadioButton("Process Markdown File(s)")
        self.txt_radio = QRadioButton("Process TXT Word List")
        self.single_word_radio = QRadioButton("Process Single Word")
        
        self.mode_group.addButton(self.md_radio, 0)
        self.mode_group.addButton(self.txt_radio, 1)
        self.mode_group.addButton(self.single_word_radio, 2)
        
        mode_layout.addWidget(self.md_radio)
        mode_layout.addWidget(self.txt_radio)
        mode_layout.addWidget(self.single_word_radio)
        self.md_radio.setChecked(True)
        self.mode_group.idClicked.connect(self.on_mode_changed)
        left_layout.addWidget(mode_group_box)

        # --- Input Widgets ---
        self.input_stack = QStackedWidget()
        self.setup_input_widgets()
        left_layout.addWidget(self.input_stack)

        # --- Output Folder (for TXT and Single Word modes) ---
        self.output_folder_widget = QWidget()
        output_layout = QHBoxLayout(self.output_folder_widget)
        output_layout.setContentsMargins(0, 0, 0, 0)
        output_layout.addWidget(QLabel("Output Folder:"))
        self.output_path_input = QLineEdit()
        self.output_path_input.setReadOnly(True)
        browse_output_btn = QPushButton("Browse...")
        browse_output_btn.clicked.connect(self.select_output_folder)
        output_layout.addWidget(self.output_path_input)
        output_layout.addWidget(browse_output_btn)
        left_layout.addWidget(self.output_folder_widget)

        # --- API Config ---
        api_group = QFrame()
        api_group.setFrameShape(QFrame.StyledPanel)
        api_layout = QVBoxLayout(api_group)
        api_key_layout = QHBoxLayout()
        api_key_layout.addWidget(QLabel("API Key:"))
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.Password)
        api_key_layout.addWidget(self.api_key_input)
        api_layout.addLayout(api_key_layout)
        left_layout.addWidget(api_group)
        
        # --- Prompt ---
        prompt_group = QFrame()
        prompt_group.setFrameShape(QFrame.StyledPanel)
        prompt_layout = QVBoxLayout(prompt_group)
        prompt_layout.addWidget(QLabel("Prompt:"))
        self.prompt_edit = QTextEdit()
        self.prompt_edit.setMinimumHeight(100)
        prompt_layout.addWidget(self.prompt_edit)
        left_layout.addWidget(prompt_group)
        
        left_layout.addStretch()

        # --- Controls & Progress ---
        self.progress_bar = QProgressBar()
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        
        controls_layout = QHBoxLayout()
        self.pause_button = QPushButton("Pause")
        self.stop_button = QPushButton("Stop")
        self.process_button = QPushButton("Process")

        self.pause_button.setEnabled(False)
        self.stop_button.setEnabled(False)

        self.pause_button.clicked.connect(self.toggle_pause)
        self.stop_button.clicked.connect(self.stop_processing)
        self.process_button.clicked.connect(self.process_files)

        controls_layout.addWidget(self.pause_button)
        controls_layout.addWidget(self.stop_button)

        left_layout.addWidget(self.progress_bar)
        left_layout.addWidget(self.status_label)
        left_layout.addLayout(controls_layout)
        left_layout.addWidget(self.process_button)
        
        # --- Right Panel (File List) ---
        self.right_panel = QWidget()
        right_layout = QVBoxLayout(self.right_panel)
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search files...")
        self.search_input.textChanged.connect(self.filter_files)
        search_layout.addWidget(self.search_input)
        
        self.select_all_button = QPushButton("Select All")
        self.select_all_button.clicked.connect(self.toggle_select_all)
        search_layout.addWidget(self.select_all_button)
        right_layout.addLayout(search_layout)
        
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.MultiSelection)
        right_layout.addWidget(self.file_list)
        
        splitter.addWidget(left_panel)
        splitter.addWidget(self.right_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
        
        self.load_settings()
        self.on_mode_changed(self.mode_group.checkedId())

    def setup_input_widgets(self):
        # Markdown Mode Widget
        md_widget = QWidget()
        md_layout = QHBoxLayout(md_widget)
        md_layout.setContentsMargins(0, 0, 0, 0)
        md_layout.addWidget(QLabel("Source Folder:"))
        self.md_path_input = QLineEdit()
        self.md_path_input.setReadOnly(True)
        browse_md_btn = QPushButton("Browse...")
        browse_md_btn.clicked.connect(self.select_md_folder)
        md_layout.addWidget(self.md_path_input)
        md_layout.addWidget(browse_md_btn)
        self.input_stack.addWidget(md_widget)

        # TXT File Mode Widget
        txt_widget = QWidget()
        txt_layout = QHBoxLayout(txt_widget)
        txt_layout.setContentsMargins(0, 0, 0, 0)
        txt_layout.addWidget(QLabel("Source TXT File:"))
        self.txt_path_input = QLineEdit()
        self.txt_path_input.setReadOnly(True)
        browse_txt_btn = QPushButton("Browse...")
        browse_txt_btn.clicked.connect(self.select_txt_file)
        txt_layout.addWidget(self.txt_path_input)
        txt_layout.addWidget(browse_txt_btn)
        self.input_stack.addWidget(txt_widget)

        # Single Word Mode Widget
        word_widget = QWidget()
        word_layout = QHBoxLayout(word_widget)
        word_layout.setContentsMargins(0, 0, 0, 0)
        word_layout.addWidget(QLabel("Single Word:"))
        self.word_input = QLineEdit()
        self.word_input.setPlaceholderText("Enter a word to process...")
        word_layout.addWidget(self.word_input)
        self.input_stack.addWidget(word_widget)

    def on_mode_changed(self, mode_id):
        self.input_stack.setCurrentIndex(mode_id)
        if mode_id == 0: # Markdown
            self.output_folder_widget.setVisible(False)
            self.right_panel.setVisible(True)
        elif mode_id == 1: # TXT File
            self.output_folder_widget.setVisible(True)
            self.right_panel.setVisible(False)
        elif mode_id == 2: # Single Word
            self.output_folder_widget.setVisible(True)
            self.right_panel.setVisible(False)

    def select_md_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Source Folder", self.md_path_input.text())
        if folder:
            self.md_path_input.setText(folder)
            self.load_files_from_folder(folder)

    def select_txt_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select TXT Word List", "", "Text Files (*.txt)")
        if file_path:
            self.txt_path_input.setText(file_path)

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder", self.output_path_input.text())
        if folder:
            self.output_path_input.setText(folder)
    
    def load_files_from_folder(self, folder):
        self.file_list.clear()
        if folder and os.path.isdir(folder):
            try:
                for file in os.listdir(folder):
                    if file.lower().endswith('.md'):
                        self.file_list.addItem(file)
            except Exception as e:
                self.status_label.setText(f"Error reading folder: {e}")

    def process_files(self):
        if not self.api_key_input.text():
            QMessageBox.warning(self, "Input Error", "Please enter your API key.")
            return

        mode_id = self.mode_group.checkedId()
        items_to_process = []
        mode_str = ""
        output_folder = self.output_path_input.text()

        if mode_id == 0: # Markdown
            selected_items = self.file_list.selectedItems()
            if not selected_items:
                QMessageBox.warning(self, "Input Error", "Please select at least one Markdown file.")
                return
            items_to_process = [os.path.join(self.md_path_input.text(), item.text()) for item in selected_items]
            mode_str = "markdown"

        elif mode_id == 1: # TXT
            txt_file = self.txt_path_input.text()
            if not txt_file or not os.path.exists(txt_file):
                QMessageBox.warning(self, "Input Error", "Please select a valid TXT file.")
                return
            if not output_folder:
                QMessageBox.warning(self, "Input Error", "Please select an output folder.")
                return
            with open(txt_file, 'r', encoding='utf-8') as f:
                items_to_process = [line.strip() for line in f if line.strip()]
            mode_str = "txt"

        elif mode_id == 2: # Single Word
            word = self.word_input.text().strip()
            if not word:
                QMessageBox.warning(self, "Input Error", "Please enter a word.")
                return
            if not output_folder:
                QMessageBox.warning(self, "Input Error", "Please select an output folder.")
                return
            items_to_process = [word]
            mode_str = "single_word"
        
        if not items_to_process:
            QMessageBox.information(self, "Information", "Nothing to process.")
            return

        self.set_controls_enabled(False)

        self.processor = AIProcessorThread(
            items_to_process, mode_str, self.prompt_edit.toPlainText(),
            self.api_key_input.text(), "gemini", output_folder
        )
        self.processor.progress.connect(self.progress_bar.setValue)
        self.processor.status.connect(self.status_label.setText)
        self.processor.finished.connect(self.processing_finished)
        self.processor.error.connect(self.processing_error)
        self.processor.start()

    def set_controls_enabled(self, is_enabled):
        self.process_button.setEnabled(is_enabled)
        self.pause_button.setEnabled(not is_enabled)
        self.stop_button.setEnabled(not is_enabled)
        # Disable mode switching during processing
        self.md_radio.setEnabled(is_enabled)
        self.txt_radio.setEnabled(is_enabled)
        self.single_word_radio.setEnabled(is_enabled)

    def toggle_pause(self):
        if hasattr(self, 'processor') and self.processor.isRunning():
            if self.processor.is_paused:
                self.processor.resume()
                self.pause_button.setText("Pause")
            else:
                self.processor.pause()
                self.pause_button.setText("Resume")

    def stop_processing(self):
        if hasattr(self, 'processor'):
            self.processor.stop()

    def processing_finished(self):
        self.status_label.setText("Processing complete!")
        self.set_controls_enabled(True)
        self.pause_button.setText("Pause")
        QMessageBox.information(self, "Success", "All items have been processed successfully!")

    def processing_error(self, error_msg):
        self.status_label.setText("An error occurred.")
        self.set_controls_enabled(True)
        self.pause_button.setText("Pause")
        QMessageBox.critical(self, "Processing Error", f"An error occurred:\n{error_msg}")

    def load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
            except Exception:
                settings = DEFAULT_SETTINGS
        else:
            settings = DEFAULT_SETTINGS
        
        self.api_key_input.setText(settings.get('api_key', ''))
        self.prompt_edit.setText(settings.get('prompt', ''))
        self.md_path_input.setText(settings.get('input_folder', ''))
        self.output_path_input.setText(settings.get('output_folder', ''))
        self.word_input.setText(settings.get('single_word', ''))

        if self.md_path_input.text():
            self.load_files_from_folder(self.md_path_input.text())
    
    def save_settings(self):
        settings = {
            'api_key': self.api_key_input.text(),
            'prompt': self.prompt_edit.toPlainText(),
            'input_folder': self.md_path_input.text(),
            'output_folder': self.output_path_input.text(),
            'single_word': self.word_input.text()
        }
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Could not save settings: {e}")

    def closeEvent(self, event):
        self.save_settings()
        event.accept()

    def filter_files(self):
        search_text = self.search_input.text().lower()
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            item.setHidden(search_text not in item.text().lower())

    def toggle_select_all(self):
        all_selected = all(self.file_list.item(i).isSelected() for i in range(self.file_list.count()) if not self.file_list.item(i).isHidden())
        if all_selected:
            self.file_list.clearSelection()
            self.select_all_button.setText("Select All")
        else:
            for i in range(self.file_list.count()):
                if not self.file_list.item(i).isHidden():
                    self.file_list.item(i).setSelected(True)
            self.select_all_button.setText("Deselect All")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    # Use a dummy icon file name for the path function to work
    # You MUST create an 'app_icon.ico' file in the same directory as the script
    # or the bundled .exe for the icon to appear.
    try:
        if os.path.exists('app_icon.ico'):
             app.setWindowIcon(QIcon(resource_path('app_icon.ico')))
    except Exception as e:
        print(f"Could not load app icon: {e}")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
