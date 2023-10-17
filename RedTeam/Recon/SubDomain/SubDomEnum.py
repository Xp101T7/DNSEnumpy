import dns.resolver
import tkinter as tk
from tkinter import filedialog

def load_subdomains_from_file(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f]

def is_valid_domain(domain):
    if len(domain) > 255:
        return False
    labels = domain.split('.')
    for label in labels:
        if len(label) > 63:
            return False
    return True

def run_resolver():
    domain = domain_entry.get()
    file_path = file_path_entry.get()
    
    if not is_valid_domain(domain):
        output_text.insert(tk.END, "Invalid domain name.\n")
        root.update_idletasks()
        return

    subdomain_array = load_subdomains_from_file(file_path)
    
    output_text.delete(1.0, tk.END)
    for subdoms in subdomain_array:
        full_domain = f'{subdoms}.{domain}'
        if not is_valid_domain(full_domain):
            output_text.insert(tk.END, f"Invalid subdomain: {full_domain}\n")
            root.update_idletasks()
            continue

        try:
            ip_value = dns.resolver.resolve(full_domain, 'A')
            if ip_value:
                output_text.insert(tk.END, f'{full_domain} PWN_ABLE\n')
                root.update_idletasks()
        except dns.resolver.NXDOMAIN:
            pass
        except dns.resolver.NoAnswer:
            pass

def browse_file():
    file_path = filedialog.askopenfilename()
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, file_path)

def save_output():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w') as f:
            f.write(output_text.get(1.0, tk.END))

# GUI code
root = tk.Tk()
root.title('Sub Domain Finder')

# Set root background to dark
root.configure(bg='black')

# Modify label, button, and entry widgets
dark_label_opts = {'bg': 'black', 'fg': 'white'}
dark_entry_opts = {'bg': '#333', 'fg': 'white', 'insertbackground': 'white'}
dark_button_opts = {'bg': '#333', 'fg': 'white', 'activebackground': '#555', 'activeforeground': 'white'}
dark_text_opts = {'bg': '#333', 'fg': '#00FF00', 'insertbackground': 'white'}


domain_label = tk.Label(root, text="Enter Domain:", **dark_label_opts)
domain_label.grid(row=0, column=0, sticky="w")

domain_entry = tk.Entry(root, **dark_entry_opts)
domain_entry.grid(row=0, column=1, columnspan=2, sticky="ew")

file_path_label = tk.Label(root, text="Subdomain File:", **dark_label_opts)
file_path_label.grid(row=1, column=0, sticky="w")

file_path_entry = tk.Entry(root, **dark_entry_opts)
file_path_entry.grid(row=1, column=1, sticky="ew")

browse_button = tk.Button(root, text="Browse", command=browse_file, **dark_button_opts)
browse_button.grid(row=1, column=2, sticky="e")

# Run and Save buttons next to each other
run_button = tk.Button(root, text="Run", command=run_resolver, **dark_button_opts)
run_button.grid(row=2, column=1, sticky="e")

save_button = tk.Button(root, text="Save", command=save_output, **dark_button_opts)
save_button.grid(row=2, column=2, sticky="w")

output_text = tk.Text(root, height=45, width=50, **dark_text_opts)
output_text.grid(row=4, columnspan=3)

# Create Scrollbar and associate with Text widget
scrollbar = tk.Scrollbar(root, orient="vertical", command=output_text.yview)
scrollbar.grid(row=4, column=3, sticky="ns")

output_text['yscrollcommand'] = scrollbar.set

# Make the entry widgets expandable
root.grid_columnconfigure(1, weight=1)

root.mainloop()
