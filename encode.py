import tkinter as tk
from tkinter import scrolledtext, messagebox
import base64
import os

clipboard_snippet = ""

def encode_script():
    global clipboard_snippet
    raw_script = input_text.get("1.0", tk.END).rstrip()
    filename = filename_entry.get().strip()
    folder = folder_entry.get().strip()
    if not raw_script:
        messagebox.showwarning("Empty Input", "Please paste your script into the input box.")
        return

    if not filename:
        filename = "decoded.txt"
    if not folder:
        folder = "$desktop = [Environment]::GetFolderPath(\"Desktop\")"
        path_expr = "$outputPath = Join-Path $desktop \"{}\"".format(filename)
    else:
        path_expr = "$outputPath = \"{}\\{}\"".format(folder, filename)
        folder = ""

    # Encode the script to base64
    encoded_bytes = base64.b64encode(raw_script.encode("utf-8"))
    encoded_str = encoded_bytes.decode("utf-8")

    # Create PowerShell snippet with newlines between commands
    clipboard_snippet = (
        f"$encoded = \"{encoded_str}\"\n\n"
        "$decoded = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($encoded))\n\n"
        f"{folder}\n\n"
        f"{path_expr}\n\n"
        "$decoded | Set-Content $outputPath\n\n"
        "Write-Host \"Saved to: $outputPath\""
    )

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, clipboard_snippet)

def generate_linux_snippet():
    raw_script = input_text.get("1.0", tk.END).rstrip()
    filename = filename_entry.get().strip()
    folder = folder_entry.get().strip()
    if not raw_script:
        messagebox.showwarning("Empty Input", "Please paste your script into the input box.")
        return

    if not filename:
        filename = "decoded.txt"
    if not folder:
        filepath = f"~/Desktop/{filename}"
    else:
        filepath = f"{folder.rstrip('/')}/{filename}"

    encoded_bytes = base64.b64encode(raw_script.encode("utf-8"))
    encoded_str = encoded_bytes.decode("utf-8")

    linux_snippet = (
        f"echo '{encoded_str}' | base64 -d > {filepath}\n\n"
        f"echo 'Saved to {filepath}'"
    )

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, linux_snippet)

def copy_to_clipboard():
    window.clipboard_clear()
    window.clipboard_append(output_text.get("1.0", tk.END).strip())
    window.update()
    messagebox.showinfo("Copied", "Code copied to clipboard.")

# GUI setup
window = tk.Tk()
window.title("Script Clipboard Encoder for VM Paste")
window.geometry("800x750")
window.configure(bg="#2e2e2e")

# Styling for dark mode
label_style = {"bg": "#2e2e2e", "fg": "#f0f0f0"}
entry_style = {"bg": "#3c3c3c", "fg": "#ffffff", "insertbackground": "white"}
text_style = {"bg": "#1e1e1e", "fg": "#dcdcdc", "insertbackground": "white"}
button_style = {"bg": "#444", "fg": "#fff", "activebackground": "#666", "activeforeground": "#fff"}

# Input field
tk.Label(window, text="Paste your script here:", **label_style).pack(anchor='w')
input_text = scrolledtext.ScrolledText(window, height=15, width=100, **text_style)
input_text.pack(padx=10, pady=5)

# Filename input
tk.Label(window, text="Output filename (default: decoded.txt):", **label_style).pack(anchor='w')
filename_entry = tk.Entry(window, width=50, **entry_style)
filename_entry.insert(0, "decoded.txt")
filename_entry.pack(padx=10, pady=5)

# Folder input
tk.Label(window, text="Output folder (default: Desktop):", **label_style).pack(anchor='w')
folder_entry = tk.Entry(window, width=50, **entry_style)
folder_entry.pack(padx=10, pady=5)

# Encode buttons
tk.Button(window, text="Generate PowerShell Snippet", command=encode_script, **button_style).pack(pady=5)
tk.Button(window, text="Generate Linux Snippet", command=generate_linux_snippet, **button_style).pack(pady=5)

# Output field
tk.Label(window, text="Step 1: Paste this into the VM", **label_style).pack(anchor='w')
output_text = scrolledtext.ScrolledText(window, height=15, width=100, **text_style)
output_text.pack(padx=10, pady=5)

# Copy to clipboard button
tk.Button(window, text="Copy to Clipboard", command=copy_to_clipboard, **button_style).pack(pady=10)

# Start the GUI loop
window.mainloop()