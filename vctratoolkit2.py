import smtplib
import requests
import speedtest
import webbrowser
import time
import socket
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from bs4 import BeautifulSoup
from urllib.parse import urljoin

console = Console()

EMAIL = "nexelix.smtp.expl@gmail.com"
PASSWORD = "vova cfmk wjwa odko"

def cool_loading(text="Loading..."):
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task(f"[cyan]{text}", total=None)
        time.sleep(2)

def show_menu():
    console.print(Panel.fit("[bold green]PROJECT VCTRA TOOLKIT", title="[bold cyan]Main Menu"))
    console.print("[1] SMTP Email Spammer")
    console.print("[2] Website Vulnerability Tester")
    console.print("[3] IP Address Tracker")
    console.print("[4] Internet Speed Tester")
    console.print("[5] Directory Brute Forcer")
    console.print("[6] Port Scanner")
    console.print("[7] JavaScript Link Crawler")
    console.print("[0] Exit")

def smtp_spammer():
    target_email = console.input("[bold red]Enter Target Email: ")
    user_message = console.input("[bold red]Enter message to send: ")
    subject = "Spam Alert!"
    message = f"Subject: {subject}\n\n{user_message}"
    console.print("[yellow]Starting high-speed spam loop (CTRL+C to stop)...")
    while True:
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(EMAIL, PASSWORD)
                server.sendmail(EMAIL, target_email, message)
                console.print(f"[green]Sent to {target_email}")
        except Exception as e:
            console.print(f"[red]Error: {e}")
            break

def form_detector(url):
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        forms = soup.find_all('form')
        console.print(f"[green]Found {len(forms)} forms.")
        for i, form in enumerate(forms, start=1):
            console.print(f"\n[bold cyan]Form {i}:")
            console.print(f"Action: {form.get('action')}")
            console.print(f"Method: {form.get('method')}")
            inputs = form.find_all('input')
            for input_field in inputs:
                console.print(f"  - Input: {input_field.get('name')} (type: {input_field.get('type')})")
    except Exception as e:
        console.print(f"[red]Form detection failed: {e}")

def subdomain_finder(domain):
    subdomains = ['www', 'mail', 'admin', 'ftp', 'test', 'blog']
    for sub in subdomains:
        url = f"http://{sub}.{domain}"
        try:
            res = requests.get(url, timeout=2)
            if res.status_code < 400:
                console.print(f"[green]Found: {url}")
        except:
            continue

def directory_brute_force(url):
    wordlist = ['admin', 'login', 'uploads', 'images', 'css', 'js', 'dashboard']
    console.print("[yellow]Starting directory brute-force scan...")
    for word in wordlist:
        full_url = urljoin(url, word)
        try:
            r = requests.get(full_url)
            if r.status_code < 400:
                console.print(f"[green]Found: {full_url}")
        except:
            pass

def port_scanner():
    target = console.input("[bold blue]Enter target IP or domain: ")
    ports = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 8080]
    console.print("[yellow]Scanning ports...")
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target, port))
            if result == 0:
                console.print(f"[green]Port {port} is open")
            sock.close()
        except Exception as e:
            console.print(f"[red]Error scanning port {port}: {e}")

def js_link_crawler():
    url = console.input("[bold blue]Enter URL to scan JS links: ")
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        js_links = []
        for tag in soup.find_all(['a', 'script']):
            link = tag.get('href') or tag.get('src')
            if link and 'javascript' in link.lower():
                js_links.append(link)
        if js_links:
            console.print(f"[green]Found {len(js_links)} JS-related links:")
            for link in js_links:
                console.print(f" - {link}")
        else:
            console.print("[red]No JS-based links found.")
    except Exception as e:
        console.print(f"[red]Error: {e}")

def vuln_tester():
    url = console.input("[bold blue]Enter website URL (e.g., https://example.com): ")
    cool_loading("Testing Vulnerabilities")
    tests = {
        "HTTP Headers": url,
        "SQL Injection Test": url + "'",
        "XSS Test": url + "<script>alert(1)</script>",
        "robots.txt": url + "/robots.txt",
        "Admin Panel": url + "/admin"
    }
    for name, link in tests.items():
        try:
            r = requests.get(link)
            console.print(f"[cyan]{name} => [green]{r.status_code}")
        except:
            console.print(f"[red]{name} => Failed")
    form_detector(url)
    domain = url.replace("https://", "").replace("http://", "").split("/")[0]
    subdomain_finder(domain)

def ip_tracker():
    ip = console.input("[bold magenta]Enter IP address: ")
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}").json()
        for key in ['query','country','regionName','city','zip','lat','lon','isp','org','as']:
            console.print(f"[green]{key.capitalize()}: [white]{res.get(key)}")
        lat, lon = res.get('lat'), res.get('lon')
        if lat and lon:
            maps_url = f"https://www.google.com/maps?q={lat},{lon}"
            console.print(f"\n[bold green]Google Maps Link: [underline blue]{maps_url}")
            open_map = console.input("[bold yellow]Do you want to open location in Google Maps? (yes/no): ").strip().lower()
            if open_map == "yes":
                webbrowser.open(maps_url)
                console.print("[bold cyan]Opened location on Google Maps.")
            else:
                console.print("[bold magenta]Skipped opening Google Maps.")
    except Exception as e:
        console.print(f"[red]Error: {e}")

def internet_speed_test():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download = st.download() / 1_000_000
        upload = st.upload() / 1_000_000
        console.print(f"[green]Download: {download:.2f} Mbps")
        console.print(f"[green]Upload: {upload:.2f} Mbps")
    except Exception as e:
        console.print(f"[red]Speed test error: {e}")

if __name__ == "__main__":
    cool_loading("Booting PROJECT VCTRA TOOLKIT...")
    while True:
        show_menu()
        choice = console.input("\n[bold cyan]Choose an option: ")

        if choice == '1':
            cool_loading("Launching Email Spammer")
            smtp_spammer()
        elif choice == '2':
            vuln_tester()
        elif choice == '3':
            cool_loading("Launching IP Tracker")
            ip_tracker()
        elif choice == '4':
            cool_loading("Launching Speed Test")
            internet_speed_test()
        elif choice == '5':
            url = console.input("[bold blue]Enter website URL to brute force: ")
            directory_brute_force(url)
        elif choice == '6':
            port_scanner()
        elif choice == '7':
            js_link_crawler()
        elif choice == '0':
            console.print("[bold red]Exiting...")
            break
        else:
            console.print("[red]Invalid option. Try again.")