import dns.resolver
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

def fetch_dns():
    domain = entry.get()
    record_types = ['A', 'AAAA', 'NS', 'CNAME', 'MX', 'PTR', 'SOA', 'TXT']
    output.delete(1.0, tk.END)
    
    for records in record_types:
        try:
            answer = dns.resolver.resolve(domain, records)
            output.insert(tk.END, f'\n{records} Records\n')
            output.insert(tk.END, '-'*30 + '\n')
            for server in answer:
                output.insert(tk.END, f'{server.to_text()}\n')
                
        except dns.resolver.NoAnswer:
            pass
        except dns.resolver.NXDOMAIN:
            output.insert(tk.END, f'{domain} **DOES\'NT EXIST**\n')
            break
        except Exception as e:
            output.insert(tk.END, f'An error occurred: {e}\n')
            break

def save_output():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w") as f:
            f.write(output.get(1.0, tk.END))

# GUI Setup
root = tk.Tk()
root.title("DNS Enumeration")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

entry = ttk.Entry(frame, width=40)
entry.grid(row=0, column=0, sticky=(tk.W, tk.E))
entry.insert(0, "Enter domain here")

fetch_button = ttk.Button(frame, text="Fetch DNS Records", command=fetch_dns)
fetch_button.grid(row=0, column=1)

save_button = ttk.Button(frame, text="Save Output", command=save_output)
save_button.grid(row=0, column=2)

output = tk.Text(frame, wrap=tk.WORD, width=100, height=50)
output.grid(row=1, columnspan=3, sticky=(tk.W, tk.E))

root.mainloop()
