
# Script Clipboard Encoder for VM Paste

A simple, cross-platform GUI tool for safely transferring multiline scripts into restrictive VM consoles. This tool Base64-encodes your script and outputs a compatible decoding snippet for either Windows PowerShell or Linux bash.


---

## Features

-  Base64-encodes multiline scripts to preserve formatting
-  Outputs ready-to-paste decoding snippets for:
  - **PowerShell** (Windows 7+)
  - **Bash** (Linux/Ubuntu)
-  One-click copy to clipboard
-  Optional filename and output directory control

---

## Getting Started

### Run the Python Script

1. Make sure you have Python 3.6+
2. Launch the GUI:
   ```bash
   python encode.py
   ```

---

### Build Standalone `.exe`

To build a single Windows executable (no Python required to run):

```bash
pyinstaller --onefile --noconsole encode.py
```

The `.exe` will be in the `dist/` directory.

---

## How to Use

1. Paste your source script into the top box.
2. Optionally specify an output filename and folder.
3. Click `Generate PowerShell Snippet` or `Generate Linux Snippet`.
4. Copy the output to your clipboard with one click.
5. Paste it into the VM console (or browser input tool).
6. Run the commands to decode and save the original script.

---

## Why?

Some VMs strip or collapse newlines when pasting into remote consoles. This tool ensures your full script makes it intact — no manual escaping or reformatting required.

---

## 📁 Output Examples

### PowerShell
```powershell
$encoded = "..."
$decoded = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($encoded))

$desktop = [Environment]::GetFolderPath("Desktop")

$outputPath = Join-Path $desktop "decoded.txt"

$decoded | Set-Content $outputPath

Write-Host "Saved to: $outputPath"
```

### Linux
```bash
echo '...' | base64 -d > ~/Desktop/decoded.txt

echo 'Saved to ~/Desktop/decoded.txt'
```
