import tkinter as tk
from tkinter import scrolledtext, messagebox
import base64
import os
import textwrap

clipboard_snippet = ""

def encode_script():
    global clipboard_snippet
    raw_script = input_text.get("1.0", tk.END).rstrip()
    filename = filename_entry.get().strip()
    folder = folder_entry.get().strip()
    split_length = split_entry.get().strip()

    if not raw_script:
        messagebox.showwarning("Empty Input", "Please paste your script into the input box.")
        return

    if not filename:
        filename = "decoded.txt"

    try:
        split_length = int(split_length) if split_length else None
    except ValueError:
        messagebox.showerror("Invalid Input", "Split length must be an integer.")
        return

    # Encode the script to base64
    encoded_bytes = base64.b64encode(raw_script.encode("utf-8"))
    encoded_str = encoded_bytes.decode("utf-8")

    # Split the base64 string if split_length is specified
    if split_length:
        parts = textwrap.wrap(encoded_str, split_length)
        assignment_lines = [f"$encoded{idx} = \"{part}\"" for idx, part in enumerate(parts)]
        combine_line = "$encoded = " + " + ".join([f"$encoded{idx}" for idx in range(len(parts))])
    else:
        assignment_lines = [f"$encoded = \"{encoded_str}\""]
        combine_line = ""

    if not folder:
        folder_cmd = "$desktop = [Environment]::GetFolderPath(\"Desktop\")"
        path_expr = f"$outputPath = Join-Path $desktop \"{filename}\""
    else:
        folder_cmd = ""
        path_expr = f"$outputPath = \"{folder}\\{filename}\""

    # Create PowerShell snippet with newlines between commands
    clipboard_snippet = (
        "\n\n".join(assignment_lines) +
        (f"\n\n{combine_line}" if split_length else "") +
        f"\n\n$decoded = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($encoded))\n\n"
        f"{folder_cmd}\n\n"
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
    split_length = split_entry.get().strip()

    if not raw_script:
        messagebox.showwarning("Empty Input", "Please paste your script into the input box.")
        return

    if not filename:
        filename = "decoded.txt"
    if not folder:
        basepath = "~/Desktop"
    else:
        basepath = folder.rstrip('/')

    filepath = f"{basepath}/{filename}"

    try:
        split_length = int(split_length) if split_length else None
    except ValueError:
        messagebox.showerror("Invalid Input", "Split length must be an integer.")
        return

    encoded_bytes = base64.b64encode(raw_script.encode("utf-8"))
    encoded_str = encoded_bytes.decode("utf-8")

    if split_length:
        parts = textwrap.wrap(encoded_str, split_length)
        echo_lines = [f"echo '{part}' >> /tmp/tmp.b64" for part in parts]
        decode_line = f"base64 -d /tmp/tmp.b64 > {filepath}"
        clean_line = "rm /tmp/tmp.b64"
        linux_snippet = "\n\n".join(echo_lines + [decode_line, clean_line, f"echo 'Saved to {filepath}'"])
    else:
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
window.geometry("800x800")
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

# Split size input
tk.Label(window, text="Split encoded string every N characters (optional):", **label_style).pack(anchor='w')
split_entry = tk.Entry(window, width=50, **entry_style)
split_entry.pack(padx=10, pady=5)

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
